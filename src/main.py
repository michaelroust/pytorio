# The pytorio_playground "main"

from pytorio.calculator import *
import pprint

pp = pprint.PrettyPrinter(indent=4)


# MAYBE move this to easy_io
def save_dict(ddict):
    import json, easy_io
    json_str = json.dumps(ddict, sort_keys=True, indent=4)
    easy_io.write_file(json_str, 'src/pytorio/resources/misc/' + 'dict.json')


# pp.pprint(recipes)
# pp.pprint(recipes[find_item_recipe('iron-plate')])

shared_items = ['iron-plate', 'copper-plate', 'crude-oil', 'water', 'sulfuric-acid', 'light-oil', 'heavy-oil']
prefered_recipes = {'petroleum-gas': 'advanced-oil-processing', 'solid-fuel': 'solid-fuel-from-light-oil'}

# recipe_tree = build_recipe_tree(5, 'iron-gear-wheel')
# recipe_tree = build_recipe_tree(5, 'iron-gear-wheel', 'item', shared_items=['iron-plate'])
# recipe_tree = build_recipe_tree(1, 'advanced-circuit', 'item', shared_items, prefered_recipes)
# recipe_tree = build_recipe_tree(0.1, 'rocket-part', 'item', shared_items, prefered_recipes)

# pp.pprint(recipe_tree)
# save_dict(recipe_tree)

# pp.pprint()
# pp.pprint(find_all_item_recipes('petroleum-gas'))

# ====================================================================================

prefered_machines = ['assembling-machine-3']
# module_priorities = {'assembling-machine-3': {'module_priority': [{'productivity-module-3': 4}, {'speed-module-3': 4}]}}

# def multiplier_calculator

# prod_tree = build_production_tree(1, 'item', 'advanced-circuit', shared_items, prefered_recipes, prefered_machines)
prod_tree = build_production_tree(1, 'item', 'processing-unit', shared_items, prefered_recipes, prefered_machines)
# prod_tree = build_production_tree(0.1, 'item', 'rocket-part', shared_items, prefered_recipes)

pp.pprint(prod_tree)
save_dict(prod_tree)

# pp.pprint()
# pp.pprint(find_all_item_recipes('petroleum-gas'))
