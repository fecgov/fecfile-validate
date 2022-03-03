import subprocess


def test_generates_table():
    proc = subprocess.run(
        ['python3', 'bin/generate-spec-table.py', 'schema/F3X.json'],
        capture_output=True)
    output = proc.stdout.decode("utf-8")
    assert proc.stderr.decode("utf-8") == ""
    assert output.startswith("<!DOCTYPE html>")
