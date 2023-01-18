from openpyxl import load_workbook
import json
from os import path


COLUMNS = {
	"property_name": 0,
	"type": 1,
	"required": 2,
	"value_reference": 4
}


def get_sheet_name(sheet):
	if sheet['F6'].value == None:
		return ""

	return sheet['F6'].value

def get_schema_fields(sheet):
	name_overrides = {
		'contribution_purpose_description': 'contribution_purpose_descrip',
		'memo_text/description': 'memo_text_description',
		'contributor_organization': 'contributor_organization_name',
		'contributor_street__1': 'contributor_street_1',
		'contributor_street__2': 'contributor_street_2',
	}

	skipped_fields = [
		'receipt_description',
	]

	fields = {}
	row = 4
	while sheet['A'+str(row)].value:
		field_name_raw = sheet['A'+str(row)].value.lower()
		field_name = '_'.join(field_name_raw.split(' '))
		if field_name in name_overrides:
			field_name = name_overrides[field_name]

		if field_name[-1] == "_":
			field_name = field_name[:-1]

		if field_name not in skipped_fields:
			fields[field_name] = row

		row+=1

	return fields

def get_schema_property(schema, field_name, property, FEC_spec=False):
	field = schema['properties'][field_name]
	if FEC_spec:
		field = field['fec_spec']

	return field[property]

def compare_type(row, schema, field_name):
	expected_type = row[COLUMNS['type']].value
	actual_type = get_schema_property(schema, field_name, 'TYPE', FEC_spec=True)

	if expected_type == None:
		match = True
	else:
		expected_type = expected_type.strip(' ') ##Strips the lingering spaces present in some fields of the spreadsheet
		match = (expected_type == actual_type)

	if not match:
		return f'    Error: {field_name}, {expected_type}, {actual_type}'

def compare_required(row, schema, field_name):
	sheet_required_raw = row[COLUMNS['required']].value
	schema_required_raw = get_schema_property(schema, field_name, 'REQUIRED', True)
	schema_required_list = schema['required']
	
	if sheet_required_raw == None:
		sheet_required = False
	else:
		sheet_required = "X (error)" in sheet_required_raw

	if schema_required_raw == None:
		schema_required = False
	else:
		schema_required = "X (error)" in schema_required_raw

	if sheet_required != schema_required:
		return f'    Error: {field_name}, {sheet_required_raw}, {schema_required_raw}'

	if sheet_required and not field_name in schema_required_list:
		foundInAllOf = False
		if (schema['allOf']):
			for allOfRule in schema['allOf']:
				if field_name in allOfRule['then']['required']:
					foundInAllOf = True; break

		if not foundInAllOf:
			return f'    Error: {field_name} not in required list'

def verify(sheet, schema):
	errors = []
	comparisons = [
		compare_type,
		compare_required,
	]

	fields = get_schema_fields(sheet)
	for field in fields.keys():
		row = sheet[str(fields[field])]
		for comparison_function in comparisons:
			error = comparison_function(row, schema, field)
			if error != None:
				errors.append(error)
	
	return errors

if (__name__ == "__main__"):
	workbook = load_workbook('spec.xlsx')
	sheets = workbook._sheets

	for sheet in sheets:
		name = get_sheet_name(sheet)
		if not name:
			continue

		schema_file_path = '../schema/'+name+'.json'
		if not path.exists(schema_file_path):
			continue

		json_file = open(schema_file_path, 'r')
		if not json_file:
			continue

		schema = json.load(json_file)
		if not schema:
			continue

		##if name != 'INDIVIDUAL_RECEIPT':
		##	continue

		errors = verify(sheet, schema)
		if (len(errors) > 0):
			print(name)
			for error in errors:
				print(error)
			print('\n')