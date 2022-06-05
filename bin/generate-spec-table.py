"""Script to read in a JSON schema file and output HTML to STDOUT that
displays the current spec in table format.

USAGE: python generate-spec-table.py MY_SCHEMA.json > MY_SPEC_TABLE.html
"""

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='filename of JSON schema doc to convert'
                    ' to HTML table')
args = parser.parse_args()

f = open(args.filename)
data = json.load(f)
f.close()

title = args.filename.split('.')[0]

COLUMNS = [
    "COL SEQ",
    "FIELD DESCRIPTION",
    "TYPE",
    "REQUIRED",
    "SAMPLE DATA",
    "VALUE REFERENCE",
    "RULE REFERENCE",
    "FIELD FORM ASSOCIATION",
    "VALIDATION RULES"
]

print(f'<!DOCTYPE html><html lang="en"><head><title>{title}</title>'
      '<link rel="stylesheet" href="spec_table.css"></head><body><table>'
      f'<caption>Specification for {title}</caption><tr>')

for c in COLUMNS:
    print(f'<th>{c}</th>')
print('</tr>')

for p in data['properties']:
    print('<tr>')
    for s in data['properties'][p]['fec_spec']:
        if s == 'AUTO_POPULATE':
            continue
        value = data["properties"][p]["fec_spec"][s]
        if not value:
            value = ''
        print(f'<td>{value}</td>')
    validation_rules = '<ul>'

    if 'allOf' in data:
        for allOf in data['allOf']:
            if p in allOf['then']['required']:
                conditions = []
                for q in allOf['if']['properties']:
                    if 'const' in allOf['if']['properties'][q]:
                        conditions.append(f"{q.upper()} equals {allOf['if']['properties'][q]['const']}")
                    if 'enum' in allOf['if']['properties'][q]:
                        conditions.append(f"{q.upper()} one of {allOf['if']['properties'][q]['enum']}")
                    if 'minimum' in allOf['if']['properties'][q]:
                        conditions.append(f"{q.upper()} >= {allOf['if']['properties'][q]['minimum']}")
                validation_rules += f"<li>REQUIRED if {' & '.join(conditions)}</li>"

    if p in data['required']:
        validation_rules += "<li>REQUIRED</li>"
    if 'type' in data['properties'][p]:
        validation_rules += f"<li>type: {data['properties'][p]['type']}</li>"
    if 'const' in data['properties'][p]:
        validation_rules += f"<li>must equal: {data['properties'][p]['const']}</li>"
    if 'enum' in data['properties'][p]:
        validation_rules += f"<li>must be one of: {data['properties'][p]['enum']}</li>"
    if 'minLength' in data['properties'][p]:
        validation_rules += f"<li>min length: {data['properties'][p]['minLength']}</li>"
    if 'maxLength' in data['properties'][p]:
        validation_rules += f"<li>max length: {data['properties'][p]['maxLength']}</li>"
    if 'pattern' in data['properties'][p]:
        validation_rules += f"<li>regex: {data['properties'][p]['pattern']}</li>"
    if 'minimum' in data['properties'][p]:
        validation_rules += f"<li>minimum: {data['properties'][p]['minimum']}</li>"
    if 'maximum' in data['properties'][p]:
        validation_rules += f"<li>maximum: {data['properties'][p]['maximum']}</li>"

    print(f'<td>{validation_rules}</td>')
    print('</tr>')
print('</table></body></html>')
