# GARLIBOOST static production foundation

`designs/concept-03.html` at commit `8e80f1807c445b27b33bfcf729313c3b392178cc` is the visual and content reference. Do not edit `designs/` as part of production generation.

Run `python3 production-src/generate.py` from the project root. The standard-library-only generator reads `template/page.html`, the locale JSON files named in `manifest/publication.json`, and the curated `assets/` directory. It writes plain static files to `site/`. The browser uses only HTML, CSS, vanilla JS, native MP4 and WebVTT.

`published_locales` is the publication allowlist. At Stage 1 it contains only `ru`; route entries for other languages are future routing definitions, not publication approval. The generator checks every text placeholder before it writes output and rejects missing or empty values. Locale values are ordinary text and are HTML-escaped, including inside quoted attributes. Intentional markup such as `<br>`, evidence links and section structure stays in the shared template; do not put HTML into locale JSON values.

The current master dictionary was extracted from the approved Russian page without editorial changes. Its keys identify the page area and the source text sequence; translators should use the corresponding template position and approved source wording, not infer meaning from a key alone. An approved translation must cover every required key before its locale is added to `published_locales`.

`domain` is currently `null`: no canonical or hreflang URLs are emitted. A confirmed HTTPS origin may be configured later. Hreflang entries are generated only for published locales; `x-default` is emitted only after `sk` is published. No root redirect, sitemap, robots file, form endpoint or other locale is part of Stage 1.

The RU form is intentionally unavailable until an external provider is chosen. The absent Ofir DOCX is omitted from the generated list; no substitute document is present.
