from utils import get_schema_property, has_schema_property


def check_aggregation_group(row, schema, field_name, columns):
    errors = []
    if field_name != "aggregation_group":
        return errors

    sheet_aggr_group = row[columns["value_reference"]].value
    if not sheet_aggr_group:
        sheet_aggr_group = row[columns["rule_reference"]].value

    if not sheet_aggr_group:
        errors.append(
            f"Error: {field_name} - Cannot find aggregation group in sheet"
        )
        return errors

    if "," in sheet_aggr_group or "|" in sheet_aggr_group:
        return check_aggregation_group_multiple(sheet_aggr_group, schema, field_name)
    else:
        return check_aggregation_group_single(sheet_aggr_group, schema, field_name)


def clean_aggregation_group_name(aggr_group):
    sheet_aggr_group = aggr_group.strip(" ").replace(" ", "_")
    sheet_aggr_group = sheet_aggr_group.replace("-", "_")
    sheet_aggr_group = sheet_aggr_group.upper()
    return sheet_aggr_group


def clean_aggregation_group_names(aggr_group_field):
    no_brackets = aggr_group_field.replace("[", "").replace("]", "")
    no_whitespace = no_brackets.replace("\n", "")
    bars_please = no_whitespace.replace(",", "|")

    aggr_groups = bars_please.split("|")
    return [clean_aggregation_group_name(name) for name in aggr_groups]


def check_aggregation_group_single(sheet_aggr_group, schema, field_name):
    errors = []

    if not has_schema_property(schema, field_name, "const"):
        errors.append(
            f"Error: {field_name} - Cannot find aggregation group field in schema"
        )
        return errors
    schema_group_name = get_schema_property(schema, field_name, "const")

    sheet_group_name = ""
    if sheet_aggr_group:
        sheet_group_name = clean_aggregation_group_name(sheet_aggr_group)
    if sheet_group_name == "N/A":
        sheet_group_name = None

    if sheet_group_name != schema_group_name:
        errors.append(
            f"Error: {field_name} - Sheet has an (adjusted) Aggregation Group "
            f'of "{sheet_group_name}" while the JSON has "{schema_group_name}"'
        )

    return errors


def group_in_all_of(schema, group):
    group_name = group.replace("XX", "")
    if "allOf" in schema.keys():
        for all_of_rule in schema["allOf"]:
            if "required" in all_of_rule["then"]:
                if "aggregation_group" in all_of_rule["then"]["properties"]:
                    prop = all_of_rule["then"]["properties"]["aggregation_group"]
                    if "const" in prop and prop["const"] == group_name:
                        return True
                    if "pattern" in prop and group_name in prop["pattern"]:
                        return True
    return False


def check_aggregation_group_multiple(sheet_aggr_group, schema, field_name):
    errors = []

    schema_group_names = get_schema_property(schema, field_name, "enum")
    if not schema_group_names:
        errors.append(
            f"Error: {field_name} - Cannot find aggregation groups field in schema"
        )
        return errors

    sheet_group_names = None
    if sheet_aggr_group:
        sheet_group_names = clean_aggregation_group_names(sheet_aggr_group)

    for sheet_group_name in sheet_group_names:
        in_all_of = group_in_all_of(schema, sheet_group_name)
        if sheet_group_name not in schema_group_names and not in_all_of:
            errors.append(
                f'    Error: {field_name} - Sheet has a group "{sheet_group_name}" '
                "that is missing in the schema"
            )

    for schema_group_name in schema_group_names:
        if schema_group_name not in sheet_group_names:
            errors.append(
                f'    Error: {field_name} - Schema has a group "{schema_group_name}" '
                f"that is not found in the sheet"
            )

    return errors
