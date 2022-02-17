import subprocess


def test_generate_starter_schema():
    fec_format_proc = subprocess.run(
        ['python3',
         'bin/generate-starter-schema.py',
         'schema/backlog/FEC_Format_v8.3.0.1.xlsx',
         '--sheets-to-generate=bin/sheets-to-generate.json'
         ], capture_output=True)
    assert fec_format_proc.stderr.decode("utf-8") == ""
    contacts_proc = subprocess.run(
        ['python3',
         'bin/generate-starter-schema.py',
         'schema/backlog/Contacts_Specs\ -\ Revised.xlsx'
         ], capture_output=True)
    assert contacts_proc.stderr.decode("utf-8") == ""
