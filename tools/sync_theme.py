#!/usr/bin/env python3
"""Copy assets/theme.css into index.html.

Usage:  python3 tools/sync_theme.py

assets/theme.css is the one place to edit fonts and theme colours. The text
pages link to it; index.html carries an inline copy between the theme:start /
theme:end markers so the first screen paints without waiting for a CSS file.
Run this after editing theme.css. tools/check-contrast.py fails if they differ.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- theme:start -->", "<!-- theme:end -->"


def inline_css():
    css = (ROOT / "assets" / "theme.css").read_text(encoding="utf-8")
    # url() paths in theme.css are relative to assets/; inline they're relative to the page
    return css.replace("url(fonts/", "url(assets/fonts/")


def block():
    return f"{START}\n<style>\n{inline_css()}</style>\n{END}"


def in_sync():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(re.escape(START) + r".*?" + re.escape(END), html, re.S)
    return bool(m) and m.group(0) == block()


def main():
    page = ROOT / "index.html"
    html = page.read_text(encoding="utf-8")
    new, n = re.subn(re.escape(START) + r".*?" + re.escape(END), lambda _: block(), html, flags=re.S)
    if n != 1:
        raise SystemExit("index.html needs exactly one theme:start / theme:end block")
    page.write_text(new, encoding="utf-8")
    print("index.html updated from assets/theme.css")


if __name__ == "__main__":
    main()
