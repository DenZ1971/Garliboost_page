# GARLIBOOST static production foundation

`designs/concept-03.html` at commit `8e80f1807c445b27b33bfcf729313c3b392178cc` is the visual and content reference. Do not edit `designs/` as part of production generation.

Run `python3 production-src/generate.py` from the project root. The standard-library-only generator reads `template/page.html`, the locale JSON files named in `manifest/publication.json`, and the curated `assets/` directory. It writes plain static files to `site/`. The browser uses only HTML, CSS, vanilla JS, native MP4 and WebVTT.

`published_locales` is the publication allowlist; it currently contains `ru`, `en` and `sk`. Route entries for other languages are future routing definitions, not publication approval. The generator checks every text placeholder and each locale's required WebVTT files before it writes output. Locale values are ordinary text and are HTML-escaped, including inside quoted attributes. Intentional markup such as `<br>`, evidence links and section structure stays in the shared template; do not put HTML into locale JSON values.

The current master dictionary was extracted from the approved Russian page without editorial changes. Its keys identify the page area and the source text sequence; translators should use the corresponding template position and approved source wording, not infer meaning from a key alone. An approved translation must cover every required key before its locale is added to `published_locales`.

`domain` is the confirmed HTTPS production origin. The generator emits self-canonical URLs, reciprocal hreflang entries for all published locales, and an `x-default` entry using `default_locale`. It also writes a noindex root redirect to the default locale, `sitemap.xml`, `robots.txt`, localized Open Graph and Twitter metadata, and JSON-LD for the organization, website and locale page. `og_locales` and `social_image` are required while a production domain is configured.

The form submits to the external Formspree endpoint configured in the template. The generator emits a localized privacy notice at `/<locale>/privacy/` and links it from the form. Before publication, verify endpoint ownership and recipient, execute the required processor/SCC documentation, and configure deletion in Formspree to match the published retention period. The absent Ofir DOCX is omitted from the generated list; no substitute document is present.
