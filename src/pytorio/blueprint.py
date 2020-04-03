from enum import IntEnum

# ============================================================================

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__class__.__name__ + self.__str__()

    @staticmethod
    def to_dict(position):
        return {"x":position.x, "y":position.y}

    @staticmethod
    def from_dict(pos_dict):
        return Position(pos_dict["x"], pos_dict["y"])

# ============================================================================

class Direction(IntEnum):
    NORTH = 0
    EAST = 2
    SOUTH = 4
    WEST = 6

# ============================================================================

class Logistic_Filter:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __str__(self):
        return "(name: {}, count: {})".format(self.name, self.count)

    def __repr__(self):
        return self.__class__.__name__ + self.__str__()


    @staticmethod
    def generate_indexes(logistic_filter_list):
        """Takes a list of logistic filters and correctly given them each and index."""
        i = 1
        for logistic_filter in logistic_filter_list:
            logistic_filter.index = i
            i += 1


    @staticmethod
    def to_dict(logistic_filter):
        return {"name": logistic_filter.name, "index": logistic_filter.index, "count": logistic_filter.count}


    @staticmethod
    def from_dict(lf_dict):
        return Logistic_Filter(lf_dict["name"], lf_dict["count"])

# ============================================================================

class Entity:
    def __init__(self, name:str, position:Position, direction:Direction=None, bar:int=None, recipe:str=None, request_filter_list:list=None):
        self.name = name
        self.position = position
        if direction != None: self.direction = direction
        if bar != None: self.bar = bar
        if recipe != None: self.recipe = recipe
        if request_filter_list != None: self.request_filters = request_filter_list


    def __str__(self):
        e_str = "(name: {},  {}".format(self.name, repr(self.position))

        if hasattr(self, "direction"): e_str += ",  " + str(self.direction)
        if hasattr(self, "bar"): e_str += ",  bar: " + str(self.bar)
        if hasattr(self, "recipe"): e_str += ",  recipe: " + self.recipe
        if hasattr(self, "request_filters"): e_str += ",  " + str(self.request_filters)
        e_str += ")"

        return e_str


    def __repr__(self):
        return self.__class__.__name__ + self.__str__()


    @staticmethod
    def generate_all_numbers(entity_list:list):
        """Generates all the entity_numbers/indexes for contents of this entity"""
        i = 1
        for entity in entity_list:
            entity.entity_number = i
            i += 1

            if hasattr(entity, "request_filters"): Logistic_Filter.generate_indexes(entity.request_filters)


    @staticmethod
    def to_dict(entity):
        entity_dict = {
            "entity_number": entity.entity_number,
            "name": entity.name,
            "position": Position.to_dict(entity.position)
        }
        if hasattr(entity, "direction"): entity_dict.update({"direction": int(entity.direction)})
        if hasattr(entity, "bar"): entity_dict.update({"bar": entity.bar})
        if hasattr(entity, "recipe"): entity_dict.update({"recipe": entity.recipe})
        if hasattr(entity, "request_filters"):
            entity_dict.update({
                "request_filters": [Logistic_Filter.to_dict(logistic_filter) for logistic_filter in entity.request_filters]
            })

        return entity_dict


    @staticmethod
    def from_dict(entity_dict):
        direction = Direction(entity_dict.get("direction"))
        bar = entity_dict.get("bar")
        recipe = entity_dict.get("recipe")
        request_filters = [Logistic_Filter.from_dict(lf_dict) for lf_dict in entity_dict.get("request_filters")]

        return Entity(entity_dict["name"], Position.from_dict(entity_dict["position"]), direction, bar, recipe, request_filters)

# ============================================================================

class Blueprint:
    default = {
        "blueprint": {
            "entities": [],
            "tiles": [],
            "icons": [
                {
                    "index": 1,
                    "signal": {
                        "name": "signal-info",
                        "type": "virtual"
                    }
                }
            ],
            "item": "blueprint",
            "label": "main",
            "version": 73017917444
        }
    }

    # TODO make Blueprint a proper class, and not a hack!!!
    def __init__(self, entities:list):
        self.entities = entities

    # def add_entity(self, entity):
    #     self.entities.append(entity)

    # def add_entities(self, *args):
    #     self.entities.extend(args)

    @staticmethod
    def to_dict(blueprint):
        bp_dict = blueprint.default.copy()
        Entity.generate_all_numbers(blueprint.entities)
        bp_dict["blueprint"]["entities"] = [Entity.to_dict(entity) for entity in blueprint.entities]

        return bp_dict

    @staticmethod
    def from_dict(bp_dict):
        return Blueprint([Entity.from_dict(entity_dict) for entity_dict in bp_dict["blueprint"]["entities"]])
