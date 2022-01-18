"""Convert the FEC validation Excel spreadsheet into JSON schema documents.

This is a utility script to create *starter* JSON schema document templates
from the FEC validation Excel spreadsheet found in the FEC VenPak zip file
that can be downloaded from:

https://www.fec.gov/help-candidates-and-committees/filing-reports/fecfile-software/

The JSON schema standard can be found here:

http://json-schema.org/

Note: Schema properties prefixed with "fec_" are not part of the JSON schema
standard and are specific to the FEC data.
"""

import openpyxl
import json
import argparse

parser = argparse.ArgumentParser(description='Convert the FEC validation Excel spreadsheet into JSON schema documents.')
parser.add_argument('excel_filename', help='an excel filename that will be parsed to generate JSON schema docs')
args = parser.parse_args()
FILENAME = args.excel_filename or "Form_3X_ Receipts_Vendor_10.20.2020.xlsx"
print(FILENAME)
SCHEMA_ID_PREFIX = "https://github.com/mjtravers/fecfile-online-sandbox/blob/main/validator/schema"

# Column postions of fields in the spreadsheet row array
COL_SEQ = 0
FIELD_DESCRIPTION = 1
TYPE = 2
REQUIRED = 3
SAMPLE_DATA = 4
VALUE_REFERENCE = 5
RULE_REFERENCE = 6



def convert_row_to_property(row):# noqa
    """Take a row from the spreadsheet and convert it into a schema object.

    Args:
        row (array): Single row from the spreadsheet

    Returns:
        token (string): The token key identifier for this property in the schema.
        prop (dict): The property object to add to the schema.
    """
    prop = {}
    field_type = row[TYPE].strip()
    token = row[FIELD_DESCRIPTION].strip().replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")

    prop["title"] = row[FIELD_DESCRIPTION].strip()
    prop["description"] = ""

    if field_type.startswith("AMT-"):
        prop["type"] = "number"

    if field_type.startswith("NUM-"):
        prop["type"] = "integer"

    if field_type.startswith("AMT-") or field_type.startswith("NUM-"):
        prop["minimum"] = 0
        prop["maximum"] = int('9' * int(field_type.split('-')[1]))

    if field_type.startswith("A/N-") or field_type.startswith("A-"):
        if field_type == "A-1" and isinstance(row[RULE_REFERENCE], str) and row[RULE_REFERENCE].strip() == "Check-box":
            prop["type"] = "boolean"
        else:
            length = field_type.split('-')[1].strip()
            prop["type"] = "string"
            prop["minLength"] = 0
            prop["maxLength"] = int(length)
            prop["pattern"] = f'^[ A-z0-9]{{0,{length}}}$'

    if row[SAMPLE_DATA]:
        prop["examples"] = [row[SAMPLE_DATA]]

    prop["fec_col_seq"] = row[COL_SEQ]
    prop["fec_form_line"] = "0"
    prop["fec_type"] = field_type

    if isinstance(row[REQUIRED], str):
        prop["fec_requiredErrorLevel"] = row[REQUIRED].strip()
        if "error" in row[REQUIRED].strip():
            schema["required"].append(token)
    if isinstance(row[VALUE_REFERENCE], str):
        prop["fec_valueReference"] = row[VALUE_REFERENCE].strip()
    if isinstance(row[RULE_REFERENCE], str):
        prop["fec_ruleReference"] = row[RULE_REFERENCE].strip()

    return (token, prop)


wb = openpyxl.load_workbook(FILENAME)

for ws in wb.worksheets:
    if ws.title in ['All receipts', 'All Schedule A Transactions', 'Version 8.3', 'SUMMARY OF CHANGES']:
        continue

    # we don't care about these now, but will in the future
    if ws.cell(3, 5).value is not None and ws.cell(3, 5).value.strip() == 'Auto populate':
        continue
    
    title = ws.title.replace(' ', '')
    # transaction schemas should be named after their id
    if (isinstance(ws.cell(7, 2).value, str)
            and ws.cell(7, 2).value.strip() == 'TRANSACTION TYPE IDENTIFIER'
            and isinstance(ws.cell(7, 5).value, str)):
        output_file = title + '-' + ws.cell(7, 5).value + '.json'
    else:
        output_file = title + ".json"

    print(f'Parsing {output_file}...')

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f'{SCHEMA_ID_PREFIX}/{output_file}',
        "title": f'FEC {ws.title}',
        "description": ws.cell(1, 1).value,
        "type": "object",
        "properties": {},
        "additionalProperties": False,
        "required": []
    }

    for row in ws.iter_rows(min_row=5, max_col=7, values_only=True):
        if (not row[COL_SEQ]
                or row[COL_SEQ] == "--"
                or not row[FIELD_DESCRIPTION]
                or not row[TYPE]
                or len(row) > 10):
            continue

        print(row)
        token, prop = convert_row_to_property(row)
        schema["properties"][token] = prop

    f = open(output_file, "w")
    f.write(json.dumps(schema, indent=4))
    f.close()
    print('Done')
