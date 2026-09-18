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
PLACEHOLDER = re.compile(r"\{\{(t\.[a-z0-9_]+|locale_code|seo_links)\}\}")
SAFE_LOCALE = re.compile(r"^[a-z]{2}$")


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

    if not isinstance(published, list) or not published or len(set(published)) != len(published):
        raise ValueError("published_locales must be a nonempty list without duplicates")
    if any(not SAFE_LOCALE.fullmatch(locale) or locale not in routes for locale in published):
        raise ValueError("Each published locale needs a valid language code and route")
    if len({routes[locale] for locale in published}) != len(published):
        raise ValueError("Published routes must be unique")
    if any(not SAFE_LOCALE.fullmatch(routes[locale]) for locale in published):
        raise ValueError("Routes must be simple two-letter directories")
    if domain is not None:
        parsed = urlparse(domain)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/"):
            raise ValueError("domain must be an HTTPS origin without a path")

    template = (source_dir / "template" / "page.html").read_text(encoding="utf-8")
    needed = {match[2:] for match in PLACEHOLDER.findall(template) if match.startswith("t.")}
    pages = {}
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

        seo = ""
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
            if "sk" in published:
                seo_lines.append(
                    f'<link rel="alternate" hreflang="x-default" '
                    f'href="{html.escape(origin + "/sk/", quote=True)}">'
                )
            seo = "\n".join(seo_lines)

        def substitute(match):
            key = match.group(1)
            if key == "locale_code":
                return html.escape(locale, quote=True)
            if key == "seo_links":
                return seo
            # The template only has text and quoted-attribute placeholders.
            return html.escape(content[key[2:]], quote=True)

        rendered = PLACEHOLDER.sub(substitute, template)
        if PLACEHOLDER.search(rendered):
            raise ValueError(f"{locale}: unresolved placeholder")
        pages[routes[locale]] = rendered

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
