import pytest
import json
import os
from jsonschema import Draft7Validator
from fecfile_validate import validate


@pytest.fixture
def sample_ie():
    with open(
        os.path.join(os.path.dirname(__file__), "sample_independent_expenditure.json")
    ) as f:
        form_data = json.load(f)
    return form_data


def test_ie(sample_ie):
    validation_result = validate.validate("INDEPENDENT_EXPENDITURE_PARENTS", sample_ie)
    # pass if election code is Gxxxx without candidate state
    assert validation_result.errors == []
    sample_ie["election_code"] = "P2020"
    validation_result = validate.validate("INDEPENDENT_EXPENDITURE_PARENTS", sample_ie)
    # faile if election code is Pxxxx without candidate state
    assert validation_result.errors[0].path == "so_candidate_state"
