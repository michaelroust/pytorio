# The pytorio_playground "main"

import pprint

import easy_io
from pytorio import encoding, calculator

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


def foo():
    folder = 'src/pytorio/resources/example_blueprints/'
    filename_in = folder + 'fluids1.txt'
    filename_out = folder + 'fluids1.json'

    decode_blueprint_file(filename_in, filename_out)


foo()
