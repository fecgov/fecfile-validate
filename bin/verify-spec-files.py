from openpyxl import load_workbook
import json
from os import path

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


def verify(sheet, schema):
	fields = get_schema_fields(sheet)
	for field in fields.keys():
		row = sheet[str(fields[field])]
		rowStr = field
		for cell in row:
			rowStr += ', '
			rowStr += str(cell.value)
		print(rowStr)
	
	return True

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

		if name != 'INDIVIDUAL_RECEIPT':
			continue

		if not verify(sheet, schema):
			print(name, "does not match!")
