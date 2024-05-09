from utils import get_length_from_type, get_schema_property


def check_contribution_amount(row, schema, field_name, columns):
    errors = []

    if field_name != "contribution_amount":
        return errors

    sheet_form_type = row[columns["type"]].value
    expected_length = get_length_from_type(sheet_form_type)
    if not expected_length:
        return errors

    sheet_rule_reference = row[columns["rule_reference"]].value
    sheet_amount_negative = False
    if sheet_rule_reference is not None:
        sheet_amount_negative = "negative" in sheet_rule_reference.lower()

    json_minimum = get_schema_property(schema, field_name, "minimum")
    json_maximum = get_schema_property(schema, field_name, "maximum")
    json_exclusive_maximum = get_schema_property(schema, field_name, "exclusiveMaximum")

    if json_minimum is None:
        errors.append(
            f"Error: {field_name} - The JSON for the field has no minimum value"
        )
    elif json_minimum != 0 and len(str(json_minimum)) != expected_length:
        errors.append(
            f"Error: {field_name} - The JSON's minimum value "
            f"is {json_minimum} when it should have a length of 12"
        )

    if not sheet_amount_negative:
        if json_maximum is None:
            errors.append(
                f"Error: {field_name} - The JSON for the field "
                f"has no maximum value"
            )
        elif len(str(json_maximum)) != expected_length:
            errors.append(
                f"Error: {field_name} - The JSON's maximum value "
                f"is {json_maximum} when it should have a length of 12"
            )
    else:
        if json_exclusive_maximum is None:
            errors.append(
                f"Error: {field_name} - The JSON for "
                f"the field has no exclusiveMaximum value"
            )
        elif json_exclusive_maximum != 0:
            errors.append(
                f"Error: {field_name} - The JSON's "
                f"exclusiveMaximum should equal 0"
            )

    return errors
