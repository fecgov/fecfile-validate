The FEC validator is designed around the definintion of a data dictionary which
defines each line item of each FEC form using the JSON Schema Specification
(http://json-schema.org/).

The baseline for the definition of each fields was defined by and kept in sync
with the FEC Format MS Excel spreadsheet found in the FEC Vendor Pack.
(https://www.fec.gov/help-candidates-and-committees/filing-reports/fecfile-software/)
See bin/generate-starter-schema.py for the script that created the initial
schema definition files that were then manually curated and updated.

The data dictionary can be found in a human-freindly HTML format at:
https://fecgov.github.io/fecfile-Validate/


