"""Process Transaction JSON Schema files to determine similar groups.

This utility script creates a grouping of transaction JSON Schemas that are
similar so they can be turned into a single schema with rules to handle
multiple transaction types.

The JSON schema standard can be found here:

http://json-schema.org/

Note: Schema properties prefixed with "fec_" are not part of the JSON schema
standard and are specific to the FEC data.
"""

import json
import os
import glob

OUTPUT = "../bin/transaction-groups.json"
transaction_profiles = {}

for schema_filename in glob.glob('*.json'):
    with open(os.path.join(os.getcwd(), schema_filename), 'r') as f:
        schema_json = json.load(f)
        title = schema_json.get('title')
        properties = schema_json.get('properties')

        transaction_type = properties.get('TRANSACTION_TYPE_IDENTIFIER')
        if transaction_type == None:
            continue
        form_type = properties.get('FORM_TYPE')
        if 'SA' not in form_type.get('fec_valueReference'):
            continue

        fields_str = ''.join(properties)
        similar_schemas = transaction_profiles.get(fields_str, []) + [title]
        transaction_profiles[fields_str] = similar_schemas
        

for profile in sorted(list(transaction_profiles)):
    print(profile)
    for title in transaction_profiles[profile]:
        print("    " + title)
print(f'Number of profiles: {len(transaction_profiles)}')

f = open(os.path.join(os.getcwd(), OUTPUT), "w")
f.write(json.dumps(transaction_profiles, indent=4))
f.close()

print('Done')



