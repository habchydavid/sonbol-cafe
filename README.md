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
