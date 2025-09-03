import json


INDENTATION_WIDTH=4


def format_html(string, indentation_level=0):
	return f"{' '*INDENTATION_WIDTH*indentation_level}{string}\n"


def get_spec_links(file_name):
	return {
		"json": f"https://github.com/fecgov/fecfile-validate/blob/develop/schema/{file_name}.json",
		"doc": f"{file_name}.html",
		"spec": f"{file_name}_spec.html",
	}


def gen_html_for_link_specs(file_name):
	spec_links = get_spec_links(file_name)
	output_str = ""
	for spec_type in spec_links.keys():
		spec_link = spec_links[spec_type]

		output_str += format_html('<td>', 2)
		output_str += format_html(f'<div class="link"><a href="{spec_link}" target="_blank" rel="noopener">{spec_type}</a></div>', 3)
		output_str += format_html('</td>', 2)

	return output_str


def build_html_for_head():
	output_str = format_html("<head>")
	output_str += format_html('<link rel=stylesheet type=text/css href="https://fonts.googleapis.com/css?family=Overpass:300,400,600,800">', 1)
	output_str += format_html('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin=anonymous></script>', 1)
	output_str += format_html('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin=anonymous></script>', 1)
	output_str += format_html('<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel=stylesheet integrity=sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T crossorigin=anonymous>', 1)
	output_str += format_html('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"	integrity=sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM crossorigin=anonymous></script>', 1)
	output_str += format_html('<link rel=stylesheet type=text/css href=schema_doc.css>', 1)
	output_str += format_html('<link rel=stylesheet type=text/css href=spec_table.css>', 1)
	output_str += format_html('<script src=schema_doc.min.js></script>', 1)
	output_str += format_html('<meta charset=utf-8>', 1)
	output_str += format_html('<title>FEC Form Data Dictionaries</title>', 1)
	output_str += format_html("</head>")
	return output_str


def build_html_for_schema_category(schema_map, category):
	category_map = schema_map[category]

	output_str = format_html(f"<h5>{category_map["title"]}</h5>")
	output_str += format_html('<table style="width: 50%">')
	output_str += format_html(f'<caption>{category_map["caption"]}</caption>', 1)
	output_str += format_html('<tr>', 1)
	output_str += format_html(f'<th>{category_map["file_type"]}</th>', 2)
	output_str += format_html('<th>Description</th>', 2)
	output_str += format_html('<th>JSON</th>', 2)
	output_str += format_html('<th>DOC</th>', 2)
	output_str += format_html('<th>Specification</th>', 2)
	output_str += format_html('</tr>', 1)
	for TTI in category_map["files"].keys():
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
		output_str += gen_html_for_link_specs(file_name)
		output_str += format_html('</tr>', 1)
	output_str += '</table>\n'

	return output_str


def gen_index_dot_html():
	schema_map_file = open("schema_map.json", "r")
	schema_map = json.load(schema_map_file)
	output_file = open("../docs/index.html", "w")

	output_file.write(
		format_html('<!DOCTYPE html>\n<html lang=en>\n')
	)

	output_file.write(build_html_for_head())

	output_file.write(
		format_html('\n<body>\n<h2>FEC Form Data Dictionaries</h2>\n<hr>\n')
	)

	for schema_category in schema_map.keys():
		output_file.write(
			build_html_for_schema_category(schema_map, schema_category)
		)

	output_file.write(
		format_html('</body>\n\n</html>')
	)


if __name__ == "__main__":
	gen_index_dot_html()