---
id: 01a0022b-44fc-7365-a663-cf44b5984eae
status: in_progress
priority: medium
assignee: adithya.yerramsetty@gmail.com
created: 2026-08-14T21:26:30.000Z
---

# Native lualatex SVG renderer in adihtml

Add first-class LaTeX support to adihtml so posts can render equations and
figures via `lualatex` -> PDF -> `pdf2svg` -> SVG, with content-addressed
caching so unchanged inputs are never recompiled.

## Deliverables

1. `adihtml/adihtml/latex.py` exposing `Tex(src=None, *, file=None, scale=1.0, alt="")`
   returning an `<img>` tag referencing `adihtmltex_{sha3_512}.svg`.
   - Literal `src` is cached under `tex_literals` keyed by `sha3_512(src)`.
   - `file` (path relative to the calling `.py`) is cached under `tex_files`
     keyed by the path with value `sha3_512(file_contents)`.
   - Dirty inputs are compiled in a temp dir under `/tmp/opencode/latex/`
     via `lualatex -interaction=nonstopmode -halt-on-error` then
     `pdf2svg input.pdf <dir>/adihtmltex_{h}.svg 1`.
   - `scale` is caller-applied CSS (emitted as `<img>` width/height from the
     SVG intrinsic size x scale); it is NOT part of the cache key.
   - `tex.json` (schema `{"tex_literals": {}, "tex_files": {}}`) is colocated
     with the calling `.py` and written atomically.

2. `autobuild.py` watches, per `index.py`, every path declared by a `#DEPS <path>`
   line (regex `#DEPS\s+(\S+)`, resolved relative to the `.py`'s dir). A change
   to any `#DEPS` file re-runs that `.py`'s builder.

3. `scripts/clean_latex.py` recursively nukes every `adihtmltex_*.svg` and every
   colocated `tex.json` under `serve/`.

4. `.gitignore` ignores `adihtmltex_*.svg` and `tex.json` (regenerable build
   artifacts, like `.issuescache.sqlite`).

## Success criteria

- A generator `.py` under `serve/` that calls `Tex(...)` with a literal TeX
  string AND with a `file=` argument produces `adihtmltex_{sha3_512}.svg`
  files and a `tex.json` colocated with it, visible in the rendered HTML via
  `<img>`.
- A second `autobuild.py` run with unchanged inputs does NOT invoke `lualatex`
  for the already-cached entries (no-op rebuild).
- Touching a `#DEPS`-declared `.tex` file triggers a rebuild of the watching
  `.py` on the next `autobuild.py` poll.
- `python3 scripts/clean_latex.py` removes all `adihtmltex_*.svg` and `tex.json`
  files under `serve/`, and a subsequent `autobuild.py` run regenerates them.