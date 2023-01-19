from openpyxl import load_workbook
import json
from os import path, listdir
import sys
import re
import time


COLUMNS = {
    "property_name": 0,
    "type": 1,
    "required": 2,
    "sample_data": 3,
    "value_reference": 4,
    "rule_reference": 5,
}


def get_transaction_type_identifier(sheet):
    overrides = {
        "TEXT": "Text",
    }

    tti_row_range = range(5, 11)
    for row in tti_row_range:
        if sheet[f'A{row}'].value == "TRANSACTION TYPE IDENTIFIER":
            return sheet[f'F{row}'].value

    if sheet.title in overrides.keys():
        return overrides[sheet.title]

    return ""


def get_schema_fields(sheet):
    name_overrides = {
        'contribution_purpose_description': 'contribution_purpose_descrip',
        'memo_text/description': 'memo_text_description',
        'contributor_organization': 'contributor_organization_name',
        'contributor_street__1': 'contributor_street_1',
        'contributor_street__2': 'contributor_street_2',
    }

    skipped_fields = [
        'receipt_description',
    ]

    fields = {}
    row = 4
    while sheet['A'+str(row)].value:
        field_name_raw = sheet['A'+str(row)].value.lower()
        field_name = '_'.join(field_name_raw.split(' '))
        if field_name in name_overrides:
            field_name = name_overrides[field_name]

        if field_name[-1] == "_":
            field_name = field_name[:-1]

        if field_name not in skipped_fields:
            fields[field_name] = row

        row += 1

    return fields


def get_schema_property(schema, field_name, property, is_fec_spec=False):
    field = schema['properties'][field_name]
    if is_fec_spec:
        field = field['fec_spec']

    return field[property]


def compare_type(row, schema, field_name):
    errors = []
    expected_type = row[COLUMNS['type']].value
    actual_type = get_schema_property(schema, field_name, 'TYPE', is_fec_spec=True)

    if expected_type == None:
        match = True
    else:
        # Strips the lingering spaces present in some fields of the spreadsheet
        expected_type = expected_type.strip(' ')
        match = (expected_type == actual_type)

    if not match:
        errors.append(f'    Error: {field_name} - Sheet has Type {expected_type} and Schema has {actual_type}')

    return errors


def check_required(row, schema, field_name):
    errors = []
    sheet_required_raw = row[COLUMNS['required']].value
    schema_required_raw = get_schema_property(schema, field_name, 'REQUIRED', is_fec_spec=True)
    schema_required_list = schema['required']

    if sheet_required_raw == None:
        sheet_required = False
    else:
        sheet_required = "X (error)" in sheet_required_raw

    if schema_required_raw == None:
        schema_required = False
    else:
        schema_required = "X (error)" in schema_required_raw

    field_rule_reference = row[COLUMNS['rule_reference']].value
    if field_rule_reference == None:
        conditionally_required = False
    else:
        conditionally_required = "Req" in field_rule_reference

    in_required_list = field_name in schema_required_list
    in_all_of = False
    if conditionally_required and "allOf" in schema.keys():
        for all_of_rule in schema['allOf']:
            if field_name in all_of_rule['then']['required']:
                in_all_of = True
                break

    if sheet_required != schema_required:
        if sheet_required:
            errors.append(f'    Error: {field_name} - This is a required field, but the Schema\'s FEC Spec does not have "X (error)"')
        else:
            errors.append(f'    Error: {field_name} - This is not a required field, but the Schema\'s FEC Spec has "X (error) in it"')

    if not conditionally_required:
        if sheet_required != in_required_list:
            if sheet_required:
                errors.append(f"    Error: {field_name} - This is a required field, but it's not in the Schema's required array")
            else:
                errors.append(f"    Error: {field_name} - This is not a required field, but it is in the Schema's required array")
    else:
        if sheet_required != in_all_of:
            if sheet_required:
                errors.append(f"    Error: {field_name} - This is a conditionally required field, but it's not in the Schema's AllOf")
            else:
                errors.append(f"    Error: {field_name} - This is not a conditionally required field, but it is in the Schema's AllOf")

    return errors


def compare_sample_data(row, schema, field_name):
    errors = []
    sheet_sample_data = row[COLUMNS['sample_data']].value
    schema_sample_data = get_schema_property(schema, field_name, 'SAMPLE_DATA', True)
    if sheet_sample_data != schema_sample_data:
        errors.append(f'    Minor Error: {field_name} - The Sheet has Sample Data of "{sheet_sample_data}" while the Schema has "{schema_sample_data}"')

    return errors


def check_form_type(row, schema, field_name):
    errors = []
    if field_name not in ["form_type", "back_reference_sched_name"]:
        return errors

    form_type = row[COLUMNS['sample_data']].value
    schema_properties = schema['properties'][field_name]

    if "const" in schema_properties.keys():
        if form_type != schema_properties["const"]:
            errors.append(f'    Error: {field_name} - Sheet has Form Type "{form_type}" while the Schema has "{schema_properties["const"]}"')

    elif "enum" in schema_properties.keys():
        if form_type not in schema_properties["enum"]:
            errors.append(f'    Error: {field_name} - Sheet has Form Type "{form_type}" while the Schema has "{schema_properties["enum"]}"')

    return errors


def check_entity_type(row, schema, field_name):
    errors = []
    if field_name != "entity_type":
        return errors

    entity_types = row[COLUMNS['value_reference']].value
    schema_properties = schema['properties'][field_name]

    if "const" in schema_properties.keys():
        if schema_properties["const"] not in entity_types:
            errors.append(f'    Error: {field_name} - Sheet has Entity Type "{entity_types}" while the Schema has "{schema_properties["const"]}"')

    elif "enum" in schema_properties.keys():
        for e_type in schema_properties["enum"]:
            if e_type not in entity_types:
                errors.append(f'    Error: {field_name} - Sheet has Entity Types: "{entity_types}" while the Schema has "{schema_properties["enum"]}"')

    return errors


def check_aggregation_group(row, schema, field_name):
    errors = []
    if field_name != "aggregation_group":
        return errors

    sheet_aggr_group = row[COLUMNS['rule_reference']].value

    schema_aggr_group = schema['properties'][field_name]["const"]

    if sheet_aggr_group:
        sheet_aggr_group = sheet_aggr_group.replace(" ", "_")
        sheet_aggr_group = sheet_aggr_group.replace("-", "_")
        sheet_aggr_group = sheet_aggr_group.upper()

    if sheet_aggr_group != schema_aggr_group:
        errors.append(f'    Error: {field_name} - Sheet has an (adjusted) Aggregation Group of "{sheet_aggr_group}" while the Schema has "{schema_aggr_group}"')

    return errors


def verify(sheet, schema):
    errors = []
    error_check_functions = [
        compare_type,
        check_required,
        check_form_type,
        check_entity_type,
        check_aggregation_group
    ]

    minor_errors = []
    minor_error_check_functions = [
        compare_sample_data,
    ]

    fields = get_schema_fields(sheet)
    for field in fields.keys():
        row = sheet[str(fields[field])]
        for check_function in error_check_functions:
            errors += check_function(row, schema, field)
        for check_function in minor_error_check_functions:
            minor_errors += check_function(row, schema, field)

    return [errors, minor_errors]


def get_help_message():
    return str("""
This script checks for differences between this repo's JSON Schema files and a spec spreadsheet.
The script will scan the local directory for a spreadsheet ending with ".xlsx" unless the user
passes in a valid  spreadsheet file name.

options:
    -v Displays minor errors (e.g. Sample Data mismatches)
    -h Displays this message
    """)


if (__name__ == "__main__"):
    filename = None
    display_minor_errors = False

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if ".xlsx" in arg:
                filename = arg
            if arg == "-v":
                display_minor_errors = True
            if arg == "-h":
                print(get_help_message())
                exit()

    if not filename:
        files = listdir('./')
        xlsx_files = []
        for file in files:
            if re.search("\\.xlsx$", file):
                xlsx_files.append(file)
        if len(xlsx_files) > 0:
            xlsx_files.sort()
            filename = xlsx_files[-1]
            print("\nTesting against found spreadsheet:", filename)
            time.sleep(1.5)

    if not filename or not path.exists(filename):
        print("\nFile does not exist:", filename)
        print(get_help_message())
        exit()

    print()

    workbook = load_workbook(filename)
    sheets = workbook._sheets

    # Sheet titles cannot be longer than 31 characters
    excluded_sheets = [
        "HDR Record",
        "zzEARMARK_MEMO_HEADQUARTERS_ACCOUNT"[:31],
        "zzEARMARK_RECEIPT_HEADQUARTERS_ACCOUNT"[:31],
        "zzEARMARK_MEMO_CONVENTION_ACCOUNT"[:31],
        "zzEARMARK_RECEIPT_CONVENTION_ACCOUNT"[:31],
        "zzEARMARK_MEMO_RECOUNT_ACCOUNT"[:31],
        "zzEARMARK_RECEIPT_RECOUNT_ACCOUNT"[:31],
    ]

    errors = {}
    minor_errors = {}
    missing_schema_files = []
    missing_transaction_type_identifiers = []
    failed_to_open = []
    failed_to_load = []

    for sheet in sheets:
        if sheet.title in excluded_sheets:
            continue

        transaction_type_identifier = get_transaction_type_identifier(sheet)
        if not transaction_type_identifier:
            missing_transaction_type_identifiers.append(sheet.title)
            continue

        schema_file_path = '../schema/'+transaction_type_identifier+'.json'
        if not path.exists(schema_file_path):
            missing_schema_files.append(f'{sheet.title}: {transaction_type_identifier}')
            continue

        json_file = open(schema_file_path, 'r')
        if not json_file:
            failed_to_open.append(f'Failed to open JSON file: {transaction_type_identifier}')
            continue

        schema = json.load(json_file)
        if not schema:
            failed_to_load.append(f'Failed to load JSON: {transaction_type_identifier}')
            continue

        new_errors, new_minor_errors = verify(sheet, schema)
        errors[transaction_type_identifier] = new_errors
        minor_errors[transaction_type_identifier] = new_minor_errors

    sheets_with_errors = list(errors.keys())
    sheets_with_minor_errors = list(minor_errors.keys())
    sheets_with_errors.sort()
    sheets_with_minor_errors.sort()
    missing_schema_files.sort()
    missing_transaction_type_identifiers.sort()
    failed_to_open.sort()
    failed_to_load.sort()

    if (len(missing_schema_files) > 0):
        print("Transaction Type Identifiers without a corresponding JSON Schema file:")
        print("   ", "\n    ".join(missing_schema_files), "\n")

    if (len(missing_transaction_type_identifiers) > 0):
        print("Sheets missing a Transaction Type Identifier:")
        print("   ", "\n    ".join(missing_transaction_type_identifiers), "\n")

    if (len(failed_to_open) > 0):
        print("Failed to open:")
        print("   ", *failed_to_open)

    if (len(failed_to_load) > 0):
        print("Failed to load:")
        print("   ", *failed_to_load)

    sheets = sheets_with_errors
    if (display_minor_errors):
        sheets += sheets_with_minor_errors

    for sheet in sheets:
        if (len(errors[sheet]) > 0):
            print(sheet)
            for error in errors[sheet]:
                print(error)
            if (display_minor_errors):
                for minor_error in minor_errors[sheet]:
                    print(minor_error)
            print('\n')
