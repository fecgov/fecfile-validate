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
def sample_indv_rec():
    with open(os.path.join(os.path.dirname(__file__), "sample_INDV_REC.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def test_schema():
    with open(os.path.join(os.path.dirname(__file__), "test_schema.json")) as f:
        schema = json.load(f)
    return schema


def test_is_correct(sample_f3x):
    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors == []


def test_missing_required_field(sample_f3x):
    # Create error by removing FORM_TYPE
    sample_f3x.pop("form_type", None)

    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors[0].path == "form_type"
    assert validation_result.errors[0].message == "'form_type' is a required property"


def test_invalid_string_character(sample_f3x):
    # Create error by setting COMMITTEE_NAME to a 201 char string
    sample_f3x["committee_name"] = "a" * 201
    message_end = "is too long"

    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors[0].path == "committee_name"
    assert validation_result.errors[0].message.endswith(message_end)


def test_non_required_field(sample_f3x):
    sample_f3x.pop("treasurer_middle_name", None)
    validation_result = validate.validate("F3X", sample_f3x)
    assert validation_result.errors == []


"""Test parse_schema_error
parse_schema_error needs to parse jsonschema errors and
turn them into ValidationErrors
"""


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


"""Test partial validation
Calling validate with fields_to_validate contrstructs a temporary
schema from the passed schema.  This temporary schema must be a subschema
of the passed schema"""


def test_partial_validate_is_correct(sample_f3x):
    fields_to_validate = ["form_type"]
    # Even though we remove date_signed, the validation should pass
    sample_f3x.pop("date_signed", None)
    validation_result = validate.validate("F3X", sample_f3x, fields_to_validate)
    assert validation_result.errors == []


def test_partial_missing_required_field(sample_f3x):
    fields_to_validate = ["form_type"]
    # Create error by removing FORM_TYPE
    sample_f3x.pop("form_type", None)
    validation_result = validate.validate("F3X", sample_f3x, fields_to_validate)
    assert validation_result.errors[0].path == "form_type"
    assert validation_result.errors[0].message == "'form_type' is a required property"


def test_contribution_amount_accepts_decimals(sample_indv_rec):
    sample_indv_rec["contribution_amount"] = 99.99
    validation_result = validate.validate("INDV_REC", sample_indv_rec)
    assert validation_result.errors == []


def test_contribution_amount_accepts_negative_values(sample_indv_rec):
    sample_indv_rec["contribution_amount"] = -100
    validation_result = validate.validate("INDV_REC", sample_indv_rec)
    assert validation_result.errors == []


def test_contribution_amount_max_length(sample_indv_rec):
    sample_indv_rec["contribution_amount"] = 999999999.99
    validation_result = validate.validate("INDV_REC", sample_indv_rec)
    print(validation_result)
    assert validation_result.errors == []


def test_contribution_amount_fails_with_over_max_length(sample_indv_rec):
    sample_indv_rec["contribution_amount"] = 9999999999.99
    validation_result = validate.validate("INDV_REC", sample_indv_rec)
    assert len(validation_result.errors) > 0
