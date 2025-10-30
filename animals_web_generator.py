import json


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


def get_animal_info():
    """Reads the content of animals_data.json, iterates through the animals, and for each one prints:
    - Name
    - Diet
    - The first location from the locations list
    - Type
    If one of these fields doesn’t exist, don’t print it.
    """

    animals_data = load_data('animals_data.json')
    for animal in animals_data:
        name = animal.get("name")
        locations = animal.get("locations", [])
        characteristics = animal.get("characteristics", {})
        diet = characteristics.get("diet")
        animal_type = characteristics.get("type")

        if name: print(f"Name: {name}")
        if diet: print(f"Diet: {diet}")
        if locations: print(f"Location: {locations[0]}")
        if animal_type: print(f"Type: {animal_type}")
        print()
