import subprocess

def test_generates_table():
    proc = subprocess.run(['python3', 'bin/generate-spec-table.py', 'schema/F3X.json'], capture_output=True)
    out = proc.stdout.decode("utf-8")
    assert out.startswith("<!DOCTYPE html>")
    assert out.endswith("<</table></body></html>>")
