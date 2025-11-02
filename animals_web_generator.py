import json


def load_data(file_path):
  """Loads a JSON file."""
  with open(file_path, "r") as handle:
    return json.load(handle)


def serialize_animal(animal):
    """Handles a single animal serialization."""

    name = animal.get("name")
    locations = animal.get("locations", [])
    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet")
    animal_type = characteristics.get("type")
    main_prey = characteristics.get("main_prey")
    distinctive_feature = characteristics.get("distinctive_feature")
    habitat = characteristics.get("habitat")

    output = ""
    output += '<li class="cards__item">\n'
    if name: output += f'<div class="card__title"><strong>{name}</strong></div>\n'
    output += '<div class="card__text">\n<ul>\n'
    if diet: output += f'<li><strong>Diet:</strong> {diet}</li>\n'
    if main_prey: output += f'<li><strong>Main prey:</strong> {main_prey}</li>\n'
    if locations: output += f'<li><strong>Location:</strong> {locations[0]}</li>\n'
    if habitat: output += f'<li><strong>Habitat:</strong> {habitat}</li>\n'
    if animal_type: output += f'<li><strong>Type:</strong> {animal_type}</li>\n'
    if distinctive_feature: output += f'<li><strong>Distinctive feature:</strong> {distinctive_feature}</li>\n'
    output += '</ul>\n</div>\n</li>\n'

    return output


def get_animal_info():
    """Reads the content of animals_data.json, iterates through the animals, and for each one returns name, diet,
    the first location from the locations list, type.
    If one of these fields doesn’t exist, don’t print it.
    """

    animals_data = load_data('animals_data.json')
    output = ""

    for animal in animals_data:
        output += serialize_animal(animal)
    return output


def create_new_html():
    with open("animals_template.html", "r") as template:
        animals = template.read()

        with open("animals.html", "w") as new:
            new.write(animals.replace("__REPLACE_ANIMALS_INFO__", get_animal_info()))


if __name__ == "__main__":
    create_new_html()
