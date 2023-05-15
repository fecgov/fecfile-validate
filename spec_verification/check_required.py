from utils import get_schema_property


def check_required(row, schema, field_name, columns):
    sheet_required_raw = row[columns["required"]].value
    if sheet_required_raw is not None:
        sheet_required = sheet_required_raw.strip()

        if sheet_required == "X (error)":
            return check_strictly_required(schema, field_name)

        if sheet_required == "X (conditional error)":
            return check_conditionally_required(schema, field_name)

    return check_not_required(schema, field_name)


def check_strictly_required(schema, field_name):
    errors = []
    schema_required = get_schema_property(
        schema, field_name, "REQUIRED", is_fec_spec=True
    )

    if schema_required != "X (error)":
        errors.append(
            f"    Error: {field_name} - The field is required, "
            'but the JSON\'s FEC Spec does not have "X (error)"'
        )

    if field_name not in schema["required"]:
        errors.append(
            f"    Error: {field_name} - The field is required, "
            "but it's not present in the JSON's required array"
        )

    return errors


def found_in_all_of(schema, field_name):
    if "allOf" in schema.keys():
        for all_of_rule in schema["allOf"]:
            if "required" in all_of_rule["then"]:
                if field_name in all_of_rule["then"]["required"]:
                    return True
    return False


def check_conditionally_required(schema, field_name):
    errors = []
    schema_required = get_schema_property(
        schema, field_name, "REQUIRED", is_fec_spec=True
    )

    if schema_required != "X (conditional error)":
        errors.append(
            f"    Error: {field_name} - The field is conditionally required, "
            'but the JSON\'s FEC Spec does not have "X (conditional error)"'
        )

    if field_name in schema["required"]:
        errors.append(
            f"    Error: {field_name} - The field is conditionally required, "
            "but it is present in the JSON's required array"
        )

    if not found_in_all_of(schema, field_name):
        errors.append(
            f"    Error: {field_name} - The field is conditionally required, "
            "but it is not present in the JSON's allOf rules"
        )

    return errors


def check_not_required(schema, field_name):
    errors = []
    schema_required = get_schema_property(
        schema, field_name, "REQUIRED", is_fec_spec=True
    )

    if schema_required is not None:
        errors.append(
            f"    Error: {field_name} - The field is not required, "
            f'but it\'s marked as "{schema_required}" in the JSON'
        )

    if field_name in schema["required"]:
        errors.append(
            f"    Error: {field_name} - The field is not required,"
            " but it's present in the JSON's required array"
        )

    if found_in_all_of(schema, field_name):
        errors.append(
            f"    Error: {field_name} - The field is not required,"
            " but it can be set as required in the JSON's AllOf"
        )

    return errors
