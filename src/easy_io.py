
from pytorio.encoding import beatify_json, exg_str_to_json_str, json_str_to_dict, dict_to_json_str, json_str_to_exg_str

# TODO use read/write_file in these two bit functions

def decode_file(input_filename :str, json_output_filename:str=None, dict_output_filename:str=None) -> dict:
    """Takes a file containing a blueprint string and turns it into a dict.
    If json_output_filname is given a value the loaded blueprint will also be
    written to that file in json format."""

    with open(input_filename) as fin:
        exg_str = fin.read()

    mini_json_str = exg_str_to_json_str(exg_str) # mini as in minified
    json_str = beatify_json(mini_json_str)

    if (json_output_filename != None):
        with open(json_output_filename, 'w') as fout:
            fout.write(json_str)

    bp_dict = json_str_to_dict(mini_json_str)

    if (dict_output_filename != None):
        with open(dict_output_filename, 'w') as fout:
            fout.write(str(bp_dict))

    return bp_dict


def encode_file(input_dict :dict, json_output_filename :str =None, output_filename :str =None):
    """Take a python dict (containing blueprint info) and encodes it into a
    json file and a exchange string file."""

    mini_json_str = dict_to_json_str(input_dict)
    json_str = beatify_json(mini_json_str)

    if (json_output_filename != None):
        with open(json_output_filename, "w") as fout:
            fout.write(json_str)

    exg_str = json_str_to_exg_str(mini_json_str)

    if (output_filename != None):
        with open(output_filename, "w") as fout:
            fout.write(exg_str)


def read_file(filename:str):
    with open(filename) as fin:
        return fin.read()

def write_file(text:str, filename:str):
    with open(filename, 'w') as fout:
        fout.write(text)
