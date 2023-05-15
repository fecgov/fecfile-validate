def get_schema_property(schema, field_name, property, is_fec_spec=False):
    if field_name in schema["properties"]:
        field = schema["properties"][field_name]
        if is_fec_spec:
            field = field["fec_spec"]

        if property in field.keys():
            return field[property]
        else:
            return None

def get_length_from_type(type):
    if not type:
        return None

    split_type = type.split("-")
    if len(split_type) <= 1:
        return None

    return int(split_type[-1].strip(" "))
