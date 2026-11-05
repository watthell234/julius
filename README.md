# juliusgonzalez — personal site

A story-driven, single-page personal site. One self-contained `index.html` (inline CSS and JS, Google Fonts), no build step.

Design: a journey line runs down the page from the DR coordinates in the hero to New York and today. Palette is Atlantic navy, Caribbean sea teal and flamboyán red-orange; type is Bricolage Grotesque, Source Serif 4 and JetBrains Mono. Light and dark themes follow the visitor's device.

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy (pick one, all free)
- **GitHub Pages:** Settings → Pages → deploy from branch `main`, folder `/`.
- **Vercel / Netlify:** import the repo; framework = "Other", no build command, output dir = `.`

## Editing the story
Each stop on the journey is an `<article class="stop">` in `index.html`. Copy one to add a chapter. All colors and fonts are tokens at the top of the `<style>` block.
