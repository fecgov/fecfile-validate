import pytest
import json
import os
from jsonschema import Draft7Validator
from src.fecfile_validate import validate
import pdb

@pytest.fixture
def sample_ind_contact():
    with open(os.path.join(os.path.dirname(__file__),
              "sample_contact_IND.json")) as f:
        form_data = json.load(f)
    return form_data


@pytest.fixture
def sample_can_contact():
    with open(os.path.join(os.path.dirname(__file__),
              "sample_contact_CAN.json")) as f:
        form_data = json.load(f)
    return form_data


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


def test_required_candidate_state(sample_can_contact):
    # Make sure our presidential candidate contact schema is valid
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors == []


    # Fail null for candidate state when office is S
    sample_can_contact["candidate_office"] = "S"
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors[0].path == "candidate_state"
    assert validation_result.errors[0].message == "None is not of type 'string'"


    # Fail not having candidate state at all when office is S
    del sample_can_contact["candidate_state"]
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors[0].path == "candidate_state"
    assert validation_result.errors[0].message == "'candidate_state' is a required property"


    # Fail null for candidate district when office is H
    sample_can_contact["candidate_state"] = "VA"
    sample_can_contact["candidate_office"] = "H"
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert validation_result.errors[0].message == "None is not of type 'string'"


    # Fail invalid candidate district code
    sample_can_contact["candidate_district"] = "ZZ"
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert validation_result.errors[0].message == "'ZZ' does not match '^[0-9]{2}$'"


    # Fail not having a candidate district when office is H
    del sample_can_contact["candidate_district"]
    validation_result = validate.validate("Contact_Candidate",
                                          sample_can_contact)
    assert validation_result.errors[0].path == "candidate_district"
    assert validation_result.errors[0].message == "'candidate_district' is a required property"
