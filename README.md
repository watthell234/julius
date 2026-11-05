# juliusgonzalez — personal site

A story-driven, single-page personal site. Plain HTML/CSS/JS — no build step.

- `index.html` — the story (hero → 7 chapters → values → what's next → contact)
- `styles.css` — design (light/dark aware, responsive, reduced-motion friendly)
- `script.js` — scroll reveals, reading progress bar, count-up numbers

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy (pick one, all free)
- **GitHub Pages:** Settings → Pages → deploy from branch `main`, folder `/`.
- **Vercel / Netlify:** import the repo; framework = "Other", no build command, output dir = `.`

## Editing the story
Each chapter is a `<section class="chapter">` in `index.html`. Add a chapter by copying one and bumping the `chapter-num`.
