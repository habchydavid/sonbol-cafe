# Sonbol Cafe

Website for Sonbol Cafe, Deir El Ahmar (Bekaa, Lebanon).

A single static page (`index.html`) with the menu, La Formule set menu, a WhatsApp reservation form, and English / French / Arabic versions. Host it on any static host (e.g. GitHub Pages).

## Themes

Colours and fonts live in `assets/theme.css`, shared by every page. Colours are CSS custom properties in three layers:

1. **Palette** (`--palette-*`): raw brand colours. Components never use these directly.
2. **Semantic** (`--color-*`): what a colour is for, e.g. `--color-text`, `--color-text-muted`, `--color-action`, `--color-border-control`. Each theme is one block that sets all of them.
3. **Media** (`--color-on-media`, `--media-scrim`, …): text over the walk-in video. Same in every theme.

How a theme is picked (no JavaScript needed to render):

| `<html>` class | Result |
|---|---|
| none | follows the device's light/dark setting |
| `theme-light` / `theme-dark` | forced; set by the header toggle and remembered |

**Adding a theme:** in `assets/theme.css`, copy the `.theme-dark` block, rename it `.theme-<name>`, change the values, then run

```
python3 tools/sync_theme.py      # copies theme.css into index.html (inlined there for a fast first paint)
python3 tools/check-contrast.py
```

It checks every text/background pairing (WCAG AA 4.5:1) and every control border and focus ring (3:1) in every theme, and fails if the OS-dark block has drifted from `.theme-dark` or `index.html` has an out-of-date copy. The `theme-` class prefix is reserved for themes.

## Table QR code

Ready to print, in `print/`:

| File | Use |
|---|---|
| `sonbol-table-card-A6.pdf` | one card, 105 × 148 mm, for a print shop |
| `sonbol-table-cards-A4.pdf` | four cards on one A4 sheet with dashed cut lines, for a home/office printer |
| `sonbol-qr.svg` / `sonbol-qr.png` | the QR code alone, for menus, stickers or Instagram |

Print at **100% / actual size** (not "fit to page") so the code stays 64 mm wide. Keep the white margin around the code; scanners need it.

The code opens `https://habchydavid.github.io/sonbol-cafe/`. It uses error-correction level Q, so it still scans with roughly a quarter of it scratched or stained. If the site moves to its own domain, regenerate and reprint:

```
pip install segno
python3 tools/make_qr.py https://new-domain.example/
```

then open `print/table-card.html` (or `print/table-card.html?sheet=a4`) in a browser and print to PDF with no margins.
