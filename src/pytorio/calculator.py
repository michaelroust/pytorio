from pytorio.prototype_loader import recipes, machines, items

ROUNDING_DECIMALS = 3

# Idea: Add a function that picks the first/default recipe it finds for items with many recipes


def find_all_item_recipes(item_name: str) -> list:
    """Returns a list of all recipe_names that can make item item_name."""

    all_item_recipes = set()
    for recipe in recipes.values():
        for product in recipe["products"]:
            if product["name"] == item_name:
                all_item_recipes.add(recipe["name"])

    return list(all_item_recipes)


def find_item_recipe(item_name: str, prefered_recipes: dict = {}):
    """
    Finds recipe_name of given item_name. Will first check if item_name has
    manually set prefered_recipes.

    prefered_recipes - dict of (item_name, prefered_recipe_name) pairs.

    If (recipe is found) Returns the recipe_name
    """

    if (item_name in prefered_recipes.keys()):
        return prefered_recipes[item_name]

    all_item_recipes = find_all_item_recipes(item_name)

    if len(all_item_recipes) == 0:
        return None
    if len(all_item_recipes) == 1:
        return all_item_recipes[0]
    else:
        raise ValueError("Recipe of {item_name} has multiple options. Must specify "
                         "a prefered option!".format(item_name=item_name) + "\n\tOptions:\n\t" + str(all_item_recipes))


def find_all_recipe_machines(recipe_name: str) -> list:
    all_recipe_machines = set()

    crafting_category = recipes[recipe_name]['category']

    for machine in machines.values():
        if crafting_category in machine['crafting_categories']:
            all_recipe_machines.add(machine['name'])

    return list(all_recipe_machines)


def find_recipe_machine(recipe_name: str, prefered_machines: list = []):
    """Finds a machine that can craft recipe_name, if multiple machines can craft
    the recipe it will pick the first machine in prefered_machines that can craft the recipe."""

    all_recipe_machines = find_all_recipe_machines(recipe_name)

    if len(all_recipe_machines) == 0:
        return None
    if len(all_recipe_machines) == 1:
        return all_recipe_machines[0]

    for machine_name in prefered_machines:
        if machine_name in all_recipe_machines:
            return machine_name

    raise ValueError("Recipe {recipe_name} can be made in multiple machines. Must "
                     "specify a machine preference list".format(recipe_name=recipe_name) + "\n\tOptions:\n\t" +
                     str(all_recipe_machines))


def calc_bonus_multipliers(module_setups: dict) -> tuple:
    speed_bonus = 0
    productivity_bonus = 0

    for module_setup in module_setups.items():
        module_name = module_setup[0]
        module_amount = module_setup[1]

        module_effects = items[module_name]['module_effects']
        if 'speed' in module_effects:
            speed_bonus += round(module_effects['speed']['bonus'] * module_amount, 3)
        if 'productivity' in module_effects:
            productivity_bonus += round(module_effects['productivity']['bonus'] * module_amount, 3)

    return (speed_bonus, productivity_bonus)


def calc_combined_multipliers(combined_module_setups: dict, beacon_multiplier: float = 0.5) -> tuple:
    machine_bonuses = calc_bonus_multipliers(combined_module_setups["machine_modules"])
    beacon_bonuses = calc_bonus_multipliers(combined_module_setups["beacon_modules"])

    beacon_amount = combined_module_setups['beacon_amount']
    return [1 + mb + (bb * beacon_amount * beacon_multiplier) for (mb, bb) in zip(machine_bonuses, beacon_bonuses)]


def module_selector_vanilla_max(recipe_name: str, machine_name: str) -> dict:
    """Example module selector function that specifies a 8x8 beacon setup with speed-module-3s.
    And places productivty-module-3s into the machine if possible, otherwise speed-module-3s"""

    module_inventory_size = machines[machine_name]['module_inventory_size']

    productivity_module_limitations = items['productivity-module-3']['limitations']
    machine_module_name = 'productivity-module-3' if recipe_name in productivity_module_limitations else 'speed-module-3'

    return {
        "machine_modules": {
            machine_module_name: module_inventory_size
        },
        "beacon_modules": {
            "speed-module-3": 2
        },
        "beacon_amount": 8
    }


def build_production_tree(item_rate: int,
                          item_type: str,
                          item_name: str,
                          shared_items: list = [],
                          prefered_recipes: dict = {},
                          prefered_machines: list = [],
                          module_selector=None) -> dict:

    production_tree = {
        'item_type': item_type,
        'item_name': item_name,
        'item_rate': round(item_rate, ROUNDING_DECIMALS),
    }

    # -------------------------------------------------------------------------
    # Looking for recipes and subrecipes if needed

    if not (item_name in shared_items):
        recipe_name = find_item_recipe(item_name, prefered_recipes)

        if (recipe_name != None):
            # Add recipe_name if crafting required
            production_tree.update({'recipe_name': recipe_name})

            recipe = recipes[recipe_name]

            #------------------------------------------------------------------
            # Ratios/Modules stuff

            machine_name = find_recipe_machine(recipe_name, prefered_machines)

            speed_multiplier = 1
            productivity_multipiler = 1

            combined_module_setups = None

            if machine_name != None:
                machine = machines[machine_name]

                if module_selector != None:
                    combined_module_setups = module_selector(recipe_name, machine_name)
                    (speed_multiplier, productivity_multipiler) = calc_combined_multipliers(combined_module_setups)

                    if speed_multiplier == 1 and productivity_multipiler == 1:
                        raise Warning('Didnt sepecify any modules or Possible multiplier calculation failure.')

            elif recipe_name == 'rocket-part':  # Special hacky handling of rocket-parts
                if module_selector != None:
                    combined_module_setups = module_selector(recipe_name, 'assembling-machine-3')
                    (speed_multiplier, productivity_multipiler) = calc_combined_multipliers(combined_module_setups)

                    if speed_multiplier == 1 and productivity_multipiler == 1:
                        raise Warning('Didnt sepecify any modules or Possible multiplier calculation failure.')
            else:
                machine = None

            #-------------------------------------------------------------------------
            # Main product

            main_product_per_recipe = -1

            for product in recipe["products"]:
                if product["name"] == item_name:
                    main_product_per_recipe = product["amount"] * product["probability"] * productivity_multipiler
                    break

            recipe_rate = item_rate / main_product_per_recipe
            production_tree.update({'recipe_rate': round(recipe_rate, ROUNDING_DECIMALS)})

            #-------------------------------------------------------------------------
            # Auxiliary products

            auxiliary_products = []
            for product in recipe["products"]:
                if product["name"] != item_name:
                    auxiliary_products.append({
                        'item_type': product['type'],
                        'item_name': product['name'],
                        'item_rate': round(recipe_rate * product['amount'] * product['probability'] *
                                           productivity_multipiler, ROUNDING_DECIMALS)
                    }) # yapf: disable

            if len(auxiliary_products) > 0:
                production_tree.update({'auxiliary_products': auxiliary_products})

            #-------------------------------------------------------------------------
            # Machine stuff

            if machine_name != None:
                recipe_energy = recipe['energy']  # energy = base_craft_time
                machine_base_speed = machine['crafting_speed']

                # input_rate_per_machine =
                # output_rate_per_machine =

                machine_amount = round(recipe_rate * recipe_energy / (machine_base_speed * speed_multiplier),
                                       ROUNDING_DECIMALS)

                if speed_multiplier != 1:
                    production_tree.update({'speed_multiplier': speed_multiplier})
                if productivity_multipiler != 1:
                    production_tree.update({'productivity_multipiler': productivity_multipiler})

                if combined_module_setups != None:
                    production_tree.update(combined_module_setups)

                production_tree.update({
                    'machine_name': machine_name,
                    'machine_amount': round(machine_amount, ROUNDING_DECIMALS)
                })

            #-------------------------------------------------------------------------
            # Subrecipes/subtrees stuff

            subtrees = []

            for ingredient in recipe["ingredients"]:
                subtrees.append(
                    build_production_tree(recipe_rate * ingredient["amount"], ingredient["type"], ingredient["name"],
                                          shared_items, prefered_recipes, prefered_machines, module_selector))

            if len(subtrees) > 0:
                production_tree.update({'subtrees': subtrees})

            #-------------------------------------------------------------------------

    #-------------------------------------------------------------------------

    return production_tree


#=============================================================================


def list_production_tree_inputs(production_tree: dict) -> dict:
    def combine_inputs(inputs1: dict, inputs2: dict):
        for (input_name, input_rate) in inputs2.items():
            # input_name = inp[0]
            # input_rate = inp[1]
            if input_name in inputs1.keys():
                inputs1[input_name] += input_rate
            else:
                inputs1[input_name] = input_rate

    inputs = dict()

    if 'subtrees' in production_tree:
        for subtree in production_tree['subtrees']:
            combine_inputs(inputs, list_production_tree_inputs(subtree))
    else:
        item_name = production_tree['item_name']
        item_rate = production_tree['item_rate']

        combine_inputs(inputs, {item_name: item_rate})

    return inputs


#=============================================================================
# Beware unreadable code down here


def combine_prodution_lists(prod_list1: list, prod_list2: list):
    def recipe_index(recipe_name: str, prod_list: list) -> int:
        i = 0
        for prod_node in prod_list:
            if recipe_name == prod_node['recipe_name']:
                return i

            i += 1
        return -1

    COMBINABLE_FIELDS = ['item_rate', 'machine_amount', 'recipe_rate']

    for node2 in prod_list2:
        recipe_name = node2['recipe_name']
        rl1_index = recipe_index(recipe_name, prod_list1)
        if rl1_index != -1:
            node1 = prod_list1[rl1_index]
            for field in COMBINABLE_FIELDS:
                node1[field] += node2[field]

            i = 0
            for ingredient2 in node2['ingredients']:
                ingredient1 = node1['ingredients'][i]
                i += 1

                ingredient1['item_rate'] += ingredient2['item_rate']

            if 'auxiliary_products' in node2:
                i = 0
                for aux_prod2 in node2['auxiliary_products']:
                    aux_prod1 = node1['auxiliary_products'][i]
                    i += 1

                    aux_prod1['item_rate'] += aux_prod2['item_rate']

        else:
            prod_list1.append(node2)


def prod_tree_to_node(production_tree: dict) -> dict:
    prod_node = None
    if 'subtrees' in production_tree:
        prod_node = production_tree.copy()
        prod_node.pop('subtrees')

        inputs = []
        for subtree in production_tree['subtrees']:
            COPY_KEYS = ['item_type', 'item_name', 'item_rate']
            input_dict = {key: subtree[key] for key in COPY_KEYS}
            inputs.append(input_dict)

        prod_node['ingredients'] = inputs

    return prod_node


def flatten_production_tree(production_tree: dict) -> list:
    prod_list = [prod_tree_to_node(production_tree)]

    if 'subtrees' in production_tree:
        for subtree in production_tree['subtrees']:
            if 'subtrees' in subtree:
                combine_prodution_lists(prod_list, flatten_production_tree(subtree))

    return prod_list


#=============================================================================
