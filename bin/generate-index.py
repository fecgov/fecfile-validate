import argparse
import json
import os


INDENTATION_WIDTH = 4
EXCLUDED_FILES = [
    "_OVERRIDE_SchC2.json",
    "_OVERRIDE_F99.json",
    "UNIT_TEST.json"
]


def get_schema_map() -> dict:
    if not os.path.isfile("../schema_map.json"):
        raise FileNotFoundError("schema_map.json not found")

    schema_map_file = open("../schema_map.json", "r")
    schema_map = json.load(schema_map_file)
    schema_map_file.close()

    return schema_map


# Returns a dict of file names with every value set to False
# Used to track whether or not a file is referenced by the schema map
def get_schema_files() -> dict:
    schema_files = {}
    for f in os.listdir():
        if f[-5:] == ".json" and f not in EXCLUDED_FILES:
            schema_files[f] = False

    return schema_files


def get_options() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=""
        "Generates the validator documentation's index.html based on schema_map.json"
    )
    parser.add_argument(
        "-t", "--test", help="Disables saving results to a file", action="store_true"
    )
    parser.add_argument(
        "-w", "--ignore-warnings", help="Ignore warnings", action="store_true"
    )
    return parser.parse_args()


def format_html(string, indentation_level=0):
    return f"{' '*INDENTATION_WIDTH*indentation_level}{string}\n"


def get_spec_links(file_name):
    return {
        "json": f"https://github.com/fecgov/fecfile-validate/blob/develop/schema/{file_name}.json",  # noqa: E501
        "doc": f"{file_name}.html",
        "spec": f"{file_name}_spec.html",
    }


def gen_html_for_link_specs(file_name, schema_files, invalid_links):
    spec_links = get_spec_links(file_name)

    json_link = f"{file_name}.json"
    if json_link in schema_files.keys():
        schema_files[json_link] = True
    else:
        spec_links["json"] = None
        invalid_links.append(file_name)

    output_str = ""
    for spec_type in spec_links.keys():
        spec_link = spec_links[spec_type]

        output_str += format_html('<td>', 2)
        if spec_link is not None:
            output_str += format_html(f'<div class="link"><a href="{spec_link}" target="_blank" rel="noopener">{spec_type}</a></div>', 3)  # noqa: E501
        else:
            output_str += format_html('<div class="link">WARNING: FILE NOT FOUND</div>')
        output_str += format_html('</td>', 2)

    return output_str


def build_html_for_head():
    output_str = format_html("<head>")
    output_str += format_html('<link rel=stylesheet type=text/css href="https://fonts.googleapis.com/css?family=Overpass:300,400,600,800">', 1)  # noqa: E501
    output_str += format_html('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin=anonymous></script>', 1)  # noqa: E501
    output_str += format_html('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin=anonymous></script>', 1)  # noqa: E501
    output_str += format_html('<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel=stylesheet integrity=sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T crossorigin=anonymous>', 1)  # noqa: E501
    output_str += format_html('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"    integrity=sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM crossorigin=anonymous></script>', 1)  # noqa: E501
    output_str += format_html('<link rel=stylesheet type=text/css href=schema_doc.css>', 1)  # noqa: E501
    output_str += format_html('<link rel=stylesheet type=text/css href=spec_table.css>', 1)  # noqa: E501
    output_str += format_html('<script src=schema_doc.min.js></script>', 1)
    output_str += format_html('<meta charset=utf-8>', 1)
    output_str += format_html('<title>FEC Form Data Dictionaries</title>', 1)
    output_str += format_html("</head>")
    return output_str


def build_html_for_schema_category(schema_map, category, schema_files, invalid_links):
    category_map = schema_map[category]

    style = category_map.get("style", None)
    if style is not None:
        style_string = f'style="{style}"'
    else:
        style_string = ""

    output_str = format_html(f"<h5>{category_map["title"]}</h5>")
    output_str += format_html(f'<table {style_string}>')
    output_str += format_html(f'<caption>{category_map["caption"]}</caption>', 1)
    output_str += format_html('<tr>', 1)
    output_str += format_html(f'<th>{category_map["file_type"]}</th>', 2)
    output_str += format_html('<th>Description</th>', 2)
    output_str += format_html('<th>JSON</th>', 2)
    output_str += format_html('<th>DOC</th>', 2)
    output_str += format_html('<th>Specification</th>', 2)
    output_str += format_html('</tr>\n', 1)
    for TTI in category_map["files"].keys():  # noqa: N806
        value = category_map["files"][TTI]
        if value is None:
            file_name = TTI
            subtitle = ""
        elif value.__class__ is str:
            file_name = value
            subtitle = ""
        else:
            file_name = value.get("filename", "")
            subtitle = value.get("subtitle", "")

        output_str += format_html('<tr>', 1)
        output_str += format_html(f'<td>{TTI}</td>', 2)
        output_str += format_html(f'<td>{subtitle}</td>', 2)
        output_str += gen_html_for_link_specs(file_name, schema_files, invalid_links)
        output_str += format_html('</tr>\n', 1)

    output_str = output_str[:-1]  # strip off last newline
    output_str += '</table>\n'

    return output_str


def gen_html(schema_map, schema_files, invalid_links):
    html_for_head = build_html_for_head()
    html_for_body = ""
    for schema_category in schema_map.keys():
        html_for_body += build_html_for_schema_category(
            schema_map,
            schema_category,
            schema_files,
            invalid_links
        )
    return [html_for_head, html_for_body]


def write_to_file(html_body, html_head):
    output_file = open("../docs/index.html", "w")

    output_file.write(
        format_html('<!DOCTYPE html>\n<html lang=en>\n')
    )

    output_file.write(html_head)

    output_file.write(
        format_html('\n<body>\n<h2>FEC Form Data Dictionaries</h2>\n<hr>\n')
    )

    output_file.write(html_body)

    output_file.write(
        format_html('</body>\n\n</html>')
    )
    output_file.close()


def evaluate_run_status(schema_files, invalid_links):
    warnings = []
    found_files = 0
    missing_files = 0

    for file_name in schema_files.keys():
        if not schema_files[file_name]:
            warnings.append(
                f"WARNING - Json schema file not included in schema map: {file_name}"
            )
            missing_files += 1
        else:
            found_files += 1

    for file_name in invalid_links:
        warnings.append(
            f"WARNING - Broken link in schema map - file doesn't exist: {file_name}.json"
        )

    return {
        "warnings": warnings,
        "found_files": found_files,
        "missing_files": missing_files
    }


def print_status(message, value, width):
    print(
        "  -",
        message.ljust(width),
        str(value).rjust(3)
    )

def print_status_messages(schema_files, status, invalid_links, width):
    print_status("Files present in schema directory:", len(schema_files.keys()) + len(EXCLUDED_FILES), width)  # noqa: E501
    print_status("Files excluded from search:", len(EXCLUDED_FILES), width)
    print_status("Files found in schema map:", status['found_files'], width)
    print_status("Files missing from schema map:", status['missing_files'], width)
    print_status("Invalid links in Schema Map:", len(invalid_links), width)
    print()  # Empty line for readability


def gen_index_dot_html():
    options = get_options()
    schema_map = get_schema_map()
    schema_files = get_schema_files()
    invalid_links = []

    print("Generating index.html ...\n")
    print()

    html_for_head, html_for_body = gen_html(schema_map, schema_files, invalid_links)

    status = evaluate_run_status(schema_files, invalid_links)
    
    for warning in status["warnings"]:
        print(warning)
    if len(status["warnings"]) > 0:
        print()

    print_status_messages(schema_files, status, invalid_links, 36)

    if len(status["warnings"]) > 0:
        if not options.ignore_warnings:
            raise RuntimeError(f"Failed to generate index.html: {len(status['warnings'])} warnings")  # noqa: E501
        else:
            print(f"Ignored {len(status['warnings'])} warnings ...")

    if not options.test:
        print("Saving index.html ...")
        write_to_file(html_for_head, html_for_body)
        print("Saved successfully\n")
    else:
        print("Skipped saving index.html\n")

    print("Successfully generated index.html")


if __name__ == "__main__":
    gen_index_dot_html()
