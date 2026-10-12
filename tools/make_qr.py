#!/usr/bin/env python3
"""Make the table QR code (print/sonbol-qr.svg and .png).

Usage:  python3 -m venv /tmp/qrenv && /tmp/qrenv/bin/pip install segno
        /tmp/qrenv/bin/python tools/make_qr.py [URL]

Error correction is level H, the highest: about 30% of the code can be
scratched, stained or covered and it still scans (the three big corner
squares must stay visible). The 4-module white quiet zone around
it is part of the file; don't crop it when printing.
This writes the QR images only. If the address ever changes, rerun with the
new URL, then re-export both PDFs from print/table-card.html (see README).
"""
import sys
from pathlib import Path

import segno

URL = sys.argv[1] if len(sys.argv) > 1 else "https://sonbol.cafe/"
OUT = Path(__file__).resolve().parent.parent / "print"
INK = "#241F19"   # brand ink; 16.3:1 against white, as readable to a scanner as black

qr = segno.make(URL, error="h", boost_error=False)
OUT.mkdir(exist_ok=True)
qr.save(OUT / "sonbol-qr.svg", scale=10, border=4, dark=INK, light="#FFFFFF",
        xmldecl=False, svgns=True, title="Sonbol Cafe website", desc=URL)
qr.save(OUT / "sonbol-qr.png", scale=48, border=4, dark=INK, light="#FFFFFF")
print(f"{URL}\nversion {qr.version}, error level {qr.error}, {qr.symbol_size(border=0)[0]} modules")
