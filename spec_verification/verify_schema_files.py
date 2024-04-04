from check_transaction_type_identifier import check_transaction_type_identifier
from check_contribution_amount import check_contribution_amount
from check_aggregation_group import check_aggregation_group
from check_entity_types import check_entity_type
from minor_error_checks import check_sample_data
from check_form_type import check_form_type
from check_required import check_required
from check_length import check_length
from check_type import check_type
from utils import FIELD_NAME_COLUMN


def get_schema_fields(sheet, debug):
    name_overrides = {
        "contribution_purpose_description": "contribution_purpose_descrip",
        "memo_text/description": "memo_text_description",
        "contributor_organization": "contributor_organization_name",
        "contributor_street__1": "contributor_street_1",
        "contributor_street__2": "contributor_street_2",
        "transaction_id_number": "transaction_id",
        "payee_street__1": "payee_street_1",
        "payee_street__2": "payee_street_2",
        "election_code/year": "election_code",
    }

    skipped_fields = [
        "receipt_description",
    ]

    fields = {}
    row = None
    for r in range(1, sheet.max_row):
        field_description = sheet[f"{FIELD_NAME_COLUMN}{r}"].value
        if field_description == "FORM TYPE":
            row = r
            break

    if row is None:
        print("    FORM TYPE row not found", sheet.title)

    if debug:
        print("    Determining the schema spreadsheet's fields")

    while sheet[FIELD_NAME_COLUMN + str(row)].value:
        if debug:
            print(f"        Parsing row {row}")

        field_name_raw = sheet[FIELD_NAME_COLUMN + str(row)].value.lower()
        field_name = "_".join(field_name_raw.split(" "))
        if field_name in name_overrides:
            field_name = name_overrides[field_name]

        if field_name[-1] == "_":
            field_name = field_name[:-1]

        if field_name not in skipped_fields:
            fields[field_name] = row

        row += 1

    return fields


def verify(sheet, schema, columns, verbose, debug):
    errors = []
    error_check_functions = [
        check_type,  # Runs on every field
        check_length,  # Runs on every field
        check_required,  # Runs on every field
        check_form_type,  # Runs on form_type and back_reference_sched_name
        check_entity_type,  # Runs on entity_type
        check_contribution_amount,  # Runs on contribution_amount
        check_aggregation_group,  # Runs on aggregation_group
        check_transaction_type_identifier,  # Runs on transaction_type_identifier
    ]

    minor_errors = []
    minor_error_check_functions = [  # Minor Error Checks are only run in VERBOSE mode
        check_sample_data,  # Runs on every field
    ]

    if debug:
        print("    Verifying the JSON schema")

    fields = get_schema_fields(sheet, debug)
    for field in fields.keys():
        if debug:
            print(f"        {field}")
        row = sheet[str(fields[field])]
        for check_function in error_check_functions:
            errors += check_function(row, schema, field, columns)
        for check_function in minor_error_check_functions:
            if verbose:
                minor_errors += check_function(row, schema, field, columns)

    return [errors, minor_errors]
