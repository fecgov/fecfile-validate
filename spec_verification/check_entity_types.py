from utils import get_schema_property


def check_entity_type(row, schema, field_name, columns):
    errors = []
    if field_name != "entity_type":
        return errors

    entity_types = row[columns["value_reference"]].value
    if not entity_types:
        errors.append(f"    Error: {field_name} - Entity Types not found in sheet")
        return errors

    clean_entity_types = entity_types.replace("[", "").replace("]", "")

    if "|" in clean_entity_types or "," in clean_entity_types:
        return check_multiple_entity_types(schema, field_name, clean_entity_types)
    else:
        return check_single_entity_type(schema, field_name, clean_entity_types)


def check_single_entity_type(schema, field_name, raw_sheet_entity_type):
    errors = []
    json_entity_type = get_schema_property(schema, field_name, "const")
    if not json_entity_type:
        errors.append(
            f"    Error: {field_name} - The sheet has a single entity type"
            " but the JSON does not have a constant value"
        )
        return errors

    sheet_entity_type = raw_sheet_entity_type.replace(" Only", "").replace(" only", "")

    if sheet_entity_type != json_entity_type:
        errors.append(
            f"    Error: {field_name} - The sheet has an entity type of"
            f" {sheet_entity_type}, but the JSON has {json_entity_type}"
        )
    return errors


def check_multiple_entity_types(schema, field_name, raw_sheet_entity_types):
    errors = []
    json_entity_types = get_schema_property(schema, field_name, "enum")
    if not json_entity_types:
        errors.append(
            f"    Error: {field_name} - The sheet has a single entity type"
            " but the JSON does not have an enumerated value"
        )
        return errors

    cleaned_sheet_entity_types = raw_sheet_entity_types.replace("[", "").replace(
        "]", ""
    )
    cleaner_entity_types = cleaned_sheet_entity_types.replace(" ", "").replace(",", "|")
    sheet_entity_types = cleaner_entity_types.split("|")

    for s_entity in sheet_entity_types:
        if s_entity not in json_entity_types:
            errors.append(
                f'    Error: {field_name} - The sheet has an entity type "{s_entity}"'
                " that is not present in the JSON's entity type"
            )

    for j_entity in json_entity_types:
        if j_entity not in sheet_entity_types:
            errors.append(
                f'    Error: {field_name} - The JSON has an entity type "{j_entity}"'
                " that is not present in the Sheet's entity type"
            )

    return errors