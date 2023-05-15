def clean_form_types(raw_form_type):
    no_or = raw_form_type.replace(" or ", "|")
    no_whitespace = no_or.replace(" ", "").replace("\n", ",")
    no_quotes = no_whitespace.replace('"', "")
    no_brackets = no_quotes.replace("[", "").replace("]", "")
    if "," in no_brackets:
        return no_brackets.split(",")
    if "|" in no_brackets:
        return no_brackets.split("|")
    return [no_brackets]


def check_form_type(row, schema, field_name, columns):
    errors = []
    if field_name not in ["form_type", "back_reference_sched_name"]:
        return errors

    form_type_values = row[columns["value_reference"]].value
    if not form_type_values:
        form_type_values = row[columns["sample_data"]].value
    if not form_type_values:
        errors.append(f"    Error: {field_name} - No form types found in sheet")
        return errors

    form_types = clean_form_types(form_type_values)
    schema_properties = schema["properties"][field_name]

    for form_type in form_types:
        if "const" in schema_properties.keys():
            if form_type.upper() != schema_properties["const"].upper():
                errors.append(
                    f"    Error: {field_name} - Sheet has Form Type "
                    f'"{form_type}" while the JSON has "{schema_properties["const"]}"'
                )

        elif "enum" in schema_properties.keys():
            if form_type.upper() not in [x.upper() for x in schema_properties["enum"]]:
                errors.append(
                    f"    Error: {field_name} - Sheet has Form Type "
                    f'"{form_type}" while the JSON has "{schema_properties["enum"]}"'
                )

    return errors