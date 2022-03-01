"""Validate instances of FEC form data against validation schema"""

import os
import json
from jsonschema import Draft7Validator
import logging

logger = logging.getLogger(__name__)


def get_schema(schema_name):
    """Return form schema as JSON object

    Args:
        schema_name (str): name of schema to retrieve file for

    Returns:
        dict: JSON schema that matches the schema_name"""
    schema_file = f"{schema_name}.json"
    schema_path = os.path.join(
        os.path.dirname(__file__), "schema/", schema_file
    )
    #: Handle case where we are not running from a pip package
    if not os.path.isfile(schema_path):
        logger.warning(f"Schema file ({schema_path}) not found in package.")
        schema_path = os.path.join(
            os.path.dirname(__file__), "../../../schema/", schema_file
        )
    with open(schema_path) as fp:
        form_schema = json.load(fp)

    return form_schema


def validate(schema_name, form_data):
    """Wrapper function around jsonschema validator

    Args:
        schema_name (str): unique identifier that maps to the
            JSON schema definition file
        data (dict): key-value pairs of data to be validated.
            Keys match the properties of the JSON schema file

    Returns:
        list of ValidationError: A list of all errors found in form_data"""
    form_schema = get_schema(schema_name)
    validator = Draft7Validator(form_schema)
    return sorted(validator.iter_errors(form_data), key=lambda e: e.path)
