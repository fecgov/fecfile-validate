import pytest
import json
import os
from src.fecfile_validate import validate


@pytest.fixture
def sample_f3x():
    with open(os.path.join(os.path.dirname(__file__), "sample_F3X.json")) as f:
        form_data = json.load(f)
    return form_data


def test_is_correct(sample_f3x):
    assert validate.validate("F3X", sample_f3x) == []


def test_missing_required_field(sample_f3x):
    # Create error by removing FORM_TYPE
    sample_f3x["form_type"] = ""

    errors = validate.validate("F3X", sample_f3x)
    assert errors[0].schema_path[1] == "form_type"
    assert errors[0].schema_path[2] == "enum"
    assert errors[0].message == "'' is not one of ['F3XN', 'F3XA', 'F3XT']"


def test_invalid_string_character(sample_f3x):
    # Create error by adding a '$' to COMMITTEE_NAME
    sample_f3x["committee_name"] = "Foe$ of Pat"
    message_match = "'Foe$ of Pat' does not match '^[ A-z0-9]{0,200}$'"

    errors = validate.validate("F3X", sample_f3x)
    assert errors[0].schema_path[1] == "committee_name"
    assert errors[0].schema_path[2] == "pattern"
    assert errors[0].message == message_match
