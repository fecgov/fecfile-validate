import pytest
import json
import os
from jsonschema import Draft7Validator
from src.fecfile_validate import validate


@pytest.fixture
def sample_f3x():
    with open(os.path.join(os.path.dirname(__file__), "sample_F3X.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def sample_ind_contact():
    with open(os.path.join(os.path.dirname(__file__),
              "sample_IND_contact.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def test_schema():
    with open(os.path.join(os.path.dirname(__file__),
              "test_schema.json")) as f:
        schema = json.load(f)
    return schema


def test_is_correct(sample_f3x):
    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors == []


def test_missing_required_field(sample_f3x):
    # Create error by removing FORM_TYPE
    sample_f3x["form_type"] = ""

    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors[0].path == "form_type"
    assert (
        validation_result.errors[0].message
        == "'' is not one of ['F3XN', 'F3XA', 'F3XT']"
    )


def test_invalid_string_character(sample_f3x):
    # Create error by adding a '$' to COMMITTEE_NAME
    sample_f3x["committee_name"] = "Foe$ of Pat"
    message_match = "'Foe$ of Pat' does not match '^[ A-Za-z0-9]{0,200}$'"

    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors[0].path == "committee_name"
    assert validation_result.errors[0].message == message_match


def test_non_required_field(sample_f3x):
    sample_f3x["treasurer_middle_name"] = None
    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors == []


def check_error(validation_error, message, path):
    expected_error = validate.ValidationError(message, path)
    assert validation_error.path == expected_error.path
    assert validation_error.message == expected_error.message


def test_parse_validation_error(test_schema):
    test_data = {"top_level_field": {"nested_field": -1}}
    validator = Draft7Validator(test_schema)
    errors = sorted(validator.iter_errors(test_data), key=lambda e: e.path)
    check_error(
        validate.parse_schema_error(errors[0]),
        "-1 is less than or equal to the minimum of 0",
        "top_level_field.nested_field",
    )


def test_parse_required_error(test_schema):
    test_data = {}
    validator = Draft7Validator(test_schema)
    errors = sorted(validator.iter_errors(test_data), key=lambda e: e.path)
    check_error(
        validate.parse_schema_error(errors[0]),
        "'top_level_field' is a required property",
        "top_level_field",
    )

    test_data = {"top_level_field": {}}
    errors = sorted(validator.iter_errors(test_data), key=lambda e: e.path)
    check_error(
        validate.parse_schema_error(errors[0]),
        "'nested_field' is a required property",
        "top_level_field.nested_field",
    )


def test_invalid_const_value(sample_ind_contact):
    # Make sure our Individual Contact schema is valid
    validation_result = validate.validate("Contact_Individual",
                                          sample_ind_contact)
    assert validation_result.errors == []

    # Check the const type property works by setting an invalid "type" property
    sample_ind_contact["type"] = "Individual"
    validation_result = validate.validate("Contact_Individual",
                                          sample_ind_contact)
    assert validation_result.errors[0].path == "type"
    assert validation_result.errors[0].message == "'IND' was expected"
