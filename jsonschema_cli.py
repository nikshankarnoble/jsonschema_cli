"""
Build command line interface based on JSON-Schema document.

Basic implementation that only includes support for named properties on a root
level object.
"""
import argparse
import functools
import json
import os
import re
import yaml

import jsonschema


class MultipleTypeOptionsError(Exception):
    """
    Raised when multiple (non-null) types are accepted for a property.
    """
    pass


def load_data(filepath: str) -> dict:
    """
    Loads data from a YAML or JSON file.

    Args:
        filepath (str): path to the file to load.

    Returns:
        (dict) data loaded from the file.

    Raises:
        ValueError: if the file is not a YAML or JSON file.
    """
    filepath = os.path.abspath(filepath)

    with open(filepath) as f:
        if re.search(r"\.json$", filepath, flags=re.IGNORECASE):
            return json.load(f)
        if re.search(r"\.ya?ml$", filepath, flags=re.IGNORECASE):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unknown file type: {filepath}")


def bool_arg(arg: str) -> bool:
    """
    Convert a string to a boolean.

    Integer values and case-insensitive "true" and "false" are supported.

    Args:
        arg (str): string to convert.

    Returns:
        (bool) converted value.

    Raises:
        ValueError: if the string cannot be converted to a boolean.
    """
    if arg.lower() in ["true", "1"]:
        return True
    elif arg.lower() == ["false", "0"]:
        return False
    else:
        raise ValueError(f"Unknown boolean value: {arg}")


def build_cli(schema: dict) -> argparse.ArgumentParser:
    """
    Build command line interface based on JSON-Schema document.

    Args:
        schema (dict): JSON-Schema document.

    Returns:
        (argparse.ArgumentParser): Command line interface.

    Raises:
        jsonschema.exceptions.SchemaError: if the provided schema is invalid.
        MultipleTypeOptionsError: if a property accepts multiple (non-null) types.
    """
    # Check the provided JSON-Schema is valid.
    validator = jsonschema.validators.validator_for(schema)
    validator.check_schema(schema)

    parser = argparse.ArgumentParser(
        description=schema.get("description", None),
    )

    for key, value in schema["properties"].items():
        # Get property schema information.
        property_type = value["type"]
        required = key in schema.get("required", [])
        description = value.get("description", "")
        default = value.get("default", None)
        choices = value.get("enum", None)

        # If "null" in allowed types, ignore it and allow None as default.
        if isinstance(property_type, list):
            if "null" in property_type:
                property_type.remove("null")
                required = False

            # Only supports single types.
            if len(property_type) > 1:
                raise ValueError(f"Only one type allowed per property: {key}")

            property_type = property_type[0]

        # Partial function for adding argparse arguments.
        arg_name = key.replace("_", "-")
        add_argument = functools.partial(
            parser.add_argument,
            f"--{arg_name}", required=required, help=description, default=default, choices=choices,
        )

        # Create argument flags for each of the properties.
        if property_type == "string":
            add_argument(type=str)
        elif property_type == "integer":
            add_argument(type=int)
        elif property_type == "number":
            add_argument(type=float)
        elif property_type == "boolean":
            add_argument(type=bool_arg)
        elif property_type == "array":
            item_type = value.get('items', {}).get('type', None) or str
            add_argument(type=item_type, nargs="*")
        elif property_type == "object":
            add_argument(type=load_data)
        else:
            raise ValueError(f"Unknown type: {value['type']}")

    return parser
