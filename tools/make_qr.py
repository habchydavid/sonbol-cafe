#!/usr/bin/env python3
"""Make the table QR code (print/sonbol-qr.svg and .png).

Usage:  pip install segno && python3 tools/make_qr.py [URL]

Error correction is level Q: about a quarter of the code can be scratched,
stained or covered and it still scans. The 4-module white quiet zone around
it is part of the file; don't crop it when printing.
If the site moves to its own domain, rerun with the new URL and reprint.
"""
import sys
from pathlib import Path

import segno

URL = sys.argv[1] if len(sys.argv) > 1 else "https://habchydavid.github.io/sonbol-cafe/"
OUT = Path(__file__).resolve().parent.parent / "print"
INK = "#241F19"   # brand ink; 15.9:1 against white, as readable to a scanner as black

qr = segno.make(URL, error="q", boost_error=False)
OUT.mkdir(exist_ok=True)
qr.save(OUT / "sonbol-qr.svg", scale=10, border=4, dark=INK, light="#FFFFFF",
        xmldecl=False, svgns=True, title="Sonbol Cafe website", desc=URL)
qr.save(OUT / "sonbol-qr.png", scale=48, border=4, dark=INK, light="#FFFFFF")
print(f"{URL}\nversion {qr.version}, error level {qr.error}, {qr.symbol_size(border=0)[0]} modules")
