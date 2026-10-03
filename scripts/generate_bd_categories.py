#!/usr/bin/env python3
"""Generate the Brilliant Directories category taxonomy CSV.

Writes bd_category_taxonomy.csv to the repository root: one row per category
node (top-level, child, sub-child), with deeper levels left blank so each row
maps cleanly onto Brilliant Directories' parent/child category import.

Usage:
    python3 scripts/generate_bd_categories.py
"""

import csv
import re
import sys
import unicodedata
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "bd_category_taxonomy.csv"

COLUMNS = [
    "Parent Category",
    "Child Category",
    "Sub-Child Category",
    "Category Level",
    "Sort Order",
    "Category URL Slug",
    "Meta Title",
    "Meta Description",
]

META_TITLE_MAX = 60
META_DESCRIPTION_MAX = 160

# (name, meta_title, meta_description, children)
TAXONOMY = [
    (
        "Commercial Producers and Aspiring Farmers",
        "Snail Farming for Commercial Producers & New Farmers",
        "Technical, regulatory and business guidance for commercial snail "
        "farmers and aspiring heliculture entrepreneurs in the UK and beyond.",
        [
            (
                "Farm Operations and Business",
                "Snail Farm Operations and Business Guides",
                "Run a profitable snail farm: pen design, feeding programmes, "
                "biosecurity, regulatory compliance and enterprise economics.",
                [
                    (
                        "System Design and Pens",
                        "Snail Farm System Design & Pen Layouts",
                        "Intensive and outdoor snail pen design, climate control, "
                        "escape prevention and housing for Cornu aspersum and Achatina.",
                    ),
                    (
                        "Feeding and Nutrition",
                        "Snail Feeding Formulae & Nutrition Guides",
                        "Commercial snail feed formulae, protein and calcium targets, "
                        "fresh forage and feeding practice for faster, healthier growth.",
                    ),
                    (
                        "Biosecurity and Regulations",
                        "Snail Farm Biosecurity and Regulations",
                        "Biosecurity programmes, food hygiene law, non-native species "
                        "rules and compliance checklists for commercial snail farms.",
                    ),
                    (
                        "Economics and Yields",
                        "Snail Farming Economics, Costs & Yields",
                        "Realistic snail farm start-up costs, production cycles, yields, "
                        "market prices and routes to market for heliculture businesses.",
                    ),
                ],
            ),
            (
                "Snail Science and Kitchen Prep",
                "Snail Science and Kitchen Preparation Guides",
                "The science of preparing snails: purging, humane dispatch, "
                "cleaning chemistry, meat texture and secondary yields.",
                [
                    (
                        "Purging and Cleaning",
                        "How to Purge & Clean Snails for Cooking",
                        "Purging timelines for farmed and wild snails, mucin removal "
                        "with salt, acid and alum, and professional cleaning methods.",
                    ),
                    (
                        "Dispatching and Safety",
                        "Humane Snail Dispatch & Food Safety",
                        "Humane dispatch methods, food hygiene, allergen controls and "
                        "safe handling of farmed snails, including Achatina species.",
                    ),
                    (
                        "Meat Science and Texture",
                        "Snail Meat Science and Texture Control",
                        "Control snail meat texture with court-bouillon, sous vide and "
                        "enzymatic tenderising. Cooking times by species and size.",
                    ),
                    (
                        "Mucin and Byproducts",
                        "Snail Mucin, Caviar & Byproduct Guides",
                        "Snail caviar production, cosmetic mucin collection, shell "
                        "processing and the regulations behind secondary yields.",
                    ),
                ],
            ),
        ],
    ),
    (
        "Culinary Professionals and Food Enthusiasts",
        "Snail Cookery for Chefs & Food Enthusiasts",
        "Escargot technique, heritage recipes and global snail traditions "
        "for chefs, home cooks and culinary explorers.",
        [
            (
                "Global Gastronomy and Recipes",
                "Global Snail Recipes & Culinary Traditions",
                "Regional snail recipes, history, flavour profiles and pairing "
                "guides from West Africa, Europe, Asia and the Americas.",
                [
                    (
                        "West Africa",
                        "West African Snail Recipes & Traditions",
                        "Peppered snail, snail pepper soup and Ghanaian snail kebabs: "
                        "giant African land snail cookery, spices and street food.",
                    ),
                    (
                        "Europe and Mediterranean",
                        "European & Mediterranean Snail Recipes",
                        "Escargots a la bourguignonne, caragols a la llauna, Moroccan "
                        "babbouche and Italian snail stews: Mediterranean classics.",
                    ),
                    (
                        "Asia and Southeast Asia",
                        "Asian & Southeast Asian Snail Recipes",
                        "Vietnamese bun oc, coconut snail stir-fries, luosifen and "
                        "Sichuan snail dishes from Asia's night markets and kitchens.",
                    ),
                    (
                        "Americas and USA",
                        "Snail Cuisine in the Americas and USA",
                        "Fine-dining escargot, fusion snail dishes, regional history "
                        "and US import rules for chefs across the Americas.",
                    ),
                ],
            ),
        ],
    ),
]


def slugify(name):
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def build_rows():
    rows = []
    for top_i, (top, top_title, top_desc, subs) in enumerate(TAXONOMY, 1):
        rows.append([top, "", "", 1, top_i, slugify(top), top_title, top_desc])
        for sub_i, (sub, sub_title, sub_desc, leaves) in enumerate(subs, 1):
            rows.append([top, sub, "", 2, sub_i, slugify(sub), sub_title, sub_desc])
            for leaf_i, (leaf, leaf_title, leaf_desc) in enumerate(leaves, 1):
                rows.append([top, sub, leaf, 3, leaf_i, slugify(leaf), leaf_title, leaf_desc])
    return rows


def validate(rows):
    errors = []
    slugs = [row[5] for row in rows]
    for dup in {s for s in slugs if slugs.count(s) > 1}:
        errors.append(f"duplicate slug: {dup}")
    for row in rows:
        label = row[2] or row[1] or row[0]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", row[5]):
            errors.append(f"{label}: invalid slug {row[5]!r}")
        if len(row[6]) > META_TITLE_MAX:
            errors.append(f"{label}: meta title is {len(row[6])} chars (max {META_TITLE_MAX})")
        if len(row[7]) > META_DESCRIPTION_MAX:
            errors.append(
                f"{label}: meta description is {len(row[7])} chars (max {META_DESCRIPTION_MAX})"
            )
        if not all(str(cell).isascii() for cell in row):
            errors.append(f"{label}: non-ASCII characters may break the import")
    return errors


def main():
    rows = build_rows()
    errors = validate(rows)
    if errors:
        print("Taxonomy validation failed:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(COLUMNS)
        writer.writerows(rows)
    print(f"Wrote {len(rows)} categories to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
