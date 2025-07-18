"""Script to read in a JSON schema file and output HTML to STDOUT that
displays the current spec in table format.

USAGE: python generate-spec-table.py MY_SCHEMA.json > MY_SPEC_TABLE.html
"""

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "filename", help="filename of JSON schema doc to convert to HTML table"
)
args = parser.parse_args()

f = open(args.filename)
data = json.load(f)
f.close()

title = args.filename.split(".")[0]

COLUMNS = [
    "COL SEQ",
    "FIELD DESCRIPTION",
    "TYPE",
    "REQUIRED",
    "SAMPLE DATA",
    "VALUE REFERENCE",
    "RULE REFERENCE",
    "FIELD FORM ASSOCIATION",
    "VALIDATION RULES",
]

FEC_PROPERTIES = [
    "COL_SEQ",
    "FIELD_DESCRIPTION",
    "TYPE",
    "REQUIRED",
    "SAMPLE_DATA",
    "VALUE_REFERENCE",
    "RULE_REFERENCE",
    "FIELD_FORM_ASSOCIATION",
]

if not args.filename.startswith("Sch"):
    COLUMNS = COLUMNS[1:]
    FEC_PROPERTIES = FEC_PROPERTIES[1:]

print(
    f'<!DOCTYPE html><html lang="en"><head><title>{title}</title>'
    '<link rel="stylesheet" href="spec_table.css"></head><body><table>'
    f"<caption>Specification for {title}</caption><tr>"
)


def get_conditions(all_of):
    conditions = []
    for q in all_of["if"]["properties"]:
        if "const" in all_of["if"]["properties"][q]:
            conditions.append(
                f"{q.upper()} equals {all_of['if']['properties'][q]['const']}"
            )
        if "enum" in all_of["if"]["properties"][q]:
            conditions.append(
                f"{q.upper()} one of {all_of['if']['properties'][q]['enum']}"
                )
        if "minimum" in all_of["if"]["properties"][q]:
            conditions.append(
                f"{q.upper()} >= {all_of['if']['properties'][q]['minimum']}"
            )
        if "pattern" in all_of["if"]["properties"][q]:
            conditions.append(
                f"{q.upper()} matches regex: {all_of['if']['properties'][q]['pattern']}"
            )
        if (
            "type" in all_of["if"]["properties"][q]
            and len(all_of["if"]["properties"][q]) == 1
        ):
            conditions.append(f"{q.upper()} is populated")
    return conditions


for c in COLUMNS:
    print(f"<th>{c}</th>")
print("</tr>")

for p in data["properties"]:
    print("<tr>")
    for s in FEC_PROPERTIES:
        if s not in data["properties"][p]["fec_spec"].keys():
            print("<td></td>")
            continue
        value = data["properties"][p]["fec_spec"][s]
        if not value:
            value = ""
        print(f"<td>{value}</td>")

    validation_rules = "<ul>"
    if "allOf" in data:
        for all_of in data["allOf"]:
            if "required" in all_of["then"] and p in all_of["then"]["required"]:
                conditions = get_conditions(all_of)
                validation_rules += f"<li>REQUIRED if {' & '.join(conditions)}</li>"

            if (
                "properties" not in all_of["then"]
                or p not in all_of["then"]["properties"]
            ):
                continue

            if "const" in all_of["then"]["properties"][p]:
                const_value = all_of["then"]["properties"][p]["const"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} = '{const_value}'"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "enum" in all_of["then"]["properties"][p]:
                enum_value = all_of["then"]["properties"][p]["enum"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} must be one of {enum_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "pattern" in all_of["then"]["properties"][p]:
                pattern_value = all_of["then"]["properties"][p]["pattern"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} must match {pattern_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "minimum" in all_of["then"]["properties"][p]:
                min_value = all_of["then"]["properties"][p]["minimum"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} >= {min_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "maximum" in all_of["then"]["properties"][p]:
                max_value = all_of["then"]["properties"][p]["maximum"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} <= {max_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "exclusiveMinimum" in all_of["then"]["properties"][p]:
                min_value = all_of["then"]["properties"][p]["exclusiveMinimum"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} > {min_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"
            if "exclusiveMaximum" in all_of["then"]["properties"][p]:
                max_value = all_of["then"]["properties"][p]["exclusiveMaximum"]
                conditions = get_conditions(all_of)
                result = f"{p.upper()} < {max_value}"
                validation_rules += f"<li>{result} if {' & '.join(conditions)}</li>"

    if p in data["required"]:
        validation_rules += "<li>REQUIRED</li>"
    if "type" in data["properties"][p]:
        validation_rules += f"<li>type: {data['properties'][p]['type']}</li>"
    if "const" in data["properties"][p]:
        validation_rules += f"<li>must equal: {data['properties'][p]['const']}</li>"
    if "enum" in data["properties"][p]:
        validation_rules += f"<li>must be one of: {data['properties'][p]['enum']}</li>"
    if "minLength" in data["properties"][p]:
        validation_rules += f"<li>min length: {data['properties'][p]['minLength']}</li>"
    if "maxLength" in data["properties"][p]:
        validation_rules += f"<li>max length: {data['properties'][p]['maxLength']}</li>"
    if "pattern" in data["properties"][p]:
        validation_rules += f"<li>regex: {data['properties'][p]['pattern']}</li>"
    if "minimum" in data["properties"][p]:
        validation_rules += f"<li>minimum: {data['properties'][p]['minimum']}</li>"
    if "maximum" in data["properties"][p]:
        validation_rules += f"<li>maximum: {data['properties'][p]['maximum']}</li>"
    if "exclusiveMinimum" in data["properties"][p]:
        validation_rules += (
            f"<li>greater than: {data['properties'][p]['exclusiveMinimum']}</li>"
        )
    if "exclusiveMaximum" in data["properties"][p]:
        validation_rules += (
            f"<li>less than: {data['properties'][p]['exclusiveMaximum']}</li>"
        )

    print(f"<td>{validation_rules}</td>")
    print("</tr>")
print("</table></body></html>")
