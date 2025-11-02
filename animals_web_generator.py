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


def get_animal_info() -> str:
    """Builds the HTML string for all animals."""
    animals_data = load_data(DATA_FILE)
    cards = [serialize_animal(a) for a in animals_data]
    return "".join(cards)


def create_new_html() -> None:
    """Replaces the placeholder in the template with generated HTML and saves output."""

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as template:
        tpl = template.read()

    html_out = tpl.replace(PLACEHOLDER, get_animal_info())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as new:
        new.write(html_out)


if __name__ == "__main__":
    create_new_html()