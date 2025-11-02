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


def prompt_for_skin_type(skin_types: list, has_unknown: bool = False) -> str:
    """Ask the user to choose a skin type from the list
    and return a valid choice (preserving original casing)."""

    print("Available skin types:")
    for st in skin_types:
        print(f" - {st}")
    if has_unknown:
        print(" - Unknown")

    lookup = {st.lower(): st for st in skin_types}
    if has_unknown:
        lookup["unknown"] = "Unknown"

    while True:
        choice_raw = input("\nEnter a skin_type from the list above: ").strip().lower()
        if choice_raw in lookup:
            return lookup[choice_raw]  # Return with proper casing
        print("Not in the list. Please enter exactly one of the shown values.")


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

        skin_type_lower = skin_type_str.lower()
        if skin_type_lower not in seen_lowercase:
            seen_lowercase.add(skin_type_lower)
            skin_types.append(skin_type_str)  # keep the first original version

    return skin_types


def filter_by_skin_type(data, chosen_skin: str) -> list:
    """
    Return only animals whose skin_type matches the chosen one (case-insensitive).
    """

    filtered_animals = []
    chosen_skin_lower = chosen_skin.strip().lower()

    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        # Skip missing or empty
        if not skin_type:
            continue

        # Compare case-insensitively
        if str(skin_type).strip().lower() == chosen_skin_lower:
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


def select_animals_by_choice(data, chosen_label: str, unknown_animals: list) -> list:
    """
    Return the list of animals based on the chosen skin type label.
    If 'Unknown' is chosen, return animals with missing/empty skin_type.
    """
    if chosen_label == "Unknown":
        return unknown_animals
    return filter_by_skin_type(data, chosen_label)


def create_new_html(cards_html: str) -> None:
    """Replaces the placeholder in the template with generated HTML and saves output."""

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as template:
        tpl = template.read()

    html_out = tpl.replace(PLACEHOLDER, cards_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as new:
        new.write(html_out)


def main():
    data = load_data(DATA_FILE)
    skin_types = collect_skin_types(data)
    unknown_animals = collect_unknown_skin_type(data)

    if not skin_types and not unknown_animals:
        print("No skin types found in data.")
        return

    chosen_label = prompt_for_skin_type(skin_types, has_unknown=bool(unknown_animals))

    filtered = select_animals_by_choice(data, chosen_label, unknown_animals)
    if not filtered:
        print(f"No animals found with skin_type = '{chosen_label}'.")
        return

    cards_html = "".join(serialize_animal(a) for a in filtered)
    create_new_html(cards_html)
    print(f"\nFound {len(filtered)} animals matching the selected criteria.")
    print(f"Generated {OUTPUT_FILE} with skin_type = '{chosen_label}'.")


if __name__ == "__main__":
    main()