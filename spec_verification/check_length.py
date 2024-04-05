import re
from utils import get_schema_property, get_length_from_type


def get_cpd_lengths_and_patterns(regex):
    lengths = []
    patterns = regex.split("|")
    for pattern in patterns:
        split_left = pattern.split("[")
        split_right = pattern.split("}")

        fixed = []
        if len(split_left) > 1:
            fixed.append(split_left[0])
        if len(split_right) > 1:
            fixed.append(split_right[1])

        # Right of the "[" we find the "[ -~]{min_length,max_length}$" pattern
        length_str = split_left[-1]

        # Finding the maximum length of abritrary characters in the pattern
        length_str = length_str.split(",")[1]  # Right of the comma aaaaand
        max_length = length_str.split("}")[0]  # left of the brace is the max length

        length = 0
        # Remove the ^, &, \\, (, and ) symbols since they're not part of the length
        # Count the length of escaped parens!
        for f in fixed:
            fix = f.strip("^").strip("$")
            length += fix.count("\\)") + fix.count("\\(")
            fix = fix.replace("\\", "").replace("(", "").replace(")", "")
            length += len(fix)

        lengths.append([length + int(max_length), pattern])

    return lengths


def check_length(row, schema, field_name, columns):
    errors = []

    # These are recurring patterns whose lengths are very hard to measure with a function
    # Instead, the fields corresponding to the keys here are considered as matching if
    # their pattern matches the value below
    committee_id_pattern = "^(?:[PC][0-9]{8}|[HS][0-9]{1}[A-Z]{2}[0-9]{5})$"
    fixed_patterns = {
        "filer_committee_id_number": committee_id_pattern,
        "donor_committee_fec_id": committee_id_pattern,
        "beneficiary_committee_fec_id": committee_id_pattern,
        "beneficiary_candidate_fec_id": committee_id_pattern,
        "contribution_date": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "expenditure_date": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        "election_code": "^[GPRSCEO]\\d{4}$",
    }

    field_type = row[columns["type"]].value
    expected_length = get_length_from_type(field_type)
    if not expected_length:
        return errors

    json_max_length = get_schema_property(schema, field_name, "maxLength")
    json_pattern_regex = get_schema_property(schema, field_name, "pattern")

    if json_max_length and json_max_length != expected_length:
        errors.append(
            f"    Error: {field_name} - Sheet has Type {field_type} but "
            f"the JSON's max_length is {json_max_length}"
        )

    if json_pattern_regex:
        if field_name in ["contribution_purpose_descrip", "expenditure_purpose_descrip"]:
            lengths_and_patterns = get_cpd_lengths_and_patterns(json_pattern_regex)
            for pattern_length, pattern in lengths_and_patterns:
                if expected_length != pattern_length:
                    # Phrase the error different depending on whether or not
                    # it is a sub-pattern
                    substring = "field's pattern's"
                    if len(lengths_and_patterns) > 0:
                        substring = f"field has a sub-pattern ({pattern}) whose"

                    errors.append(
                        f"    Error: {field_name} - Sheet has Type {field_type} but "
                        f"the JSON {substring} length adds up to {pattern_length}"
                    )
        elif field_name not in fixed_patterns.keys():
            if not re.search(f"{expected_length}}}\\$$", json_pattern_regex):
                errors.append(
                    f"    Error: {field_name} - Sheet has Type {field_type} but "
                    f"the JSON field's pattern's max length is wrong "
                    f"({json_pattern_regex})"
                )
        else:
            if json_pattern_regex != fixed_patterns[field_name]:
                errors.append(
                    f"    Error: {field_name} - The JSON has a pattern of "
                    f"{json_pattern_regex} "
                    f"but the expected pattern is {fixed_patterns[field_name]}"
                )

    return errors
