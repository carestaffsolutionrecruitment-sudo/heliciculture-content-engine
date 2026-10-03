#!/usr/bin/env python3
"""Generate the Brilliant Directories article import files.

Reads the Markdown articles in content/articles/, maps each one to its
category in the taxonomy defined in generate_bd_categories.py, and writes two
files to the repository root:

- bd_article_import.csv: one row per post using BD's default post variables.
  Every record sits on one physical line, the file is pure ASCII (non-ASCII
  characters in the HTML body become numeric entities) and it contains no
  <script> tags. Posts are published by entering each row in the Add Post
  form (see PUBLISHING.md), because BD's Import Post File rejects any file
  containing a <table> tag and our articles use tables.
- bd_article_reference.csv: everything the post form does not take (live URL,
  SEO title and description, category path, JSON-LD), to be entered on each
  post after publishing.

Uses only the Python standard library.

Usage:
    python3 scripts/generate_bd_article_import.py
"""

import csv
import html
import json
import re
import sys
from pathlib import Path

from generate_bd_categories import TAXONOMY, slugify

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = ROOT / "content" / "articles"
OUTPUT = ROOT / "bd_article_import.csv"
REFERENCE_OUTPUT = ROOT / "bd_article_reference.csv"

SITE_URL = "https://snailworld.org"
# Observed on snailworld.org (not documented by BD): blog posts are served at
# /blog/<slugified title> with no trailing slash, and the post form has no
# slug field, so post URLs are derived from the title.
POST_URL_PREFIX = "/blog/"
AUTHOR = "Batuli Kassim"
# BD member that owns the posts: "Admin User - Blog Author" (member #5).
BD_USER_ID = "5"
# Observed on snailworld.org (not documented by BD): the post form rejects
# tags longer than 100 characters.
POST_TAGS_MAX = 100
META_TITLE_MAX = 60
META_DESCRIPTION_MAX = 160
CATEGORY_SEPARATOR = " > "

# Exact header row Brilliant Directories requires for blog imports (add
# post_image only when importing images).
IMPORT_COLUMNS = ["post_title", "post_content", "post_category", "post_tags", "user_id"]

REFERENCE_COLUMNS = [
    "post_title",
    "Post URL",
    "Category Tree",
    "Secondary Categories",
    "Author",
    "Meta Title",
    "Meta Description",
    "Target Region",
    "Schema JSON-LD",
    "Source File Path",
]

# Keyed by article slug.
ARTICLES = {
    "intensive-heliculture-pen-design": {
        "category": (
            "Commercial Producers & Aspiring Farmers",
            "Farm Operations & Business",
            "System Design and Pens",
        ),
        "secondary": [
            ("Commercial Producers & Aspiring Farmers", "Farm Operations & Business", "Feeding & Nutrition"),
            ("Commercial Producers & Aspiring Farmers", "Farm Operations & Business", "Biosecurity & Regulations"),
        ],
        "tags": [
            "heliculture", "snail farming", "Cornu aspersum", "Achatina", "pen design",
            "escape prevention", "snail feed formulae", "biosecurity", "UK", "Europe",
        ],
        "meta_title": "Intensive Snail Farming: Pen Design, Climate & Biosecurity",
    },
    "purging-and-kitchen-preparation-science": {
        "category": (
            "Commercial Producers & Aspiring Farmers",
            "Snail Science & Kitchen Prep",
            "Purging & Cleaning",
        ),
        "secondary": [
            ("Commercial Producers & Aspiring Farmers", "Snail Science & Kitchen Prep", "Dispatching & Safety"),
            ("Commercial Producers & Aspiring Farmers", "Snail Science & Kitchen Prep", "Meat Science & Texture"),
            ("Commercial Producers & Aspiring Farmers", "Snail Science & Kitchen Prep", "Mucin & Byproducts"),
        ],
        "tags": [
            "purging snails", "humane dispatch", "escargot preparation", "mucin removal",
            "enzymatic tenderising", "snail caviar", "snail mucin", "food safety", "allergens",
        ],
        "meta_title": "Snail Purging, Dispatch & Kitchen Preparation Science",
    },
    "regional-gastropod-culinary-heritage": {
        "category": (
            "Culinary Professionals & Food Enthusiasts",
            "Global Gastronomy & Recipes",
            "West Africa",
        ),
        "secondary": [
            ("Culinary Professionals & Food Enthusiasts", "Global Gastronomy & Recipes", "Europe & Mediterranean"),
        ],
        "tags": [
            "West Africa", "Europe & Mediterranean", "Nigeria", "Ghana", "Morocco", "Spain",
            "Sicily", "Crete", "peppered snail", "babbouche", "snail pepper soup",
            "caragols a la llauna", "alligator pepper", "wild thyme", "street food",
        ],
        "meta_title": "Peppered Snails to Babbouche: Regional Snail Cookery",
    },
}


# --- Markdown to HTML (covers the subset used by our articles) -------------

def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


def table_cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_to_html(markdown):
    lines = markdown.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
        elif m := re.match(r"(#{1,6})\s+(.*)", stripped):
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
        elif re.fullmatch(r"-{3,}", stripped):
            out.append("<hr>")
            i += 1
        elif stripped.startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>\n{markdown_to_html(chr(10).join(quoted))}\n</blockquote>")
        elif stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(table_cells(lines[i]))
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            parts = ["<table>", "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>", "<tbody>"]
            parts += ["<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body]
            parts += ["</tbody>", "</table>"]
            out.append("\n".join(parts))
        elif re.match(r"([-*]|\d+\.)\s+", stripped):
            ordered = bool(re.match(r"\d+\.", stripped))
            pattern = r"\d+\.\s+" if ordered else r"[-*]\s+"
            items = []
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(re.sub(pattern, "", lines[i].strip(), count=1))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>\n" + "\n".join(f"<li>{inline(it)}</li>" for it in items) + f"\n</{tag}>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,6}\s|>|\||[-*]\s|\d+\.\s|-{3,}$)", lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# --- Article parsing --------------------------------------------------------

def parse_article(path):
    text = path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---\n", 2)
    meta = dict(re.findall(r'^(\w+): "(.*)"$', frontmatter, re.M))
    schema = " ".join(
        '<script type="application/ld+json">' + json.dumps(json.loads(block), ensure_ascii=False) + "</script>"
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    )
    body = re.split(r"\n<!-- Structured data", body)[0]
    body = re.sub(r"^\s*# .*\n", "", body, count=1)  # BD renders the post title as the H1
    return meta, markdown_to_html(body.strip()), schema


def to_single_line_ascii(body_html):
    """Flatten HTML to one line and encode non-ASCII characters as entities.

    Block-level tags make the newlines between them insignificant, and the
    bodies contain no <pre> blocks, so joining lines does not change rendering.
    """
    one_line = "".join(line.strip() for line in body_html.splitlines())
    one_line = one_line.replace('"', "&quot;")
    return one_line.encode("ascii", "xmlcharrefreplace").decode("ascii")


def post_url(title):
    return f"{SITE_URL}{POST_URL_PREFIX}{slugify(title)}"


def join_tags(tags, limit=POST_TAGS_MAX):
    """Join tags in priority order, dropping whole tags that would exceed the limit."""
    kept = []
    for tag in tags:
        if len(", ".join(kept + [tag])) > limit:
            break
        kept.append(tag)
    return ", ".join(kept)


def write_csv(path, columns, rows, quote_header=True):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        if quote_header:
            writer.writerow(columns)
        else:
            f.write(",".join(columns) + "\r\n")
        writer.writerows(rows)


def category_index():
    index = {}
    for top, _, _, subs in TAXONOMY:
        index[(top,)] = slugify(top)
        for sub, _, _, leaves in subs:
            index[(top, sub)] = slugify(sub)
            for leaf, _, _ in leaves:
                index[(top, sub, leaf)] = slugify(leaf)
    return index


def build_rows():
    categories = category_index()
    errors, rows, reference_rows = [], [], []
    paths = sorted(ARTICLES_DIR.glob("*.md"))
    found = {p.stem for p in paths}
    for slug in ARTICLES.keys() - found:
        errors.append(f"{slug}: mapped but no Markdown file found")
    for path in paths:
        meta, body_html, schema = parse_article(path)
        slug = meta.get("slug", "")
        mapping = ARTICLES.get(slug)
        if mapping is None:
            errors.append(f"{path.name}: no category mapping for slug {slug!r}")
            continue
        for tree in [mapping["category"], *mapping["secondary"]]:
            if tree not in categories:
                errors.append(f"{slug}: category {CATEGORY_SEPARATOR.join(tree)!r} is not in the taxonomy")
        if len(mapping["meta_title"]) > META_TITLE_MAX:
            errors.append(f"{slug}: meta title exceeds {META_TITLE_MAX} chars")
        if len(meta["meta_description"]) > META_DESCRIPTION_MAX:
            errors.append(f"{slug}: meta description exceeds {META_DESCRIPTION_MAX} chars")
        if not schema:
            errors.append(f"{slug}: no JSON-LD schema found")
        url = post_url(meta["title"])
        if f'"{url}"' not in schema:
            errors.append(f"{slug}: JSON-LD does not reference the post URL {url}")
        for found_url in set(re.findall(rf"{re.escape(SITE_URL + POST_URL_PREFIX)}[^\"#]*", schema)):
            if found_url != url:
                errors.append(f"{slug}: JSON-LD uses {found_url}, expected {url}")
        import_row = [
            meta["title"],
            to_single_line_ascii(body_html),
            mapping["category"][-1],
            join_tags(mapping["tags"]),
            BD_USER_ID,
        ]
        for column, value in zip(IMPORT_COLUMNS, import_row):
            if not value.isascii() or re.search(r"[\r\n]", value) or "<script" in value.lower():
                errors.append(f"{slug}: {column} must be single-line ASCII without <script>")
        rows.append(import_row)
        reference_rows.append([
            meta["title"],
            url,
            CATEGORY_SEPARATOR.join(mapping["category"]),
            " | ".join(CATEGORY_SEPARATOR.join(t) for t in mapping["secondary"]),
            AUTHOR,
            mapping["meta_title"],
            meta["meta_description"],
            meta["target_region"],
            schema,
            path.relative_to(ROOT).as_posix(),
        ])
    return rows, reference_rows, errors


def main():
    rows, reference_rows, errors = build_rows()
    if errors:
        print("Article import validation failed:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    # The header goes out unquoted so it matches BD's required row byte for byte.
    write_csv(OUTPUT, IMPORT_COLUMNS, rows, quote_header=False)
    write_csv(REFERENCE_OUTPUT, REFERENCE_COLUMNS, reference_rows)
    print(f"Wrote {len(rows)} articles to {OUTPUT}")
    print(f"Wrote post metadata and schema to {REFERENCE_OUTPUT}")
    if not BD_USER_ID:
        print("Warning: BD_USER_ID is not set, so user_id is blank in every row.", file=sys.stderr)
    with_tables = [row[0] for row in rows if "<table" in row[1].lower()]
    if with_tables:
        print(
            f"Note: {len(with_tables)} of {len(rows)} posts contain tables, which BD's Import Post File "
            "rejects as 'Invalid file'. Publish them through the Add Post form (see PUBLISHING.md).",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
