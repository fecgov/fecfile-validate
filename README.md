The FEC validator is designed around the definintion of a data dictionary which
defines each line item of each FEC form using the JSON Schema Specification
(http://json-schema.org/).

The baseline for the definition of each fields was defined by and kept in sync
with the FEC Format MS Excel spreadsheet found in the FEC Vendor Pack.
(https://www.fec.gov/help-candidates-and-committees/filing-reports/fecfile-software/)
See bin/generate-starter-schema.py for the script that created the initial
schema definition files that were then manually curated and updated.

The data dictionary schema defines the meta data needed to manage and validate
each form line item. The schema definition files are located
in the /schema directory and consist of the usual JSON Schema Specifiaction meta
data fields augmented with custom FEC meta data fields:

fec_col_seq: COL SEQ column value from FEC Format spreadsheet
fec_form_line: Form line identifier for the line item (if exists)
fec_type: TYPE column value from FEC Format spreadsheet
fec_requiredErrorLevel: REQUIRED column value from FEC Format spreadsheet
fec_valueReference: VALUE_REFERENCE column value from FEC Format spreadsheet

The data dictionary can be found in a human-freindly HTML format at:
https://fecgov.github.io/fecfile-Validate/


##### Install dependencies
```bash
$ pip install -r requirements.txt
```

##### Run the app
```bash
$ python run.py
```

## Test

```bash
$ make test
```
