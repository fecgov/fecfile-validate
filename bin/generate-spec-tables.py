"""Script to read in a JSON schema file and output HTML to STDOUT that
displays the current spec in table format.
"""

import glob
import json

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

for file in sorted(glob.glob('*.json')):
    
    title = file.split('.')[0]

    f = open(file)
    data = json.load(f)
    f.close()

    f = open(f'{title}_spec.html', 'w')

    f.write(f'<!DOCTYPE html><html lang="en"><head><title>{title}</title>'
        '<link rel="stylesheet" href="spec_table.css"></head><body><table>'
        f'<caption>Specification for {title}</caption><tr>')

    for c in COLUMNS:
        f.write(f'<th>{c}</th>')
    f.write('</tr>')

    for p in data['properties']:
        f.write('<tr>')
        for s in data['properties'][p]['fec_spec']:
            value = data["properties"][p]["fec_spec"][s]
            if not value:
                value = ''
            f.write(f'<td>{value}</td>')
        f.write('</tr>')
    f.write('</table></body></html>')

    f.close()
