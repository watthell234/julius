# juliusgonzalez — personal site

A story-driven, single-page personal site. One self-contained `index.html` (inline CSS and JS, Google Fonts), no build step.

Design: Edward Tufte's *The Visual Display of Quantitative Information* blended with Tudor printing. A single reading column with margin sidenotes, a Mercator chart of the journey (Hispaniola → New York, with a New York State inset), a to-scale career timeline and a booktabs table. Tudor touches: blackletter initials, IM Fell small caps, a half-timbered band and a Tudor rose between parts. Light and dark themes follow the visitor's device.

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy (pick one, all free)
- **GitHub Pages:** Settings → Pages → deploy from branch `main`, folder `/`.
- **Vercel / Netlify:** import the repo; framework = "Other", no build command, output dir = `.`

## Rebuilding the map
`index.html` is generated from `tools/template.html`. The map paths come from Natural Earth via the npm packages `world-atlas@2.0.2` and `us-atlas@3.0.1`:
```bash
mkdir -p work/geo && cd work/geo
curl -sO https://registry.npmjs.org/world-atlas/-/world-atlas-2.0.2.tgz && mkdir wa && tar -xzf world-atlas-2.0.2.tgz -C wa
curl -sO https://registry.npmjs.org/us-atlas/-/us-atlas-3.0.1.tgz && mkdir us && tar -xzf us-atlas-3.0.1.tgz -C us
cd ../.. && cp tools/template.html work/tools/ 2>/dev/null || (mkdir -p work/tools && cp tools/template.html work/tools/)
python3 tools/geo.py work/geo work/geo/map.json && python3 tools/build.py work index.html
```

## Editing the story
Edit `tools/template.html` and rebuild (or edit `index.html` directly for quick text changes). Each part is a `<section class="part col">`; sidenotes are `<span class="sidenote">` inside a paragraph. All colors and fonts are tokens at the top of the `<style>` block.
