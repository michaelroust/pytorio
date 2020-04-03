import os
import os.path
import unittest

import easy_io as easy_io
from pytorio import encoding
from pytorio.blueprint import (Blueprint, Direction, Entity, Logistic_Filter, Position)

test_data_path = "test/test_blueprint_encoding_data"


class Test_Blueprint_Encoding(unittest.TestCase):
    def assert_files_equal(self, expected_filename, result_filename):
        """Helper method. Reads two files (as string) and compares contents"""
        with open(expected_filename) as f:
            expected = f.read()
        with open(result_filename) as f:
            result = f.read()
        return self.assertEqual(result, expected)

    def test_gear_array(self):
        """Tests a certain set of machines"""
        def add_single_set(entities, x, y):
            entities.extend([
                Entity("assembling-machine-3", Position(x + 0, y + 0), recipe="iron-gear-wheel"),
                Entity("fast-inserter", Position(x + -2, y + 0), direction=Direction.WEST),
                Entity("logistic-chest-requester",
                       Position(x + -3, y + 0),
                       request_filter_list=[Logistic_Filter("iron-plate", 80)]),
                Entity("fast-inserter", Position(x + 2, y + 0), direction=Direction.WEST),
                Entity("logistic-chest-active-provider", Position(x + 3, y + 0), bar=2)
            ])

        def add_double_set(entities, x, y):
            add_single_set(entities, x + 0, y + -2)
            add_single_set(entities, x + 0, y + 2)
            entities.append(Entity("medium-electric-pole", Position(x, y)))

        entity_list = []

        for i in range(-5, 5):
            add_double_set(entity_list, 0, i * 7)

        blueprint = Blueprint(entity_list)
        bp_dict = Blueprint.to_dict(blueprint)

        if not (os.path.exists(test_data_path + '/result')):
            os.mkdir(test_data_path + '/result')

        easy_io.encode_file(bp_dict, test_data_path + "/result/gear_array.json",
                            test_data_path + "/result/gear_array.txt")

        self.assert_files_equal(test_data_path + "/expected/gear_array.json",
                                test_data_path + "/result/gear_array.json")

    def test_one(self):
        self.assertEqual('foo'.upper(), 'FOO')

    # def test_two(self):
    #     submodule.submodule_fun()
    #     self.assertEqual(0, 0)
