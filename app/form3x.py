"""Validate instances of FEC form data against validation schema"""

import os
import json
from jsonschema import Draft7Validator

def get_schema():
    """Return form schema as JSON object"""
    with open(
        os.path.join(os.path.dirname(__file__), '../schema/F3X.json')
    ) as fp:
        form_schema = json.load(fp)
    return form_schema

def validate(form_data):
    """Wrapper function around jsonschema validator"""
    form_schema = get_schema()
    validator = Draft7Validator(form_schema)
    return sorted(validator.iter_errors(form_data), key=lambda e: e.path)
