import subprocess

version = "8.5"


def test_generates_table():
    proc = subprocess.run(
        [
            "python3",
            "bin/generate-spec-table.py",
            f"schema/{version}/OTHER_RECEIPT.json",
        ],
        capture_output=True,
    )
    output = proc.stdout.decode("utf-8")
    assert proc.stderr.decode("utf-8") == ""
    assert output.startswith("<!DOCTYPE html>")
