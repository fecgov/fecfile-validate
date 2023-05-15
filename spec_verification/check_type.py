from utils import get_schema_property

def check_type(row, schema, field_name, columns):
    errors = []
    expected_type = row[columns["type"]].value
    actual_type = get_schema_property(schema, field_name, "TYPE", is_fec_spec=True)

    if expected_type is None:
        match = True
    else:
        # Strips the lingering spaces present in some fields of the spreadsheet
        expected_type = expected_type.strip(" ")
        match = expected_type == actual_type

    if not match:
        errors.append(
            f"    Error: {field_name} - Sheet has Type {expected_type} "
            f"and the JSON has {actual_type}"
        )

    return errors