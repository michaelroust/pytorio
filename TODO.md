## Long term:
 - Cost function = sum of all edge_costs between machines where: edge_cost = (distance_between_machines * item_rate_between_machines)

 - Look into Makefile
 - Look into python "sphinx" for documentation generation
 - Maybe `.gitignore` .env again. And find a proper way to do this
 - Create a scala project for similar purposes
 - Potential to split calculator into two parts... One that build a recipe_tree and the next
   that updates info on the tree. Using for example the beacons that a specific part would us and etc.



## Short term:
 - prod_tree vs prod_list (using topological sort for dependecies). Maybe allow combinations of both...



## No
 - put `test_submodule.py` into `pytorio/test_submodule.py`. Tried and failed!
