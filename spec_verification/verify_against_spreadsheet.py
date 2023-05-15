"""
Verify local JSON schema files against an Excel spreadsheet.

This script checks for differences between this repo's JSON files and a spec spreadsheet.
The script will scan the local directory for a spreadsheet ending with ".xlsx" unless
the user passes in a valid  spreadsheet file name.

The JSON schema standard can be found here:
http://json-schema.org/
"""


from os import path, listdir, getcwd
from openpyxl import load_workbook
import json
import time
import re

from verify_schema_files import verify


def populate_global_columns(sheet):
    columns = {}
    column_header_row = 0
    for r in range(1, 10):
        value = sheet[f"A{r}"].value
        if value and value.replace("\n", " ") == "FIELD DESCRIPTION":
            column_header_row = r
            break

    if column_header_row == 0:
        return columns

    col_vals = "ABCDEFGHIJKL"
    for c in range(len(col_vals)):
        header = sheet[f"{col_vals[c]}{column_header_row}"].value
        if header:
            cleaned_header = header.replace("\n", "_").replace(" ", "_").lower()
            columns[cleaned_header] = c

    return columns


def get_filename(sheet):
    filename_overrides = {
        (
            "NATIONAL_PARTY_PARTNERSHIP_MEMOS (needs review as it is named "
            "PARTNERSHIP_NATIONAL_PARTY_MEMOS in the code)"
        ): "PARTNERSHIP_NATIONAL_PARTY_MEMOS",
        (
            "NATIONAL_PARTY_PARTNERSHIP_RECEIPTS (needs review as it is named "
            "PARTNERSHIP_NATIONAL_PARTY_RECEIPTS in the code)"
        ): "PARTNERSHIP_NATIONAL_PARTY_RECEIPTS",
    }

    filename = sheet["A2"].value
    if not filename and filename in filename_overrides.keys():
        filename = filename_overrides[filename]

    return filename


def generate_report(
    errors,
    minor_errors,
    missing_schema_files,
    missing_transaction_type_identifiers,
    missing_column_headers,
    failed_to_open,
    failed_to_load,
    verbose=False,
    save=True,
):
    report = "\n"

    sheets_with_errors = list(s for s in errors.keys() if len(errors[s]) > 0)
    sheets_with_minor_errors = list(minor_errors.keys())
    sheets_with_errors.sort()
    sheets_with_minor_errors.sort()
    missing_schema_files.sort()
    missing_transaction_type_identifiers.sort()
    failed_to_open.sort()
    failed_to_load.sort()

    error_count = len(
        [item for sublist in errors.values() for item in sublist]
    )
    sheet_count = len(errors.keys())
    error_sheets_count = len(sheets_with_errors)

    if len(missing_schema_files) > 0:
        report += "Sheets without a corresponding JSON file:\n"
        report += "    " + "\n    ".join(missing_schema_files) + "\n\n"

    if len(missing_transaction_type_identifiers) > 0:
        report += "Sheets missing a Transaction Type Identifier:\n"
        report += "    " + "\n    ".join(missing_transaction_type_identifiers) + "\n\n"

    if len(missing_column_headers) > 0:
        report += "Sheets missing Column Headers:\n"
        report += "    " + "\n    ".join(missing_column_headers) + "\n\n"

    if len(failed_to_open) > 0:
        report += "Failed to open:\n"
        report += "    " + "\n    ".join(failed_to_open) + "\n\n"

    if len(failed_to_load) > 0:
        report += "Failed to load:\n"
        report += "    " + "\n    ".join(failed_to_load) + "\n\n"

    report += f"""
    {error_count} Errors in {error_sheets_count} out of {sheet_count} sheets total\n
    """

    sheets = sheets_with_errors
    if verbose:
        sheets += sheets_with_minor_errors

    for sheet_name in sheets:
        if len(errors[sheet_name]) > 0:
            report += sheet_name + "\n"
            for error in errors[sheet_name]:
                report += error + "\n"
            if verbose:
                for minor_error in minor_errors[sheet_name]:
                    report += minor_error + "\n"
            report += "\n\n"

    print(report)
    if save:
        file = open(path.join(getcwd(), "spec_verification_report.txt"), "w")
        file.write(report)
        file.close()


def run_verification(filename, verbose, debug):
    if not filename:
        files = listdir(getcwd())
        xlsx_files = []
        for file in files:
            if re.search("\\.xlsx$", file):
                xlsx_files.append(file)
        if len(xlsx_files) > 0:
            xlsx_files.sort()
            filename = xlsx_files[-1]
            print("\nTesting against found spreadsheet:", filename)
            time.sleep(1)

    if not filename:
        print("No excel file found")
        exit()
    if not path.exists(filename):
        print("File does not exist:", filename)
        exit()

    workbook = load_workbook(filename)
    sheets = workbook._sheets

    # Sheet titles cannot be longer than 31 characters
    excluded_sheets = [
        "HDR Record",
        "TEXT",
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
    missing_column_headers = []
    failed_to_open = []
    failed_to_load = []

    for sheet in sheets:
        if sheet.title in excluded_sheets:
            continue

        if debug:
            print(sheet.title)

        filename = get_filename(sheet)
        schema_file_path = f"schema/{filename}.json"
        if not path.exists(schema_file_path):
            missing_schema_files.append(f"{sheet.title}: {schema_file_path}")
            continue

        json_file = open(schema_file_path, "r")
        if not json_file:
            failed_to_open.append(f"Failed to open JSON file: {filename}")
            continue

        schema = json.load(json_file)
        if not schema:
            failed_to_load.append(f"Failed to load JSON: {filename}")
            continue

        columns = populate_global_columns(sheet)
        if len(columns.keys()) == 0:
            missing_column_headers.append(sheet.title)
            continue

        new_errors, new_minor_errors = verify(sheet, schema, columns, verbose, debug)
        errors[filename] = new_errors
        minor_errors[filename] = new_minor_errors

    generate_report(
        errors,
        minor_errors,
        missing_schema_files,
        missing_transaction_type_identifiers,
        missing_column_headers,
        failed_to_open,
        failed_to_load,
        verbose,
        save=True,
    )
