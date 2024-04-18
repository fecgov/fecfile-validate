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
        "contributor_organization": "contributor_organization_name",
        "transaction_id_number": "transaction_id",
        "election_code_year": "election_code",
        "loan_amount_original": "loan_amount",
        "loan_incurred_date_terms": "loan_incurred_date",
        "loan_due_date_terms": "loan_due_date",
        "loan_interest_rate_terms": "loan_interest_rate",
        "date_of_original_loan": "loan_originally_incurred_date",
        "date_depository_account_established": "depository_account_established_date",
        "a1.loan_restructured": "loan_restructured",
        "a2._date_of_original_loan": "loan_originally_incurred_date",
        "b.1._credit_amount_this_draw": "credit_amount_this_draw",
        "c._others_liable": "others_liable",
        "d._collateral": "collateral",
        "d.1_desc_collateral": "desc_collateral",
        "d.2_collateral_value_amount": "collateral_value_amount",
        "b.2._total_balance": "total_balance",
        "d.3_perfected_interest": "perfected_interest",
        "e.1_future_income": "future_income",
        "e.2_desc_specification_of_the_above": "desc_specification_of_the_above",
        "e.3_estimated_value": "estimated_value",
        "e.4_date_depository_account_established": "depository_account_established_date",
        "e.5_ind_name_account_location": "ind_name_account_location",
        "e.6_street_1": "account_street_1",
        "e.7_street_2": "account_street_2",
        "e.8_city": "account_city",
        "e.9_state": "account_state",
        "e.10_zip": "account_zip",
        "f._basis_of_loan_description": "basis_of_loan_description",
        "g._treasurer_last_name": "treasurer_last_name",
        "g._treasurer_first_name": "treasurer_first_name",
        "g._treasurer_middle_name": "treasurer_middle_name",
        "g._treasurer_prefix": "treasurer_prefix",
        "g._treasurer_suffix": "treasurer_suffix",
        "g._date_signed": "treasurer_date_signed",
        "h._authorized_last_name": "authorized_last_name",
        "h._authorized_first_name": "authorized_first_name",
        "h._authorized_middle_name": "authorized_middle_name",
        "h._authorized_prefix": "authorized_prefix",
        "h._authorized_suffix": "authorized_suffix",
        "h._authorized_title": "authorized_title",
        "h._date_signed": "authorized_date_signed",
        "beginning_balance_this_period": "beginning_balance",
        "incurred_amount_this_period": "incurred_amount",
        "payment_amount_this_period": "payment_amount",
        "balance_at_close_this_period": "balance_at_close",
        "calendar_y-t-d_per_election_office": "calendar_ytd_per_election_office",
        "payee_cmtte_fec_id_number": "payee_committee_fec_id",
        "s_o_candidate_id_number": "so_candidate_id_number",
        "s_o_candidate_last_name": "so_candidate_last_name",
        "s_o_candidate_first_name": "so_candidate_first_name",
        "s_o_candinate_middle_name": "so_candidate_middle_name",
        "s_o_candidate_prefix": "so_candidate_prefix",
        "s_o_candidate_suffix": "so_candidate_suffix",
        "s_o_candidate_office": "so_candidate_office",
        "s_o_candidate_district": "so_candidate_district",
        "s_o_candidate_state": "so_candidate_state",

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
        field_name = clean_field_name(field_name_raw)
        if field_name in name_overrides:
            field_name = name_overrides[field_name]

        if field_name not in skipped_fields:
            fields[field_name] = row

        row += 1

    return fields


def clean_field_name(field_name):
    clear_whitespace = field_name.strip(" ")
    underscored = clear_whitespace.replace(" ", "_")
    no_parens = underscored.replace("(", "").replace(")", "")
    no_percent = no_parens.replace("%", "")
    no_question = no_percent.replace("?", "")
    no_slash = no_question.replace("/", "_")
    no_yes_no = no_slash.replace("yes_no_", "")
    no_double_underscore = no_yes_no.replace("__", "_")
    no_surrounding_underscores = no_double_underscore.strip("_")
    return no_surrounding_underscores


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
