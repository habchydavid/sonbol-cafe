#!/usr/bin/env python3
"""WCAG AA contrast check for every theme in index.html.

Usage:  python3 tools/check-contrast.py

Reads the palette and every theme block (:root/.theme-light, .theme-<name>),
resolves the semantic tokens and checks each foreground/background pairing the
page uses. Exits non-zero if any pairing fails, or if the OS-dark media block
has drifted from .theme-dark. New themes are picked up automatically.
"""
import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "index.html"

TEXT, UI = 4.5, 3.0   # WCAG 1.4.3 normal text; 1.4.11 controls, focus, states

# (foreground, background, minimum, where it appears)
PAIRS = []
for bg in ("bg", "surface", "surface-alt"):
    PAIRS += [
        ("text", bg, TEXT, "body text, headings, input text"),
        ("text-muted", bg, TEXT, "ledes, labels, notes, footer"),
        ("text-accent", bg, TEXT, "eyebrows, story numbers, link hover"),
        ("text-emphasis", bg, TEXT, "prices"),
        ("focus", bg, UI, "focus ring, hovered control border"),
    ]
for bg in ("bg", "surface"):
    PAIRS += [("border-control", bg, UI, "input, tab, toggle and copy-button borders")]
PAIRS += [
    ("on-action", "action", TEXT, "primary button label"),
    ("on-selected", "selected", TEXT, "selected menu tab"),
    ("on-toggle", "toggle", TEXT, "active language"),
    ("bg", "text", TEXT, "outline button on hover"),
    ("selected", "bg", UI, "selected tab against the page"),
    ("toggle", "bg", UI, "active language against the header"),
]


def luminance(hex_):
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    def chan(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def decls(body):
    return dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", body))


def main():
    css = HTML.read_text(encoding="utf-8")
    palette = {}
    for body in re.findall(r":root\{([^}]*--palette-[^}]*)\}", css):
        palette.update(decls(body))

    themes = {}
    for sel, body in re.findall(r"\n(:root, \.theme-light|\.theme-[\w-]+)\{([^}]*)\}", css):
        if "--color-" not in body:
            continue   # a component that happens to start with .theme-, not a theme
        name = "light" if "theme-light" in sel else sel.split("theme-", 1)[1]
        themes[name] = decls(body)

    def resolve(val, seen=()):
        m = re.fullmatch(r"var\(--([\w-]+)\)", val.strip())
        if not m:
            return val.strip()
        return resolve(palette[m.group(1)], seen + (m.group(1),))

    failed = 0
    for name, toks in themes.items():
        colors = {k[len("color-"):]: resolve(v) for k, v in toks.items() if k.startswith("color-")}
        print(f"\n{name}")
        for fg, bg, need, where in PAIRS:
            if fg not in colors or bg not in colors:
                print(f"  MISSING  --color-{fg if fg not in colors else bg}")
                failed += 1
                continue
            r = ratio(colors[fg], colors[bg])
            ok = r >= need
            failed += not ok
            print(f"  {'ok  ' if ok else 'FAIL'} {r:5.2f} >= {need}  {fg} on {bg}  ({where})")

    auto = re.search(r"prefers-color-scheme:dark\)\{\s*:root:not\(\[class\*=\"theme-\"\]\)\{([^}]*)\}", css)
    if auto and "dark" in themes:
        drift = {k for k in set(decls(auto.group(1))) | set(themes["dark"])
                 if decls(auto.group(1)).get(k) != themes["dark"].get(k)}
        if drift:
            print("\nFAIL  OS-dark block differs from .theme-dark:", ", ".join(sorted(drift)))
            failed += 1
        else:
            print("\nok    OS-dark block mirrors .theme-dark")

    print(f"\n{'all pairings pass' if not failed else f'{failed} failing'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
