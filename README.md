# juliusgonzalez — personal site

A personal site told as a short storybook: a tooled-leather cover, then pages that turn on their spine. Two-page spreads on wide screens, one page at a time on phones. Turn with the arrows, the arrow keys, a click on either page, or a swipe. Pages are linkable as `#page-N`.

Inside, the pages follow Edward Tufte's *The Visual Display of Quantitative Information* (footnotes, a to-scale timeline, a booktabs table, a Mercator chart of the journey from Hispaniola to New York) and are set like a Tudor octavo: blackletter initials, IM Fell small caps, running heads, folios and catchwords.

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy (free)
- **GitHub Pages:** Settings → Pages → deploy from branch, folder `/`.
- **Vercel / Netlify:** import the repo; framework "Other", no build command, output dir `.`

## Editing
`index.html` is generated. Edit `tools/book.html` (one `<section class="page">` per page; keep an even page count so spreads pair up), then rebuild:
```bash
mkdir -p work/geo work/tools && cd work/geo
curl -sO https://registry.npmjs.org/world-atlas/-/world-atlas-2.0.2.tgz && mkdir -p wa && tar -xzf world-atlas-2.0.2.tgz -C wa
curl -sO https://registry.npmjs.org/us-atlas/-/us-atlas-3.0.1.tgz && mkdir -p us && tar -xzf us-atlas-3.0.1.tgz -C us
cd ../.. && cp tools/book.html tools/mapsvg.html work/tools/
python3 tools/geo.py work/geo work/geo/map.json && python3 tools/build_book.py work index.html
```
For a quick text fix you can also edit `index.html` directly.
