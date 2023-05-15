from check_transaction_type_identifier import check_transaction_type_identifier
from check_contribution_amount import check_contribution_amount
from check_aggregation_group import check_aggregation_group
from check_entity_types import check_entity_type
from minor_error_checks import check_sample_data
from check_form_type import check_form_type
from check_required import check_required
from check_length import check_length
from check_type import check_type

def get_schema_fields(sheet, verbose, debug):
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
        field_description = sheet[f"A{r}"].value
        if field_description == "FORM TYPE":
            row = r
            break

    if row is None:
        print("    FORM TYPE row not found", sheet.title)

    if debug:
        print("    Determining the schema spreadsheet's fields")

    while sheet["A" + str(row)].value:
        if debug and verbose:
            print(f"        Parsing row {row}")

        field_name_raw = sheet["A" + str(row)].value.lower()
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
    # Check methods are looking for a single field
    # Compare methods run on *every* field

    errors = []
    error_check_functions = [
        check_type,
        check_length,
        check_required,
        check_form_type,
        check_entity_type,
        check_contribution_amount,
        check_aggregation_group,
        check_transaction_type_identifier,
    ]

    minor_errors = []
    minor_error_check_functions = [
        check_sample_data,
    ]

    if debug:
        print("    Verifying the JSON schema")

    fields = get_schema_fields(sheet, verbose, debug)
    for field in fields.keys():
        if debug:
            print(f"        {field}")
        row = sheet[str(fields[field])]
        for check_function in error_check_functions:
            if debug and verbose:
                print(" " * 11, check_function)
            errors += check_function(row, schema, field, columns)
        for check_function in minor_error_check_functions:
            if debug and verbose:
                print(" " * 11, check_function)
            minor_errors += check_function(row, schema, field, columns)

    return [errors, minor_errors]
