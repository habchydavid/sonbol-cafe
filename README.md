# Sonbol Cafe

Website for Sonbol Cafe, Deir El Ahmar (Bekaa, Lebanon): **https://sonbol.cafe/**

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

In `print/`. **Don't print them until https://sonbol.cafe/ opens on a phone with the padlock** (domain verified, DNS set, custom domain saved, HTTPS on); before that the code leads nowhere. The previous cards for the github.io address are in commit `514f394` (`git show 514f394:print/sonbol-table-card-A6.pdf > old.pdf`).

| File | Use |
|---|---|
| `sonbol-table-card-A6.pdf` | one card, 105 × 148 mm, for a print shop |
| `sonbol-table-cards-A4.pdf` | four cards on one A4 sheet with dashed cut lines, for a home/office printer |
| `sonbol-qr.svg` / `sonbol-qr.png` | the QR code alone, for menus, stickers or Instagram |

Print at **100% / actual size** (not "fit to page"). Check with a ruler: the black square of the code should measure about **50 mm** (64 mm including its white margin). Keep the white margin around the code; scanners need it.

The code opens `https://sonbol.cafe/`. It uses the highest error-correction level (H), so it still scans with about 30% of it scratched or stained, as long as the three big corner squares are visible. If the address ever changes, regenerate and reprint:

```
python3 -m venv /tmp/qrenv && /tmp/qrenv/bin/pip install segno
/tmp/qrenv/bin/python tools/make_qr.py https://new-address.example/
```

This rewrites `print/sonbol-qr.svg` and `.png` only. Then rebuild the two PDFs: open `print/table-card.html` and `print/table-card.html?sheet=a4` in a browser, print each to PDF with no margins and background graphics on, and save them over `print/sonbol-table-card-A6.pdf` and `print/sonbol-table-cards-A4.pdf`. Old printed cards keep pointing at the old address.

## Domain

`sonbol.cafe` is registered at Porkbun and served by GitHub Pages. Set it up in this order (verifying first stops anyone else claiming the domain while DNS points at GitHub; saving the custom domain last keeps the github.io address working until the new one resolves):

1. **Verify on GitHub:** profile picture → Settings → Pages → Add a domain → `sonbol.cafe`. Add the TXT record it shows at Porkbun (Host `_github-pages-challenge-habchydavid`), click Verify. Keep that TXT record forever; deleting it un-verifies the domain.
2. **Porkbun DNS:** delete Porkbun's default parking records (ALIAS on the bare domain and CNAME on `*`, both pointing to `pixie.porkbun.com`; leave email MX/TXT records), then add the records below. If Porkbun says "a CNAME or ALIAS record with that host already exists", a default record is still there.
3. **Wait** until https://dnschecker.org/#A/sonbol.cafe shows the 185.199.x.153 addresses.
4. **Repo Settings → Pages → Custom domain** → `sonbol.cafe` → Save. GitHub commits a `CNAME` file to `main`: `git pull` before the next push, never force-push, never delete `CNAME`.
5. **Enforce HTTPS** once it can be ticked (up to 24 h). If it still says "Certificate not yet created" after an hour, click Remove next to the domain, type it again and Save.

DNS at Porkbun:

| Type | Host | Answer |
|---|---|---|
| A | *(blank)* | 185.199.108.153 |
| A | *(blank)* | 185.199.109.153 |
| A | *(blank)* | 185.199.110.153 |
| A | *(blank)* | 185.199.111.153 |
| AAAA | *(blank)* | 2606:50c0:8000::153 |
| AAAA | *(blank)* | 2606:50c0:8001::153 |
| AAAA | *(blank)* | 2606:50c0:8002::153 |
| AAAA | *(blank)* | 2606:50c0:8003::153 |
| CNAME | www | habchydavid.github.io |
| TXT | *(GitHub's verification record)* | *(from GitHub account Settings → Pages)* |

No wildcard (`*`) record (Porkbun creates one by default; delete it): GitHub warns it allows domain takeover. Keep auto-renew on at Porkbun; if the domain lapses, every printed QR code stops working.
