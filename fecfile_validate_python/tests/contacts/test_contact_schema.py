import pytest
import json
import os

from fecfile_validate_python.src.fecfile_validate import validate


@pytest.fixture
def sample_ind_contact():
    with open(os.path.join(os.path.dirname(__file__), "sample_contact_IND.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def sample_can_contact():
    with open(os.path.join(os.path.dirname(__file__), "sample_contact_CAN.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def sample_com_contact():
    with open(os.path.join(os.path.dirname(__file__), "sample_contact_COM.json")) as f:
        form_data = json.load(f)
    return form_data


def test_invalid_const_value(sample_ind_contact):
    # Make sure our Individual Contact schema is valid
    validation_result = validate.validate("Contact_Individual", sample_ind_contact)
    assert validation_result.errors == []

    # Check the const type property works by setting an invalid "type" property
    sample_ind_contact["type"] = "Individual"
    validation_result = validate.validate("Contact_Individual", sample_ind_contact)
    assert validation_result.errors[0].path == "type"
    assert validation_result.errors[0].message == "'IND' was expected"


def test_required_candidate_state(sample_can_contact):
    # Make sure our presidential candidate contact schema is valid
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors == []

    # Fail null for candidate state when office is S
    sample_can_contact["candidate_office"] = "S"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_state"
    assert validation_result.errors[0].message == "None is not of type 'string'"

    # Fail not having candidate state at all when office is S
    del sample_can_contact["candidate_state"]
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_state"
    assert (
        validation_result.errors[0].message
        == "'candidate_state' is a required property"
    )

    # Fail null for candidate district when office is H
    sample_can_contact["candidate_state"] = "VA"
    sample_can_contact["candidate_office"] = "H"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert validation_result.errors[0].message == "None is not of type 'string'"

    # Fail invalid candidate district code
    sample_can_contact["candidate_district"] = "ZZ"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert validation_result.errors[0].message == "'ZZ' does not match '^[0-9]{2}$'"

    # Fail not having a candidate district when office is H
    del sample_can_contact["candidate_district"]
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert (
        validation_result.errors[0].message
        == "'candidate_district' is a required property"
    )


def test_committee_id_format(sample_com_contact):
    # Make sure our committee contact schema is valid
    validation_result = validate.validate("Contact_Committee", sample_com_contact)
    assert validation_result.errors == []

    # Too short
    sample_com_contact["committee_id"] = "C123"
    validation_result = validate.validate("Contact_Committee", sample_com_contact)
    assert validation_result.errors[0].path == "committee_id"
    assert validation_result.errors[0].message == "'C123' does not match '^C[0-9]{8}$'"

    # Wrong characters
    sample_com_contact["committee_id"] = "123ABCDEF"
    validation_result = validate.validate("Contact_Committee", sample_com_contact)
    assert validation_result.errors[0].path == "committee_id"
    assert (
        validation_result.errors[0].message
        == "'123ABCDEF' does not match '^C[0-9]{8}$'"
    )


def test_candidate_id_format(sample_can_contact):
    # Make sure our committee contact schema is valid
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors == []

    # Presidential format
    sample_can_contact["candidate_id"] = "P12345678"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors == []

    # Senate format
    sample_can_contact["candidate_id"] = "S0VA12345"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors == []

    # Too short
    sample_can_contact["candidate_id"] = "P123"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_id"
    assert (
        validation_result.errors[0].message
        == "'P123' does not match '^P[0-9]{8}$|^[H|S][0-9]{1}[A-Z]{2}[0-9]{5}$'"
    )

    # Wrong characters
    sample_can_contact["candidate_id"] = "12345AB1"
    validation_result = validate.validate("Contact_Candidate", sample_can_contact)
    assert validation_result.errors[0].path == "candidate_id"
    assert (
        validation_result.errors[0].message
        == "'12345AB1' does not match '^P[0-9]{8}$|^[H|S][0-9]{1}[A-Z]{2}[0-9]{5}$'"
    )
