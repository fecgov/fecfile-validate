from utils import get_schema_property

def check_transaction_type_identifier(row, schema, field_name, columns):
    errors = []
    if field_name != "transaction_type_identifier":
        return errors

    sheet_tti = row[columns["rule_reference"]].value
    if not sheet_tti:
        errors.append(
            f"    Error: {field_name} - The sheet's Transaction Type "
            + "Identifier is blank"
        )
        return errors

    if "\n" in sheet_tti:
        sheet_tti = sheet_tti.split("\n")
        return check_multi_tti(schema, field_name, sheet_tti)
    else:
        return check_single_tti(schema, field_name, sheet_tti)


def check_single_tti(schema, field_name, sheet_tti):
    errors = []
    json_tti = get_schema_property(schema, field_name, "const")
    if not json_tti:
        errors.append(
            f'    Error: {field_name} - Schema has a TTI of "{sheet_tti}"'
            " while the JSON does not have a constant value"
        )
    elif json_tti != sheet_tti:
        errors.append(
            f'    Error: {field_name} - Schema has a TTI of "{sheet_tti}"'
            f' while the JSON has "{json_tti}"'
        )
    return errors


def check_multi_tti(schema, field_name, sheet_tti):
    errors = []
    json_tti = get_schema_property(schema, field_name, "enum")
    if not json_tti:
        errors.append(
            f"    Error: {field_name} - Schema allows for TTI's of {sheet_tti}"
            " while the JSON does not have an enumerated value"
        )
    else:
        for j_tti in json_tti:
            if j_tti not in sheet_tti:
                errors.append(
                    f'    Error: {field_name} - The JSON has a TTI of "{j_tti}"'
                    " that is not present in the sheet"
                )
        for s_tti in sheet_tti:
            if s_tti != "" and s_tti not in json_tti:
                errors.append(
                    f'    Error: {field_name} - The Sheet has a TTI of "{s_tti}"'
                    " that is not present in the JSON"
                )
    return errors
