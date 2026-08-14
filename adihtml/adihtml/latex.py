"""
Native lualatex SVG renderer for adihtml.

Tex(src=..., file=..., scale=..., alt=...) -> <img> tag referencing an
adihtmltex_{sha3_512}.svg asset colocated with the calling generator .py.

Caching lives in a colocated tex.json:

  {
    "tex_literals": { "{sha3_512(src)}": "" },
    "tex_files":    { "./example.tex": "{sha3_512(file_contents)}" }
  }

A cache hit (key present for a literal, value match for a file) skips
recompilation. Dirty inputs are compiled via lualatex (PDF) then pdf2svg
into the caller's directory.
"""

import hashlib
import inspect
import json
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

_SVG_PREFIX = "adihtmltex_"
_TEX_JSON_NAME = "tex.json"


def _sha3_512(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _caller_dir(caller_frame) -> Path:
    return Path(caller_frame.filename).resolve().parent


def _load_tex_json(directory: Path) -> dict:
    path = directory / _TEX_JSON_NAME
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}
    data.setdefault("tex_literals", {})
    data.setdefault("tex_files", {})
    return data


def _save_tex_json(directory: Path, data: dict) -> None:
    path = directory / _TEX_JSON_NAME
    tmp = directory / f".{_TEX_JSON_NAME}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


def _compile_to_svg(tex_source: str, out_svg: Path) -> None:
    """Compile a complete TeX document to a single-page SVG via lualatex + pdf2svg."""
    workdir = Path(tempfile.gettempdir()) / "opencode" / "latex" / str(uuid.uuid4())
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        tex_path = workdir / "input.tex"
        tex_path.write_text(tex_source, encoding="utf-8")

        proc = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "input.tex"],
            cwd=str(workdir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.returncode != 0:
            log_path = workdir / "input.log"
            log_tail = ""
            if log_path.exists():
                log_tail = log_path.read_text(encoding="utf-8", errors="replace")[-2000:]
            raise RuntimeError(
                f"lualatex failed (exit {proc.returncode}) for tex source:\n"
                f"{tex_source}\n--- log tail ---\n{log_tail}"
            )

        pdf_path = workdir / "input.pdf"
        if not pdf_path.exists():
            raise RuntimeError(
                f"lualatex produced no PDF for tex source:\n{tex_source}\n"
                f"stdout:\n{proc.stdout}"
            )

        svg_proc = subprocess.run(
            ["pdf2svg", str(pdf_path), str(out_svg), "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if svg_proc.returncode != 0:
            raise RuntimeError(
                f"pdf2svg failed (exit {svg_proc.returncode}):\n{svg_proc.stdout}"
            )
        if not out_svg.exists():
            raise RuntimeError(f"pdf2svg produced no SVG at {out_svg}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _svg_intrinsic_size(svg_path: Path):
    """Best-effort parse of width/height from an SVG. Returns (w, h) as floats or None."""
    try:
        text = svg_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    import re
    w = re.search(r'\bwidth="([^"]+)"', text)
    h = re.search(r'\bheight="([^"]+)"', text)
    if not w or not h:
        return None

    def _to_px(val: str) -> float | None:
        m = re.match(r"^([\d.]+)", val)
        return float(m.group(1)) if m else None

    wp = _to_px(w.group(1))
    hp = _to_px(h.group(1))
    if wp is None or hp is None:
        return None
    return (wp, hp)


def Tex(src: str | None = None, *, file: str | None = None, scale: float = 1.0, alt: str = "", **kwargs) -> str:
    """
    Render TeX to an <img> referencing adihtmltex_{sha3_512}.svg.

    Exactly one of `src` (literal TeX document source) or `file` (path to a .tex
    file, relative to the calling .py) must be provided. `scale` is applied as
    CSS width/height on the <img> (caller-applied; not a cache key). Extra
    **kwargs become HTML attributes (className -> class), like core._tagCore.
    """
    if (src is None) == (file is None):
        raise ValueError("Tex: provide exactly one of `src` or `file`")
    if "alt" in kwargs:
        raise ValueError("Tex: pass `alt` only as the named parameter, not in kwargs")

    directory = _caller_dir(inspect.stack()[1])
    data = _load_tex_json(directory)

    if src is not None:
        src_bytes = src.encode("utf-8")
        h = _sha3_512(src_bytes)
        svg_name = f"{_SVG_PREFIX}{h}.svg"
        svg_path = directory / svg_name
        dirty = h not in data["tex_literals"]
        tex_source = src
        is_literal = True
    else:
        tex_path = (directory / file).resolve()
        src_bytes = tex_path.read_bytes()
        h = _sha3_512(src_bytes)
        svg_name = f"{_SVG_PREFIX}{h}.svg"
        svg_path = directory / svg_name
        dirty = data["tex_files"].get(file) != h
        tex_source = src_bytes.decode("utf-8")
        is_literal = False

    if dirty or not svg_path.exists():
        _compile_to_svg(tex_source, svg_path)
        if is_literal:
            data["tex_literals"][h] = ""
        else:
            data["tex_files"][file] = h
        _save_tex_json(directory, data)

    attrs = {"src": svg_name, "alt": alt}

    size = _svg_intrinsic_size(svg_path)
    if size is not None and scale != 1.0:
        w, hh = size
        attrs["width"] = str(w * scale)
        attrs["height"] = str(hh * scale)
    elif scale != 1.0:
        attrs["style"] = f"transform: scale({scale}); transform-origin: top left;"

    for k, v in kwargs.items():
        key = "class" if k == "className" else k
        attrs[key] = v

    attr_str = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f"<img{attr_str}>"