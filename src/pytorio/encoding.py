"""Handles the encoding and decoding between blueprint strings, json str and python dicts"""

import base64
import json
import zlib

# =============================================================================
# Wrapper functions. These Functions should cover most use cases


def decode(exg_str: str) -> dict:
    """Decodes a factorio exchange string into a python dict"""
    return json_str_to_dict(exg_str_to_json_str(exg_str))


def encode(blueprint_dict: dict) -> str:
    """Encodes a python dict into a factorio exchange string"""
    return dict_to_json_str(json_str_to_exg_str(blueprint_dict))


# =============================================================================
# Helper functions


def exg_str_to_json_str(exg_str):
    """Converts a factorio exchange string (in the form of a utf8 encoded byte array) to a json string"""

    exg_bytes = exg_str.encode("utf8")
    # version_byte = exg_bytes[0] # Obtains the version byte (currently unused)
    decoded_str = base64.b64decode(exg_bytes[1:])
    raw_json_str = zlib.decompress(decoded_str).decode(
        'utf8')  # Decompress (returns binary obj.) and decoded_str into a string
    return raw_json_str  # Does not enforce pretty formatting


def json_str_to_exg_str(json_str, versionByte='0'):
    """Converts a json string to a factorio exchange string"""

    compressed_str = zlib.compress(json_str.encode('utf8'),
                                   9)  # Compressing with zlib deflate using compression level 9
    encoded_bytes = base64.b64encode(compressed_str)  # Base64 encoding.
    exg_str = versionByte + encoded_bytes.decode()  # append version byte to front
    return exg_str


def json_str_to_dict(json_str):
    """Converts a json string to a python dict"""
    return json.loads(json_str)


def dict_to_json_str(blueprint_dict):
    """Converts a python dict to a json string"""
    return json.dumps(blueprint_dict, separators=(",", ":"), ensure_ascii=False)


def beatify_json(raw_json_str):
    """Makes sure the json string is pretty. Unserializes and serializes in order to obtain pretty formatting"""
    return json.dumps(json.loads(raw_json_str), sort_keys=True, indent=4)
