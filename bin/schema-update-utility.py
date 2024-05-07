# Utility script to perform mass updates to the schema file.
# NOTE: Be sure to run from the fecfile-Validate/schema directory
#
import glob
import json
import re
from decimal import Decimal


def encoder_override(obj):
    if isinstance(obj, Decimal):
        # We block out Decimals in | symbols so that we can
        # clean them of their surrounding quotation marks later.
        return "|" + str(obj) + "|"

    return json.JSONEncoder.default(obj)


def restore_decimal_values(json_string):
    regex = re.compile(r'"\|(.*)\|"')
    return regex.sub("\\1", json_string)


def process(file, schema):
    print("*** " + file)

    report_type = {
        "title": "REPORT TYPE",
        "description": "",
        "const": "F3X",
        "examples": ["F3X"],
        "fec_spec": {
            "FIELD_DESCRIPTION": "REPORT TYPE",
            "TYPE": "A/N-100",
            "REQUIRED": "X (error)",
            "SAMPLE DATA": "F3X",
            "VALUE REFERENCE": None,
            "RULE REFERENCE": None,
            "FIELD_FORM_ASSOCIATION": None,
        },
    }

    # if 'filer_committee_id_number' in schema['properties']:
    #     schema['properties']['filer_committee_id_number']['pattern'] = \
    #         '^[C|P][0-9]{8}$|^[H|S][0-9]{1}[A-Z]{2}[0-9]{5}$'
    #     (schema['properties']['filer_committee_id_number']['fec_spec']
    #      ['RULE_REFERENCE']) = ('this is the ID of the Committee Account the'
    #                             ' report/transaction is associated with')
    # if 'transaction_id' in schema['properties']:
    #     (schema['properties']['transaction_id']['fec_spec']
    #      ['RULE_REFERENCE']) = ('Must be unique for the life of a report '
    #                             '(original + amendments) within each committee'
    #                             ' account. Letters, if included, must be '
    #                             'uppercase.')
    # if 'contribution_date' in schema['properties']:
    #     schema['properties']['contribution_date']['type'] = 'string'
    # if 'transaction_type_identifier' in schema['properties']:
    #     for property_key in schema['properties'].keys():
    #         del schema['properties'][property_key]['fec_spec']['COL_SEQ']

    # properties = schema['properties']
    # conditionals = schema.get('allOf', [])
    changed = False

    if (
        "transaction_id" in schema["properties"]
        and "transaction_type_identifier" in schema["properties"]
    ):
        new_properties = {"report_type": report_type}
        for key, value in schema["properties"].items():
            new_properties[key] = value
        schema["properties"] = new_properties
        schema["required"].insert(0, "report_type")
        changed = True

    # for property in properties.keys():
    #     property_type = properties[property].get('type', [])
    #     if property in schema.get('required', []):
    #         if properties[property].get('minLength') == 0:
    #             properties[property]['minLength'] = 1
    #             changed = True

    #         if isinstance(property_type, list):
    #             if "null" in property_type:
    #                 properties[property]['type'] = "string"
    #                 changed = True

    #         if "examples" in properties[property]:
    #             examples = properties[property]["examples"]
    #             if "none" in examples:
    #                 examples.remove("none")
    #                 changed = True

    #     for condition in conditionals:
    #         if property in condition['then'].get('required', []):
    #             if property in condition['then']:
    #                 if condition['then'][property].get('minLength') == 0:
    #                     condition['then'][property]['minLength'] = 1
    #                     changed = True

    #                 if isinstance(property_type, list):
    #                     if "none" in property_type:
    #                         condition['then'][property]['type'] = 'string'
    #                         changed = True

    return [schema, changed]


exclude_file_list = []

for file in glob.glob("*.json"):

    if file in exclude_file_list:
        continue

    f = open(file)
    schema = json.load(f, parse_float=Decimal)
    f.close()

    schema, changed = process(file, schema)

    if changed:
        f = open(file, "w")

        output = json.dumps(schema, indent=4, default=encoder_override)
        cleaned_output = restore_decimal_values(output)

        f.write(cleaned_output)
        f.close()
