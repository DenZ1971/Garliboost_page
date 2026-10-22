#!/usr/bin/env python3
"""Generate published GARLIBOOST locale pages as plain static files."""

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent
PLACEHOLDER = re.compile(
    r"\{\{(t\.[a-z0-9_]+|locale_code|seo_links|social_meta|language_switcher)\}\}"
)
SAFE_LOCALE = re.compile(r"^[a-z]{2}$")
SAFE_OG_LOCALE = re.compile(r"^[a-z]{2}_[A-Z]{2}$")
SUBTITLE_STEMS = ("mastitis-01", "mastitis-02", "calves-01")


def read_json(path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def generate(source_dir=HERE, output_dir=None):
    source_dir = Path(source_dir).resolve()
    output_dir = Path(output_dir).resolve() if output_dir else source_dir.parent / "site"
    manifest = read_json(source_dir / "manifest" / "publication.json")
    published = manifest["published_locales"]
    routes = manifest["routes"]
    domain = manifest.get("domain")
    default_locale = manifest.get("default_locale")
    og_locales = manifest.get("og_locales")
    social_image = manifest.get("social_image")

    if not isinstance(published, list) or not published or len(set(published)) != len(published):
        raise ValueError("published_locales must be a nonempty list without duplicates")
    if any(not SAFE_LOCALE.fullmatch(locale) or locale not in routes for locale in published):
        raise ValueError("Each published locale needs a valid language code and route")
    if len({routes[locale] for locale in published}) != len(published):
        raise ValueError("Published routes must be unique")
    if any(not SAFE_LOCALE.fullmatch(routes[locale]) for locale in published):
        raise ValueError("Routes must be simple two-letter directories")
    if default_locale not in published:
        raise ValueError("default_locale must be one of published_locales")
    if domain is not None:
        parsed = urlparse(domain)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/"):
            raise ValueError("domain must be an HTTPS origin without a path")
        if not isinstance(og_locales, dict) or any(
            locale not in og_locales or not SAFE_OG_LOCALE.fullmatch(og_locales[locale])
            for locale in published
        ):
            raise ValueError("Each published locale needs a valid og_locales entry")
        if (
            not isinstance(social_image, str)
            or not social_image.startswith("/assets/")
            or ".." in Path(social_image).parts
            or not (source_dir / social_image.lstrip("/")).is_file()
        ):
            raise ValueError("social_image must reference an existing /assets/ file")

    template = (source_dir / "template" / "page.html").read_text(encoding="utf-8")
    privacy_template = (source_dir / "template" / "privacy.html").read_text(encoding="utf-8")
    needed = {
        match[2:]
        for source_template in (template, privacy_template)
        for match in PLACEHOLDER.findall(source_template)
        if match.startswith("t.")
    }
    pages = {}
    privacy_pages = {}
    locale_content = {}
    for locale in published:
        content_path = source_dir / "locales" / f"{locale}.json"
        if not content_path.is_file():
            raise ValueError(f"Missing approved locale file: {content_path}")
        content = read_json(content_path)
        missing = sorted(needed - content.keys())
        if missing:
            raise ValueError(f"{locale}: missing required locale keys: {', '.join(missing)}")
        if not all(isinstance(content[key], str) and content[key].strip() for key in needed):
            raise ValueError(f"{locale}: all required locale values must be nonempty strings")
        locale_content[locale] = content

        for stem in SUBTITLE_STEMS:
            subtitle_path = source_dir / "assets" / "subtitles" / f"{stem}-{locale}.vtt"
            if not subtitle_path.is_file():
                raise ValueError(f"{locale}: missing subtitle file: {subtitle_path}")
            subtitle = subtitle_path.read_text(encoding="utf-8-sig")
            if not subtitle.startswith("WEBVTT") or "-->" not in subtitle:
                raise ValueError(f"{locale}: invalid WebVTT subtitle file: {subtitle_path}")

        seo = ""
        social_meta = ""
        if domain:
            origin = domain.rstrip("/")
            url = f"{origin}/{routes[locale]}/"
            seo_lines = [f'<link rel="canonical" href="{html.escape(url, quote=True)}">']
            for alternate in published:
                alternate_url = f"{origin}/{routes[alternate]}/"
                seo_lines.append(
                    f'<link rel="alternate" hreflang="{alternate}" '
                    f'href="{html.escape(alternate_url, quote=True)}">'
                )
            default_url = f"{origin}/{routes[default_locale]}/"
            seo_lines.append(
                f'<link rel="alternate" hreflang="x-default" '
                f'href="{html.escape(default_url, quote=True)}">'
            )
            seo = "\n".join(seo_lines)

            image_url = origin + social_image
            social_lines = [
                '<meta property="og:type" content="website">',
                '<meta property="og:site_name" content="GARLIBOOST">',
                f'<meta property="og:title" content="{html.escape(content["head_text_001"], quote=True)}">',
                f'<meta property="og:description" content="{html.escape(content["meta_description_001"], quote=True)}">',
                f'<meta property="og:url" content="{html.escape(url, quote=True)}">',
                f'<meta property="og:image" content="{html.escape(image_url, quote=True)}">',
                f'<meta property="og:image:alt" content="{html.escape(content["meta_image_alt_001"], quote=True)}">',
                f'<meta property="og:locale" content="{og_locales[locale]}">',
            ]
            for alternate in published:
                if alternate != locale:
                    social_lines.append(
                        f'<meta property="og:locale:alternate" content="{og_locales[alternate]}">'
                    )
            social_lines.extend(
                [
                    '<meta name="twitter:card" content="summary_large_image">',
                    f'<meta name="twitter:title" content="{html.escape(content["head_text_001"], quote=True)}">',
                    f'<meta name="twitter:description" content="{html.escape(content["meta_description_001"], quote=True)}">',
                    f'<meta name="twitter:image" content="{html.escape(image_url, quote=True)}">',
                    f'<meta name="twitter:image:alt" content="{html.escape(content["meta_image_alt_001"], quote=True)}">',
                ]
            )
            structured_data = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Organization",
                        "@id": f"{origin}/#organization",
                        "name": content["footer_text_005"],
                        "url": f"{origin}/",
                        "address": {
                            "@type": "PostalAddress",
                            "streetAddress": content["footer_text_006"],
                            "addressLocality": "Bratislava",
                            "addressCountry": "SK",
                        },
                    },
                    {
                        "@type": "WebSite",
                        "@id": f"{origin}/#website",
                        "url": f"{origin}/",
                        "name": "GARLIBOOST",
                        "publisher": {"@id": f"{origin}/#organization"},
                        "inLanguage": published,
                    },
                    {
                        "@type": "WebPage",
                        "@id": f"{url}#webpage",
                        "url": url,
                        "name": content["head_text_001"],
                        "description": content["meta_description_001"],
                        "inLanguage": locale,
                        "isPartOf": {"@id": f"{origin}/#website"},
                        "about": {"@id": f"{origin}/#organization"},
                        "primaryImageOfPage": {
                            "@type": "ImageObject",
                            "url": image_url,
                            "caption": content["meta_image_alt_001"],
                        },
                    },
                ],
            }
            structured_json = json.dumps(
                structured_data, ensure_ascii=False, separators=(",", ":")
            ).replace("</", "<\\/")
            social_lines.append(
                f'<script type="application/ld+json">{structured_json}</script>'
            )
            social_meta = "\n".join(social_lines)

        language_options = []
        for alternate in published:
            label = alternate.upper()
            if alternate == locale:
                language_options.append(
                    f'<span lang="{alternate}" aria-current="page">{label}</span>'
                )
            else:
                language_options.append(
                    f'<a href="../{routes[alternate]}/" lang="{alternate}" '
                    f'hreflang="{alternate}">{label}</a>'
                )
        language_menu_id = f"language-options-{locale}"
        language_switcher = (
            f'<div class="language-menu" data-language-menu>'
            f'<button class="language-menu__toggle" type="button" '
            f'aria-expanded="false" aria-controls="{language_menu_id}" '
            f'aria-label="{html.escape(content["header_aria_label_002"], quote=True)}">'
            f'<span lang="{locale}">{locale.upper()}</span>'
            f'<span class="language-menu__chevron" aria-hidden="true"></span></button>'
            f'<div class="language-menu__list" id="{language_menu_id}" hidden>'
            f'{"".join(language_options)}</div></div>'
        )

        def render(source_template, page_seo, page_social_meta, page_language_switcher):
            def substitute(match):
                key = match.group(1)
                if key == "locale_code":
                    return html.escape(locale, quote=True)
                if key == "seo_links":
                    return page_seo
                if key == "social_meta":
                    return page_social_meta
                if key == "language_switcher":
                    return page_language_switcher
                # The templates only have text and quoted-attribute placeholders.
                return html.escape(content[key[2:]], quote=True)

            return PLACEHOLDER.sub(substitute, source_template)

        rendered = render(template, seo, social_meta, language_switcher)
        if PLACEHOLDER.search(rendered):
            raise ValueError(f"{locale}: unresolved placeholder")
        pages[routes[locale]] = rendered

        privacy_options = []
        for alternate in published:
            label = alternate.upper()
            if alternate == locale:
                privacy_options.append(
                    f'<span lang="{alternate}" aria-current="page">{label}</span>'
                )
            else:
                privacy_options.append(
                    f'<a href="../../{routes[alternate]}/privacy/" lang="{alternate}" '
                    f'hreflang="{alternate}">{label}</a>'
                )
        privacy_language_menu_id = f"privacy-language-options-{locale}"
        privacy_language_switcher = (
            f'<div class="language-menu" data-language-menu>'
            f'<button class="language-menu__toggle" type="button" '
            f'aria-expanded="false" aria-controls="{privacy_language_menu_id}" '
            f'aria-label="{html.escape(content["header_aria_label_002"], quote=True)}">'
            f'<span lang="{locale}">{locale.upper()}</span>'
            f'<span class="language-menu__chevron" aria-hidden="true"></span></button>'
            f'<div class="language-menu__list" id="{privacy_language_menu_id}" hidden>'
            f'{"".join(privacy_options)}</div></div>'
        )
        privacy_seo = ""
        if domain:
            origin = domain.rstrip("/")
            privacy_url = f"{origin}/{routes[locale]}/privacy/"
            privacy_lines = [
                f'<link rel="canonical" href="{html.escape(privacy_url, quote=True)}">'
            ]
            for alternate in published:
                alternate_url = f"{origin}/{routes[alternate]}/privacy/"
                privacy_lines.append(
                    f'<link rel="alternate" hreflang="{alternate}" '
                    f'href="{html.escape(alternate_url, quote=True)}">'
                )
            privacy_lines.append(
                f'<link rel="alternate" hreflang="x-default" '
                f'href="{origin}/{routes[default_locale]}/privacy/">'
            )
            privacy_seo = "\n".join(privacy_lines)
        privacy_rendered = render(
            privacy_template, privacy_seo, "", privacy_language_switcher
        )
        if PLACEHOLDER.search(privacy_rendered):
            raise ValueError(f"{locale} privacy: unresolved placeholder")
        privacy_pages[routes[locale]] = privacy_rendered

    # Validate every locale before writing output. Never emit unapproved pages.
    output_dir.mkdir(parents=True, exist_ok=True)
    for child in output_dir.iterdir():
        if child.is_dir() and child.name != "assets" and child.name not in pages:
            raise ValueError(f"Unpublished locale directory already in output: {child}")
    shutil.copytree(source_dir / "assets", output_dir / "assets", dirs_exist_ok=True)
    for route, rendered in pages.items():
        locale_dir = output_dir / route
        locale_dir.mkdir(exist_ok=True)
        (locale_dir / "index.html").write_text(rendered, encoding="utf-8")
        privacy_dir = locale_dir / "privacy"
        privacy_dir.mkdir(exist_ok=True)
        (privacy_dir / "index.html").write_text(
            privacy_pages[route], encoding="utf-8"
        )
    default_route = routes[default_locale]
    default_content = locale_content[default_locale]
    default_path = f"/{default_route}/"
    canonical = (
        f'<link rel="canonical" href="{html.escape(domain.rstrip("/") + default_path, quote=True)}">'
        if domain
        else ""
    )
    root_page = (
        f'<!doctype html><html lang="{default_locale}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(default_content["head_text_001"])}</title>'
        f'<meta name="robots" content="noindex,follow">{canonical}'
        f'<meta http-equiv="refresh" content="0; url={default_path}"></head>'
        f'<body><p><a href="{default_path}">{html.escape(default_content["head_text_001"])}</a></p>'
        f'</body></html>'
    )
    (output_dir / "index.html").write_text(root_page, encoding="utf-8")
    if domain:
        origin = domain.rstrip("/")
        alternate_urls = {
            locale: f"{origin}/{routes[locale]}/" for locale in published
        }
        alternate_urls["x-default"] = f"{origin}/{default_route}/"
        sitemap_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        ]
        for locale in published:
            sitemap_lines.append("  <url>")
            sitemap_lines.append(
                f"    <loc>{html.escape(alternate_urls[locale])}</loc>"
            )
            for hreflang, alternate_url in alternate_urls.items():
                sitemap_lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{hreflang}" '
                    f'href="{html.escape(alternate_url, quote=True)}" />'
                )
            sitemap_lines.append("  </url>")
        sitemap_lines.append("</urlset>")
        (output_dir / "sitemap.xml").write_text(
            "\n".join(sitemap_lines) + "\n", encoding="utf-8"
        )
        (output_dir / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n",
            encoding="utf-8",
        )
    return sorted(pages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=HERE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        print("Generated locales:", ", ".join(generate(args.source, args.output)))
    except (KeyError, ValueError, OSError) as error:
        parser.exit(1, f"Generation failed: {error}\n")
