"""Validate instances of FEC form data against validation schema"""

import os
import re
import json
from jsonschema import Draft7Validator
import logging

logger = logging.getLogger(__name__)


class ValidationError:
    def __init__(self, message, path):
        self.message = message
        self.path = path


class ValidationResult:
    def __init__(self, errors=[], warnings=[]):
        self.errors = errors
        self.warnings = warnings


def get_schema(schema_name):
    """Return form schema as JSON object

    Args:
        schema_name (str): name of schema to retrieve file for

    Returns:
        dict: JSON schema that matches the schema_name"""
    schema_file = f"{schema_name}.json"
    schema_path = os.path.join(os.path.dirname(__file__), "schema/", schema_file)
    #: Handle case where we are not running from a pip package
    if not os.path.isfile(schema_path):
        logger.warning(f"Schema file ({schema_path}) not found in package.")
        schema_path = os.path.join(
            os.path.dirname(__file__), "../../../schema/", schema_file
        )
    with open(schema_path) as fp:
        form_schema = json.load(fp)

    return form_schema


def parse_schema_error(error):
    """Parses jsonschema's ValidationError down to a simpler error

    Args:
        error jsonschema.ValidationError: error to be parsed

    Returns:
        ValidationError: a simpler error object
    """
    path = ".".join(error.path or [])
    if error.validator == "required":
        """Required fields are handled at the parent level
        To get what field failed we must parse the message
        """
        field = re.search("^'([^']*)", error.message).group(1)
        path = ".".join(filter(None, [path, field]))
    return ValidationError(error.message, path)


def validate(schema_name, form_data, fields_to_validate=None):
    """Wrapper function around jsonschema validator

    Args:
        schema_name (str): unique identifier that maps to the
            JSON schema definition file
        data (dict): key-value pairs of data to be validated.
            Keys match the properties of the JSON schema file
        fields_to_validate (list): list of property names to validate.
            Properties from the schema not in this list will not be
            validated on, even if they are required.

    Returns:
        list of ValidationError: A list of all errors found in form_data"""
    form_schema = get_schema(schema_name)

    validator = Draft7Validator(form_schema)
    errors = list(map(parse_schema_error, validator.iter_errors(form_data)))
    if fields_to_validate:
        in_fields_to_validate = lambda field: field.path in fields_to_validate
        errors = list(filter(in_fields_to_validate, errors))
    return ValidationResult(errors, [])
