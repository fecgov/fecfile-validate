from utils import get_schema_property


def check_sample_data(row, schema, field_name, columns):
    errors = []
    sheet_sample_data = row[columns["sample_data"]].value
    schema_sample_data = get_schema_property(schema, field_name, "SAMPLE_DATA", True)
    if sheet_sample_data != schema_sample_data:
        errors.append(
            f"    Minor Error: {field_name} - The Sheet has Sample Data of "
            f'"{sheet_sample_data}" while the JSON has "{schema_sample_data}"'
        )

    return errors