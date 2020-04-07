
import json

# prototypes_folder = "src/pytorio/resources/0.18.17_recipe-lister/"
prototypes_folder = "src/pytorio/resources/0.18.17_krastorio2_recipe-lister/"

def load_prototype_file(input_path)->dict:
    with open(input_path) as fin:
        return json.loads(fin.read())

recipes_path = prototypes_folder + "recipe.json"
recipes = load_prototype_file(recipes_path)

inserters_path = prototypes_folder + "inserter.json"
inserters = load_prototype_file(inserters_path)

items_path = prototypes_folder + "item.json"
items = load_prototype_file(items_path)


assembling_machines_path = prototypes_folder + "assembling-machine.json"
furnaces_path = prototypes_folder + "furnace.json"
machines = load_prototype_file(assembling_machines_path)
machines.pop("crash-site-assembling-machine-1-repaired")
machines.pop("crash-site-assembling-machine-2-repaired")
machines.update(load_prototype_file(furnaces_path))




# DEBUG
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(machines)
