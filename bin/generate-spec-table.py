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
    "FIELD FORM ASSOCIATION"
]

print(f'<!DOCTYPE html><html lang="en"><head><title>{title}</title>'
      '<link rel="stylesheet" href="spec_table.css"></head><body><table>'
      f'<caption>Specification for {title}</caption><tr>')

for c in COLUMNS:
    print(f'<th>{c}</th>')
print('</tr>')

for p in data['properties']:
    print('<tr>')
    for s in data['properties'][p]['spec']:
        value = data["properties"][p]["spec"][s]
        if not value:
            value = ''
        print(f'<td>{value}</td>')
    print('</tr>')
print('</table></body></html>')
