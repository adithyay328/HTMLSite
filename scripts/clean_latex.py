#!/usr/bin/env python3
"""
Nuke adihtml lualatex build artifacts under serve/.

Deletes every adihtmltex_*.svg and every colocated tex.json found beneath
serve/. These are regenerable build outputs of the adihtml latex renderer;
re-running autobuild.py restores them.
"""
import pathlib

SERVE = pathlib.Path("serve")


def main():
    if not SERVE.is_dir():
        print(f"no serve/ directory at {SERVE.resolve()}; nothing to clean")
        return

    svgs_removed = 0
    jsons_removed = 0

    for p in SERVE.rglob("*"):
        if not p.is_file():
            continue
        name = p.name
        if name.startswith("adihtmltex_") and name.endswith(".svg"):
            p.unlink()
            svgs_removed += 1
        elif name == "tex.json":
            p.unlink()
            jsons_removed += 1

    print(f"clean_latex: removed {svgs_removed} svg(s) and {jsons_removed} tex.json(s) under serve/")


if __name__ == "__main__":
    main()