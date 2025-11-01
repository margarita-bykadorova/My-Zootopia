import json


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


def get_animal_info():
    """Reads the content of animals_data.json, iterates through the animals, and for each one returns:
    - Name
    - Diet
    - The first location from the locations list
    - Type
    If one of these fields doesn’t exist, don’t print it.
    """

    animals_data = load_data('animals_data.json')
    output = ""

    for animal in animals_data:
        name = animal.get("name")
        locations = animal.get("locations", [])
        characteristics = animal.get("characteristics", {})
        diet = characteristics.get("diet")
        animal_type = characteristics.get("type")

        output += '<li class="cards__item">'
        if name: output += f'<div class="card__title">{name}</div>'
        output += '<p class="card__text">'
        if diet: output += f'<strong>Diet:</strong> {diet}<br/>\n'
        if locations: output += f'<strong>Location:</strong> {locations[0]}<br/>\n'
        if animal_type: output += f'<strong>Type:</strong> {animal_type}<br/>\n'
        output += '</p>'
        output += '</li>'

    return output


def create_new_html():
    with open("animals_template.html", "r") as template:
        animals = template.read()

        with open("animals.html", "w") as new:
            new.write(animals.replace("__REPLACE_ANIMALS_INFO__", get_animal_info()))


if __name__ == "__main__":
    create_new_html()
