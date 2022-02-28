"""Validate instances of FEC form data against validation schema"""

import os
import json
from jsonschema import Draft7Validator
import logging

logger = logging.getLogger(__name__)


def get_schema():
    """Return form schema as JSON object"""
    schema_file = os.path.join(os.path.dirname(__file__), "../schema/F3X.json")
    #: Handle case where we are not running from a pip package
    if not os.path.isfile(schema_file):
        logger.warning(f"Schema file ({schema_file}) not available where expected.")
        schema_file = os.path.join(
            os.path.dirname(__file__), "../../../../schema/F3X.json"
        )
    with open(schema_file) as fp:
        form_schema = json.load(fp)

    return form_schema


def validate(form_data):
    """Wrapper function around jsonschema validator"""
    form_schema = get_schema()
    validator = Draft7Validator(form_schema)
    return sorted(validator.iter_errors(form_data), key=lambda e: e.path)
