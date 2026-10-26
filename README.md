# GARLIBOOST Multilingual Website

A multilingual static product website for the GARLIBOOST agricultural feed supplement. The production site is generated from a shared HTML template and localized JSON content.

## Highlights

- Slovak, English and Russian locales
- Python standard-library site generator
- Semantic HTML, responsive CSS and vanilla JavaScript
- Localized SEO metadata, canonical URLs, hreflang, sitemap and robots.txt
- Accessible navigation, forms, tabs, video subtitles and keyboard interactions
- Automated browser checks for responsive behavior and core interactions

## Generate the site

```bash
python3 production-src/generate.py
```

Generated files are written to `site/`. Publication settings and approved locales are defined in `production-src/manifest/publication.json`.

## Project structure

- `production-src/` — templates, locale data, generator and curated assets
- `site/` — generated production output
- `scripts/` — automated interface checks
- `designs/` — design concepts and references
- `ux-ui-reference/` — accessibility and design-system documentation

Live site: [garliboost.com](https://garliboost.com/)
