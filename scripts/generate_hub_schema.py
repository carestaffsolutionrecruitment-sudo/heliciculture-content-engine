#!/usr/bin/env python3
"""Add CollectionPage and BreadcrumbList JSON-LD to the regional hub guides.

Reads each Markdown file in content/regional-hubs/, takes the hub name, slug
and meta description from its frontmatter, and (re)writes a structured-data
block at the end of the file. Hub URLs use the clean /blog/<slug> path that
the category filter URLs 301-redirect to, so the schema points at the final
page rather than a redirect.

Usage:
    python3 scripts/generate_hub_schema.py
"""

import json
import re
import sys
from pathlib import Path

from generate_bd_categories import slugify

ROOT = Path(__file__).resolve().parent.parent
HUBS_DIR = ROOT / "content" / "regional-hubs"

SITE_URL = "https://snailworld.org"
BLOG_URL = f"{SITE_URL}/blog"
META_DESCRIPTION_MAX = 160
MARKER = "<!-- Structured data: CollectionPage and BreadcrumbList JSON-LD -->"


def hub_url(slug):
    return f"{BLOG_URL}/{slug}"


def schema_blocks(meta):
    url = hub_url(meta["slug"])
    collection = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{url}#collection",
        "url": url,
        "name": f"{meta['hub_name']} Snail Farming Hub",
        "headline": meta["title"],
        "description": meta["meta_description"],
        "inLanguage": "en-GB",
        "about": {"@type": "Place", "name": meta["hub_name"]},
        "isPartOf": {"@type": "WebSite", "@id": f"{SITE_URL}/#website", "name": "Snail World", "url": f"{SITE_URL}/"},
        "publisher": {"@type": "Organization", "@id": f"{SITE_URL}/#organization", "name": "Snail World", "url": f"{SITE_URL}/"},
        "breadcrumb": {"@id": f"{url}#breadcrumb"},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG_URL},
            {"@type": "ListItem", "position": 3, "name": meta["hub_name"], "item": url},
        ],
    }
    return [collection, breadcrumb]


def main():
    errors, done = [], 0
    for path in sorted(HUBS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = dict(re.findall(r'^(\w+): "(.*)"$', text.split("---")[1], re.M))
        for field in ("title", "meta_description", "slug", "hub_name"):
            if not meta.get(field):
                errors.append(f"{path.name}: missing frontmatter field {field!r}")
        if errors:
            continue
        if meta["slug"] != slugify(meta["hub_name"]):
            errors.append(f"{path.name}: slug {meta['slug']!r} should be {slugify(meta['hub_name'])!r}")
        if "&" in meta["hub_name"]:
            errors.append(f"{path.name}: hub name must use 'and', not '&'")
        if len(meta["meta_description"]) > META_DESCRIPTION_MAX:
            errors.append(f"{path.name}: meta description is {len(meta['meta_description'])} chars")
        body = text.split(MARKER)[0].rstrip()
        blocks = "\n".join(
            '<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + "\n</script>"
            for b in schema_blocks(meta)
        )
        path.write_text(f"{body}\n\n{MARKER}\n{blocks}\n", encoding="utf-8")
        done += 1
    if errors:
        print("Hub schema generation failed:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    print(f"Wrote schema for {done} regional hubs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
