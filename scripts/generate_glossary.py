#!/usr/bin/env python3
"""Generate the Snail World glossary page content with DefinedTerm JSON-LD.

Writes content/glossary/glossary.md: one section per term (title, anchor,
definition, contextual relevance, DefinedTerm JSON-LD) plus a DefinedTermSet
block for the whole page. Definitions are validated at 60-90 words and the
JSON-LD is built from the same text as the visible definitions.

Usage:
    python3 scripts/generate_glossary.py
"""

import json
import re
import sys
from pathlib import Path

from generate_bd_categories import slugify

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "content" / "glossary" / "glossary.md"

GLOSSARY_URL = "https://snailworld.org/glossary"
TERM_SET_ID = f"{GLOSSARY_URL}#defined-term-set"
DEFINITION_WORDS = (60, 90)

PILLARS = [
    "Heliculture and Infrastructure",
    "Veterinary, Pathology and Biosecurity",
    "Culinary and Gastronomy",
]

# (pillar index, term, definition, contextual relevance)
TERMS = [
    (
        0,
        "Aestivation",
        "A state of summer dormancy in which a land snail withdraws into its shell, seals the aperture "
        "with an epiphragm and sharply reduces its metabolic rate to survive heat and drought. In "
        "Cornu aspersum it is typically triggered above roughly 27 °C, particularly when relative "
        "humidity is low. Aestivating snails neither feed nor grow, so the response is a reliable "
        "signal that the production environment has moved outside the species' tolerance band. Also "
        "spelt estivation.",
        "Every day a batch spends aestivating is lost growth, so it lengthens the cycle to market weight and "
        "worsens feed conversion. Repeated heat and drought stress also raises mortality and lowers welfare.",
    ),
    (
        0,
        "Epiphragm",
        "A temporary membrane of dried mucus, often hardened with calcium carbonate, that a land snail "
        "secretes across its shell aperture to limit water loss during hibernation, aestivation or "
        "transport. Its thickness reflects the severity and expected length of dormancy: thin and "
        "parchment-like in brief dry spells, chalky and layered in winter. The snail dissolves or pushes "
        "it away when conditions improve, so its presence signals inactivity rather than death.",
        "In the kitchen, a sealed epiphragm after the conditioning chill shows that snails are dormant and "
        "ready for humane dispatch. On the farm, widespread sealing in a growing unit is an early warning "
        "of poor humidity.",
    ),
    (
        0,
        "Overwintering",
        "The management of snails through the cold season, either as natural hibernation in sheltered "
        "outdoor pens or as a controlled artificial winter indoors. In intensive Cornu aspersum "
        "production, breeders are commonly held for six to eight weeks at around 5–7 °C in high "
        "humidity, then returned to 18–20 °C under long-day lighting. This synchronises mating and egg "
        "laying, so producers can schedule hatching batches across the year instead of relying on spring.",
        "A planned artificial winter turns breeding from a seasonal event into a predictable programme, "
        "stabilising supply for buyers. Uncontrolled cold exposure, by contrast, causes frost mortality "
        "and weight loss in unprotected stock.",
    ),
    (
        0,
        "Stocking Density",
        "The number of snails kept per square metre of usable surface, including walls, boards and tray "
        "areas as well as floor space. Working ranges for Cornu aspersum are roughly 1,500–2,000 per m² "
        "for nursery hatchlings, 300–500 per m² for growers in outdoor pens and 100–150 per m² for "
        "breeders. Achatina need far less crowding. Overstocking slows growth through competition and a "
        "pheromone-mediated crowding effect carried in mucus and faeces.",
        "Density is the first lever to pull when growth stalls. Lower densities improve uniformity, reduce "
        "disease pressure and cut mortality, while excessive densities raise feed waste and the risk of "
        "bacterial outbreaks.",
    ),
    (
        0,
        "Substrate pH",
        "The acidity or alkalinity of the soil, loam or coir in which snails rest, feed and lay eggs. "
        "Edible land snails perform best on calcium-rich substrates close to neutral or slightly "
        "alkaline, roughly pH 7–8. Acidic substrates leach calcium, weaken shell formation and can "
        "depress egg viability, while waterlogged or fouled substrates drift in pH as organic matter "
        "decomposes. Producers should test substrate regularly and correct acidity with ground limestone.",
        "Correct pH supports strong shells, which reduces breakage in handling and transport, and protects "
        "hatch rates in breeding pots. Testing costs little compared with the losses from poor shell quality.",
    ),
    (
        1,
        "Pseudomonas aeruginosa",
        "A Gram-negative, opportunistic bacterium found in soil and water and associated with intestinal "
        "infection and high mortality in farmed land snails, particularly under wet, dirty and crowded "
        "conditions. Affected snails may become lethargic, stop feeding and die in clusters. Outbreaks "
        "are driven largely by husbandry: stagnant humidity, fermenting feed residues and poor "
        "ventilation. Control relies on hygiene, airflow and reduced stocking density rather than "
        "medication.",
        "Clustered deaths in a box or pen should trigger immediate isolation, cleaning and a review of "
        "humidity and feeding residues. Because the organism can also infect people, staff should wear "
        "gloves and wash their hands.",
    ),
    (
        1,
        "Riccardoella Mites",
        "Small white mites of the genus Riccardoella that live in the lung (mantle) cavity and on the "
        "body surface of land snails, feeding on mucus and blood. Heavy infestations, including "
        "Riccardoella oudemansi in Cornu aspersum, are linked to reduced growth, lower egg production "
        "and increased mortality. Mites spread readily between snails in crowded units and survive in "
        "untreated timber, so quarantine and clean substrates are central to control.",
        "Undetected mites erode growth and fertility across a whole unit. Inspecting incoming stock under "
        "magnification and avoiding untreated wood greatly reduce the risk of a persistent infestation.",
    ),
    (
        1,
        "Rat Lungworm (Angiostrongylus cantonensis)",
        "A parasitic nematode whose adult stage lives in rats and whose larvae develop in snails and "
        "slugs, which act as intermediate hosts. People can be infected by eating raw or undercooked "
        "molluscs, or produce contaminated by them, and infection can cause eosinophilic meningitis. "
        "Giant African land snails from endemic regions are a recognised host. Thorough cooking destroys "
        "the larvae, and captive-bred stock raised on controlled feed carries far lower risk.",
        "This is the main public-health reason never to serve snails raw or undercooked. Gloves and "
        "hand-washing protect staff handling raw Achatina, and documented captive-bred sourcing protects "
        "consumers.",
    ),
    (
        1,
        "Phasmarhabditis hermaphrodita",
        "A parasitic nematode that carries bacteria lethal to many slugs and some snails, sold "
        "commercially as a biological slug control applied to gardens and crops. Infective juveniles "
        "enter the mantle region, multiply and kill the host within days. Susceptibility varies between "
        "snail species and life stages, with juveniles generally more vulnerable, so the product poses a "
        "real risk to farmed stock if applied on or near production areas.",
        "Snail farms should not use the product on site and should agree buffer zones with neighbouring "
        "growers, because drift or contaminated soil and water can introduce the nematode into pens.",
    ),
    (
        1,
        "Quarantine Protocol",
        "A documented procedure for isolating newly acquired or returning snails before they join the "
        "main population. A typical heliculture protocol holds incoming stock in a separate room for "
        "four to six weeks, with dedicated equipment and clothing, daily mortality records and "
        "inspection for mites, abnormal mucus, shell damage and behavioural change. Stock is released "
        "only when it shows no signs of disease, and any losses are investigated before release.",
        "Quarantine is the cheapest insurance a farm can buy, because a single infected consignment can "
        "introduce mites or bacterial disease that persists for several production cycles.",
    ),
    (
        2,
        "Purging Fast",
        "The controlled withdrawal of feed before slaughter so that snails clear their digestive tract of "
        "plant material, soil and grit. Farmed snails raised on known feed typically need 48–72 hours of "
        "fasting in clean, humid, ventilated containers rinsed daily. Wild-gathered snails usually need "
        "longer, often with a preliminary cleansing diet of bran or flour, because their diet may include "
        "plants that are bitter or toxic to people.",
        "A correct purge removes gritty texture and earthy bitterness and reduces the microbial load "
        "entering the kitchen. Skipping or shortening it is one of the commonest causes of poor-quality "
        "escargot.",
    ),
    (
        2,
        "Blanching",
        "The brief immersion of snails in a large volume of water at a full, rolling boil, used both to "
        "dispatch chilled, dormant snails rapidly and to loosen the body from the shell for extraction. "
        "Professional practice adds snails in small batches so the water returns to the boil "
        "immediately, and cooks Cornu or Helix for roughly three to five minutes before rapid chilling "
        "in iced water. Larger Achatina need longer.",
        "Done correctly, blanching is the most humane practical kitchen dispatch method. It also begins "
        "pathogen reduction and makes extraction faster, improving yield and consistency.",
    ),
    (
        2,
        "Hepatopancreas Removal",
        "The excision of the snail's digestive gland, the dark, coiled visceral mass known in French "
        "kitchens as the tortillon, after blanching and extraction. The gland is rich in digestive "
        "enzymes and may concentrate contaminants, so it is removed at its junction with the muscular "
        "foot. In Great Britain and the EU, food hygiene law requires its removal where it may present a "
        "hazard, and it must not then be used for food.",
        "Removal is both a legal and a quality step: retained tissue speeds enzymatic autolysis, softening "
        "texture and producing off-flavours, and keeping it can breach hygiene requirements.",
    ),
    (
        2,
        "Thermal Pasteurisation",
        "A controlled mild heat treatment that destroys vegetative pathogens and spoilage organisms in "
        "prepared snail products, such as brined snail caviar or cooked snail meat in liquor, while "
        "preserving delicate texture and flavour. Unlike commercial sterilisation in canning, it does not "
        "make a product shelf-stable at room temperature, so pasteurised products still need chilled "
        "storage and a validated shelf life set with a qualified food technologist.",
        "Validated pasteurisation lets producers sell high-value secondary yields such as snail caviar "
        "safely and legally. Unvalidated time and temperature combinations create real food-safety risk "
        "and liability.",
    ),
    (
        2,
        "Escargot Butter",
        "A compound butter traditionally made from softened unsalted butter, finely chopped garlic, "
        "flat-leaf parsley and shallot, seasoned with salt and pepper and sometimes a little white wine "
        "or Pernod. It is the defining element of escargots à la bourguignonne: tender, pre-cooked snails "
        "are returned to cleaned shells or escargot dishes, sealed with the butter and baked until it "
        "foams. Its fat carries garlic aromatics and complements the snail's earthy flavour.",
        "A well-balanced butter lets producers and chefs present affordable farmed snails as a premium "
        "dish. Butter is a declarable milk allergen, alongside the molluscs themselves.",
    ),
]


def anchor(term):
    return slugify(re.sub(r"\(.*?\)", "", term))


def term_jsonld(term, definition):
    url = f"{GLOSSARY_URL}#{anchor(term)}"
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "@id": url,
        "name": term,
        "description": definition,
        "inDefinedTermSet": TERM_SET_ID,
        "url": url,
    }


def term_set_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "@id": TERM_SET_ID,
        "name": "Snail World Glossary of Heliculture, Snail Health and Gastronomy",
        "description": "Definitions of technical terms in commercial snail farming, snail health and "
        "biosecurity, and snail preparation and cookery.",
        "url": GLOSSARY_URL,
        "inLanguage": "en-GB",
        "publisher": {"@type": "Organization", "name": "Snail World", "url": "https://snailworld.org/"},
        "hasDefinedTerm": [{"@id": f"{GLOSSARY_URL}#{anchor(t)}"} for _, t, _, _ in TERMS],
    }


def script_block(data):
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def validate():
    errors = []
    anchors = [anchor(t) for _, t, _, _ in TERMS]
    for dup in {a for a in anchors if anchors.count(a) > 1}:
        errors.append(f"duplicate anchor #{dup}")
    low, high = DEFINITION_WORDS
    for _, term, definition, relevance in TERMS:
        words = len(definition.split())
        if not low <= words <= high:
            errors.append(f"{term}: definition is {words} words (need {low}-{high})")
        if not relevance.strip():
            errors.append(f"{term}: missing contextual relevance")
    return errors


def render():
    lines = [
        "---",
        'title: "Snail World Glossary: Heliculture, Snail Health and Gastronomy Terms"',
        'meta_description: "Clear definitions of key snail farming, snail health and snail cookery terms, '
        'from aestivation and stocking density to purging, blanching and escargot butter."',
        'slug: "glossary"',
        'category_pillar: "Glossary"',
        'target_region: "Global"',
        "---",
        "",
        "# Snail World Glossary",
        "",
        "Precise definitions of the technical vocabulary used across commercial heliculture, snail health "
        "and biosecurity, and snail preparation and cookery.",
    ]
    for pillar_index, pillar in enumerate(PILLARS):
        lines += ["", f"## {pillar}"]
        for p, term, definition, relevance in TERMS:
            if p != pillar_index:
                continue
            lines += [
                "",
                f'<h3 id="{anchor(term)}">{term}</h3>',
                "",
                f"**Anchor:** `#{anchor(term)}`",
                "",
                definition,
                "",
                f"**Why it matters:** {relevance}",
                "",
                script_block(term_jsonld(term, definition)),
            ]
    lines += ["", "<!-- Structured data: DefinedTermSet for the whole glossary page -->", script_block(term_set_jsonld()), ""]
    return "\n".join(lines)


def main():
    errors = validate()
    if errors:
        print("Glossary validation failed:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {len(TERMS)} terms to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
