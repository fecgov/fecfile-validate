Working on updates to improve the schema files? Find a wealth of information about features of the JSON Schema Standard here: [Understanding JSON Schema](http://json-schema.org/understanding-json-schema/)

### Schema Files

This directory contains the canonical copies of the JSON Standard schema files
defining the validation and business rules of the FEC forms, schedules, and
transaction types.

In addition to the JSON Schema keyword attributes, several custom FEC-specific
attributes were added to the schema for more complex validation rules that
can not be captured using the standard, legacy spec information, and descriptive
meta-data.

**Custom Property Attributes**

- fec_spec: Contains the property spec information captured in the original spec FEC spreadsheets
- fec_recommended: Fields that are not required and will prohibit submission of a form but are recommended, raising a warning if missing

### Data Dictionary

To generate the data dictionary located in the /docs directory:

1. cd into the /schema directory
2. run the command: ../bin/generate_schema_docs.sh

### Schema Backlog

This directory contains the original output of the bin/generate-starter-schema.py
script. The output \*.json files in this directory are parsed from the following
files also contained in this directory:

- FEC_Format_v8.3.0.1.xlsx
- Form_3X_Receipts_Vendor_10.20.2020.xlsx

The listed spreadsheets are the result of previous spec work that is now being
ported and into the JSON Schema Standard format.

During the process of curating these original output files, each file is copied
up to the ../schema directory where it is vetted and manually modified as
needed. The original copy of each file is left in the backlog directory for future
reference.
