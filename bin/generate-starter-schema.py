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

FILENAME = "FEC_Format_v8.3.0.1.xlsx"
SCHEMA_ID_PREFIX = "https://github.com/mjtravers/fecfile-online-sandbox/blob/main/validator/schema"

# Column postions of fields in the spreadsheet row array
COL_SEQ = 0
FIELD_DESCRIPTION = 1
TYPE = 2
REQUIRED = 3
SAMPLE_DATA = 4
VALUE_REFERENCE = 5
RULE_REFERENCE = 6

def convert_row_to_property(row):
    """Take a row from the spreadsheet and convert it into a schema object.
    
    Args:
        row (array): Single row from the spreadsheet

    Returns:
        token (string): The token key identifier for this property in the schema.
        prop (dict): The property object to add to the schema.
    """
    prop = {}
    field_type = row[TYPE]
    token = row[FIELD_DESCRIPTION].replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")

    prop["title"] = row[FIELD_DESCRIPTION]
    prop["description"] = ""

    if field_type.startswith("AMT-"):
        prop["type"] = "number"

    if field_type.startswith("NUM-"):
        prop["type"] = "integer"

    if field_type.startswith("AMT-") or field_type.startswith("NUM-"):
        prop["minimum"] = 0
        prop["maximum"] = int('9' * int(field_type.split('-')[1]))

    if field_type.startswith("A/N-") or field_type.startswith("A-"):
        if field_type == "A-1" and row[RULE_REFERENCE] == "Check-box":
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

    if row[REQUIRED]:
        prop["fec_requiredErrorLevel"] = row[REQUIRED]
        if "error" in row[REQUIRED]:
            schema["required"].append(token)
    if row[VALUE_REFERENCE]:
        prop["fec_valueReference"] = row[VALUE_REFERENCE]
    if row[RULE_REFERENCE]:
        prop["fec_ruleReference"] = row[RULE_REFERENCE]

    return (token, prop)


wb = openpyxl.load_workbook(FILENAME)

for ws in wb.worksheets:

    if ws.title in ['Version 8.3', 'SUMMARY OF CHANGES']:
        continue

    output_file = ws.title.replace(' ', '') + ".json"
    print(f'Creating {output_file}...')

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
            or len(row) > 10):
            continue

        print(row)
        token, prop = convert_row_to_property(row)
        schema["properties"][token] = prop

    f = open(output_file, "w")
    f.write(json.dumps(schema, indent=4))
    f.close()
    print('Done')
