import json
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE
import re
import csv


app = Flask(__name__)

"""
************************************************* Functions to check if fields exist in JSON *******************************************************************
"""
def check_null_value(check_value):
    try:
        if check_value in ["none", "null", " ", ""]:
            return None
        else:
            return check_value
    except:
        raise
        
def length(value):
    try:
        if value in None:
            return 0
        else:
            return len(value)
    except:
        raise
        
def alpha_numeric(value):
    return not bool(re.match('^[a-zA-Z0-9]([ ]*[a-zA-Z0-9])+$', value))

def alpha(value):
    return not bool(re.match('^[a-zA-Z]+$', value))

def numeric(value):
    return not bool(re.match('^[0-9]+$', value))

def amount(value):
    return not bool(re.match('^[0-9.]+$', value))

def func_validate(field_list, data):

    errors_list = []
    warnings_list = []
    special_list = []
    str_field_not_in_json = " field is not provided"
    str_field_not_in_format = " field is not in the format of "
    str_field_not_length = " field should not be greater than "

    for field_list in field_list:
        temp_list = []
        if field_list[0] in data and check_null_value(data.get(field_list[0])):
            if field_list[1] == 'A/N':
                if alpha_numeric(data.get(field_list[0])):
                    str_output = field_list[0] + str_field_not_in_format + field_list[1]
                    temp_list.append(str_output)
            if field_list[1] == 'A':
                if alpha(data.get(field_list[0])):
                    str_output = field_list[0] + str_field_not_in_format + field_list[1]
                    temp_list.append(str_output)
            if field_list[1] == 'N':
                if numeric(data.get(field_list[0])):
                    str_output = field_list[0] + str_field_not_in_format + field_list[1]
                    temp_list.append(str_output)
            if field_list[1] == 'Amt':
                if amount(data.get(field_list[0])):
                    str_output = field_list[0] + str_field_not_in_format + field_list[1]
                    temp_list.append(str_output)

            if len(data.get(field_list[0])) > int(field_list[2]):
                str_output = field_list[0] + str_field_not_length + field_list[2]
                temp_list.append(str_output)
        else:
            str_output = field_list[0] + str_field_not_in_json
            temp_list.append(str_output)

        if field_list[3] == 'error':
            errors_list = errors_list + temp_list
        elif field_list[3] == 'warning':
            warnings_list = warnings_list + temp_list

    output = {'errors': errors_list,
                'warnings': warnings_list}
    return output

"""
******************************************************************************************************************************
VALIDATE API - SPRINT 8 - FNE 452 - BY PRAVEEN JINKA
******************************************************************************************************************************
"""
@app.route('/v1/validate', methods=['POST'])
def validate():

    # if request.content_type != JSON_MIME_TYPE:
    #     error = json.dumps({'error': 'Invalid Content Type'})
    #     return json_response(error, 400)

    if not 'form_type' in request.form:
        error = json.dumps({'errors': ['Form Type parameter missing in request body']})
        return json_response(error, 400)
    try:
        if 'json_validate' in request.files:
            json_data = request.files['json_validate']
            json_data.seek(0)
            json_data = json_data.read()
        else:
            error = json.dumps({'errors': ['validate parameter missing in request body']})
            return json_response(error, 400)
        data = json.loads(json_data.decode("utf-8"))
    except Exception as e:
        error = json.dumps({'errors': ['Error while loading JSON file attachment on validate parameter']})
        return json_response(error, 400)

    errors = []
    error_message = " is required"
    warnings = []
    warnings_message = " is expected but not required"

    """
    ************************************************* FORM 99 Valdation Rules *******************************************************************
    """
    if request.form.get('form_type') == "F99":
        with open('api/rules/F99.csv') as csvfile:
            fields = []
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                fields.append(row)
        output = func_validate(fields, data.get('data'))

    if request.form.get('form_type') == "F3X":
        schedule_lists = ['SA']
        final_output = {}
        for schedule_list in schedule_lists:
            final_output['schedules'] = {} 
            if schedule_list in data.get('data').get('schedules') and len(data.get('data').get('schedules').get(schedule_list)) > 0:
                final_output['schedules'][schedule_list] = []
                file_name = 'api/rules/' + schedule_list + '.csv'
                with open(file_name) as csvfile:
                    fields = []
                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        fields.append(row)
                for sa in data.get('data').get('schedules').get(schedule_list):
                    output = func_validate(fields, sa)                    
                    if 'child' in sa and len(sa.get('child')) > 0:
                        output['child'] = []
                        for ch in sa.get('child'):
                            child_output = func_validate(fields, ch)
                            if len(child_output.get('errors')) > 0 or len(child_output.get('warnings')) > 0:
                                child_output['transaction_id'] = ch.get('transactionId')
                                output['child'].append(child_output)
                    if len(output.get('errors')) > 0 or len(output.get('warnings')) > 0 or len(output.get('child')) > 0:
                        output['transaction_id'] = sa.get('transactionId')
                        final_output['schedules'][schedule_list].append(output)

        
        """
        ************************************************* END - FORM 99 Valdation Rules *******************************************************************
        """
        """
        if len(errors) == 0 and len(warnings) == 0:
            error = json.dumps({})
            return json_response(error,200)

        elif len(errors) > 0 and len(warnings) == 0:
            error = json.dumps({'errors': errors})
            return json_response(error,400)
        
        elif len(errors) == 0 and len(warnings) > 0:
            error = json.dumps({'warnings': warnings})
            return json_response(error,400)

        else:
            error = json.dumps({'errors': errors, 'warnings': warnings})
            return json_response(error,400)
        """
        if request.form.get('form_type') == "F99":
            error = json.dumps({'headers': data.get('header'),
                                'errors': output.get('errors'),
                                'warnings': output.get('warnings')})
            return json_response(error,200)
        else:
            error = json.dumps({'headers': data.get('header'),
                                'data': final_output})
            return json_response(error,200)


"""
******************************************************************************************************************************
END - VALIDATE API
******************************************************************************************************************************
"""
