import json
import html
from typing import Any, Dict, List

DATA_FILE = "animals_data.json"
TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def load_data(file_path: str) -> Any:
    """Loads a JSON file."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def esc(value) -> str | None:
    """HTML-escape a value if it exists."""
    return html.escape(str(value)) if value is not None else None


def serialize_animal(animal: Dict[str, Any]) -> str:
    """Serialize a single animal into an HTML <li> block with inner list styling classes."""

    name = esc(animal.get("name"))
    locations: List[str] = animal.get("locations", []) or []
    ch: Dict[str, Any] = animal.get("characteristics", {}) or {}

    diet = esc(ch.get("diet"))
    animal_type = esc(ch.get("type"))
    main_prey = esc(ch.get("main_prey"))
    distinctive_feature = esc(
        ch.get("distinctive_feature") or ch.get("most_distinctive_feature")
    )
    habitat = esc(ch.get("habitat"))

    if not name:
        return ""  # skip if name missing

    parts: List[str] = []
    parts.append('<li class="cards__item">')
    parts.append(f'  <div class="card__title"><strong>{name}</strong></div>')
    parts.append('  <div class="card__text">')
    parts.append('    <ul class="animal-info">')

    if diet:
        parts.append(f'      <li class="animal-info__item"><strong>Diet:</strong> {diet}</li>')
    if main_prey:
        parts.append(f'      <li class="animal-info__item"><strong>Main prey:</strong> {main_prey}</li>')
    if locations:
        parts.append(f'      <li class="animal-info__item"><strong>Location:</strong> {esc(locations[0])}</li>')
    if habitat:
        parts.append(f'      <li class="animal-info__item"><strong>Habitat:</strong> {habitat}</li>')
    if animal_type:
        parts.append(f'      <li class="animal-info__item"><strong>Type:</strong> {animal_type}</li>')
    if distinctive_feature:
        parts.append(
            f'      <li class="animal-info__item"><strong>Distinctive feature:</strong> {distinctive_feature}</li>')

    parts.append('    </ul>')
    parts.append('  </div>')
    parts.append('</li>')
    return "\n".join(parts) + "\n"


def collect_skin_types(data) -> list:
    """
    Collect unique, non-empty skin_type values from JSON data.
    Keeps the first appearance order and original capitalization.
    """

    seen_lowercase = set()   # To track duplicates in lowercase
    skin_types = []

    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        if not skin_type:
            continue  # skip missing

        skin_type_str = str(skin_type).strip()
        if not skin_type_str:
            continue  # skip empty string

        lower_value = skin_type_str.lower()
        if lower_value not in seen_lowercase:
            seen_lowercase.add(lower_value)
            skin_types.append(skin_type_str)  # keep the first original version

    return skin_types


def filter_by_skin_type(data, chosen_skin: str) -> list:
    """
    Return only animals whose skin_type matches the chosen one (case-insensitive).
    """

    filtered_animals = []
    chosen_lower = chosen_skin.strip().lower()

    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        # Skip missing or empty
        if not skin_type:
            continue

        # Compare case-insensitively
        if str(skin_type).strip().lower() == chosen_lower:
            filtered_animals.append(animal)

    return filtered_animals


def collect_unknown_skin_type(data) -> list:
    """
    Return animals whose characteristics.skin_type is missing or empty.
    """

    unknown = []
    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        # Missing or empty/whitespace-only
        if not skin_type or not str(skin_type).strip():
            unknown.append(animal)

    return unknown


def build_cards_block() -> str:
    """Builds the HTML string for all animals."""
    animals_data = load_data(DATA_FILE)
    cards = [serialize_animal(a) for a in animals_data]
    return "".join(cards)


def create_new_html(cards_html) -> None:
    """Replaces the placeholder in the template with generated HTML and saves output."""

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as template:
        tpl = template.read()

    html_out = tpl.replace(PLACEHOLDER, cards_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as new:
        new.write(html_out)


def main():
    # 1) Load data
    data = load_data(DATA_FILE)

    # 2) Build the options
    skin_types = collect_skin_types(data)
    unknown_animals = collect_unknown_skin_type(data)

    if not skin_types and not unknown_animals:
        print("No skin types found in data.")
        return

    # 3) Show choices (include 'Unknown' only if there are any unknowns)
    print("Available skin types:")
    for st in skin_types:
        print(f" - {st}")
    if unknown_animals:
        print(" - Unknown")

    # Case-insensitive validation map: user input (lowercased) -> display label
    lookup = {st.lower(): st for st in skin_types}
    if unknown_animals:
        lookup["unknown"] = "Unknown"

    # 4) Prompt until valid
    while True:
        choice_raw = input("\nEnter a skin_type from the list above: ").strip().lower()
        if choice_raw in lookup:
            break
        print("Not in the list. Please enter exactly one of the shown values.")

    # 5) Filter by the choice
    if choice_raw == "unknown":
        chosen_label = "Unknown"
        filtered = unknown_animals
    else:
        chosen_label = lookup[choice_raw]  # preserve original casing (e.g., "Hair")
        filtered = filter_by_skin_type(data, chosen_label)

    # 6) If nothing matched (rare), bail out gracefully
    if not filtered:
        print(f"No animals found with skin_type = '{chosen_label}'.")
        return

    # 7) Build HTML and write
    cards_html = "".join(serialize_animal(a) for a in filtered)
    create_new_html(cards_html)
    print(f"Generated {OUTPUT_FILE} with skin_type = '{chosen_label}'.")


if __name__ == "__main__":
    main()