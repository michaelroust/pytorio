# The pytorio_playground "main"

import argparse

import pprint, json
import easy_io
from pytorio import calculator, encoding, generator

pp = pprint.PrettyPrinter(indent=4)


# MAYBE move this to easy_io
def save_dict(ddict):
    import json, easy_io
    json_str = json.dumps(ddict, sort_keys=True, indent=4)
    easy_io.write_file(json_str, 'src/pytorio/resources/misc/' + 'dict.json')


def decode_blueprint_file(filename_in, filename_out):
    exg_str = easy_io.read_file(filename_in)
    json_str = encoding.exg_str_to_json_str(exg_str)
    json_str = encoding.beatify_json(json_str)
    easy_io.write_file(json_str, filename_out)


def encode_blueprint_file(filename_in, filename_out):
    pass


def decode_example_file():
    folder = 'src/pytorio/resources/example_blueprints/'
    filename_in = folder + 'bp.txt'
    filename_out = folder + 'bp.json'

    decode_blueprint_file(filename_in, filename_out)


# decode_example_file()

#================================================


def generate_factory(rate=1, item_name='processing-unit'):
    output_folder = 'src/pytorio/resources/misc/'

    # Use these shared_items instead for on-site smelting.
    # shared_items = [
    #     'iron-ore', 'copper-ore', 'petroleum-gas', 'water', 'light-oil', 'lubricant', 'solid-fuel', 'sulfuric-acid',
    #     'plastic-bar'
    # ]
    shared_items = [
        'iron-plate', 'copper-plate', 'petroleum-gas', 'water', 'light-oil', 'lubricant', 'solid-fuel', 'sulfuric-acid',
        'plastic-bar', 'battery', 'steel-plate', 'electronic-circuit',
    ]
    prefered_recipes = {}
    prefered_machines = ['assembling-machine-3', 'electric-furnace']

    prod_tree = calculator.build_production_tree(rate, 'item', item_name, shared_items, prefered_recipes,
                                                 prefered_machines)
    easy_io.write_file(json.dumps(prod_tree, sort_keys=True, indent=4), output_folder + 'prod_dict.json')

    pp.pprint(calculator.list_production_tree_inputs(prod_tree))

    prod_list = calculator.flatten_production_tree(prod_tree)
    easy_io.write_file(json.dumps(prod_list, sort_keys=True, indent=4), output_folder + 'prod_list.json')

    bp_dict = generator.generate(prod_list)
    bp_json = encoding.dict_to_json_str(bp_dict)
    bp_str = encoding.json_str_to_exg_str(bp_json)

    easy_io.write_file(encoding.beatify_json(bp_json), output_folder + 'output.json')
    easy_io.write_file(bp_str, output_folder + 'output.txt')


# generate_factory()

#================================================


def generate_factory_beacons(rate, item_name):
    output_folder = 'src/pytorio/resources/misc/'

    shared_items = [
        'iron-plate', 'copper-plate', 'petroleum-gas', 'water', 'light-oil', 'lubricant', 'solid-fuel', 'sulfuric-acid',
        'plastic-bar', 'battery', 'steel-plate', 'electronic-circuit'
    ]
    prefered_recipes = {}
    prefered_machines = ['assembling-machine-3', 'electric-furnace']

    prod_tree = calculator.build_production_tree(rate, 'item', item_name, shared_items, prefered_recipes,
                                                 prefered_machines, calculator.module_selector_vanilla_max)
    easy_io.write_file(json.dumps(prod_tree, sort_keys=True, indent=4), output_folder + 'prod_dict.json')

    pp.pprint(calculator.list_production_tree_inputs(prod_tree))

    prod_list = calculator.flatten_production_tree(prod_tree)
    easy_io.write_file(json.dumps(prod_list, sort_keys=True, indent=4), output_folder + 'prod_list.json')

    bp_dict = generator.generate_with_beacons(prod_list)
    bp_json = encoding.dict_to_json_str(bp_dict)
    bp_str = encoding.json_str_to_exg_str(bp_json)

    easy_io.write_file(encoding.beatify_json(bp_json), output_folder + 'output.json')
    easy_io.write_file(bp_str, output_folder + 'output.txt')


# "automation-science-pack",
# "logistic-science-pack",
# "military-science-pack",
# "chemical-science-pack",
# "production-science-pack",
# "utility-science-pack",
# "space-science-pack",


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="A simple example script.")
    parser.add_argument("rate", type=int, help="Production rate (per second)", default=1)
    parser.add_argument("item_name", help="Item to produce.")
    parser.add_argument("-b", action="store_true", help="Generate a beaconed blueprint or not.")

    # Parse arguments
    args = parser.parse_args()

    if not args.b:
        generate_factory(args.rate, args.item_name)
    else:
        generate_factory_beacons(args.rate, args.item_name)

    print()
    print("========== Output ==========")
    print()

    import os
    os.system('cat src/pytorio/resources/misc/output.txt | pbcopy')
    os.system('cat src/pytorio/resources/misc/output.txt')
