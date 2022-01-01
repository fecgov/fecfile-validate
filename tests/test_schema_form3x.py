import pytest
import json
import os
from app.form3x import validate

@pytest.fixture
def sample_form3x():
    with open(
        os.path.join(os.path.dirname(__file__), 'sample_form3x.json')
    ) as f:
        form_data = json.load(f)
    return form_data

def test_is_correct(sample_form3x):
    assert validate(sample_form3x) == []

def test_missing_required_field(sample_form3x):
    # Create error by removing FORM_TYPE
    sample_form3x['FORM_TYPE'] = ""

    errors = validate(sample_form3x)
    assert errors[0].schema_path[1] == 'FORM_TYPE'
    assert errors[0].schema_path[2] == 'enum'
    assert errors[0].message == "'' is not one of ['F3XN', 'F3XA', 'F3XT']"

def test_invalid_string_character(sample_form3x):
    # Create error by adding a '$' to COMMITTEE_NAME
    sample_form3x['COMMITTEE_NAME'] = "Foe$ of Pat"

    errors = validate(sample_form3x)
    assert errors[0].schema_path[1] == 'COMMITTEE_NAME'
    assert errors[0].schema_path[2] == 'pattern'
    assert errors[0].message == "'Foe$ of Pat' does not match '^[ A-z0-9]{0,200}$'"