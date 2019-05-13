import json
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE
import re
import csv
import copy
from decimal import Decimal
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
    except Exception as e:
        raise Exception('check_null_value function is throwing an error: ' + str(e))
        
def length(value):
    try:
        if value in None:
            return 0
        else:
            return len(value)
    except Exception as e:
        raise Exception('length function is throwing an error: ' + str(e))
"""
************************************************* Functions to check the type of the field *******************************************************************
"""        
def alpha_numeric(value):
    try:
        if len(value) > 1:
            return not bool(re.match('^[a-zA-Z0-9]([ ]*[a-zA-Z0-9])+$', value))
        else:
            return not bool(re.match('^[a-zA-Z0-9]+$', value))
    except Exception as e:
        raise Exception('alpha_numeric function is throwing an error: ' + str(e))

def alpha_numeric_underscore(value):
    try:
        if len(value) > 1:
            return not bool(re.match('^[a-zA-Z0-9]([ ]*[a-zA-Z0-9_])+$', value))
        else:
            return not bool(re.match('^[a-zA-Z0-9]+$', value))
    except Exception as e:
        raise Exception('alpha_numeric_underscore function is throwing an error: ' + str(e))

def alpha(value):
    try:
        return not bool(re.match('^[a-zA-Z]+$', value))
    except Exception as e:
        raise Exception('alpha function is throwing an error: ' + str(e))

def numeric(value):
    try:
        return not bool(re.match('^[0-9]+$', value))
    except Exception as e:
        raise Exception('numeric function is throwing an error: ' + str(e))

def amount(value):
    try:
        return not bool(re.match('^[0-9.]+$', value))
    except Exception as e:
        raise Exception('amount function is throwing an error: ' + str(e))

"""
************************************************* Function used to find the file based on the transactionTypeCode *******************************************************************
"""
def json_file_name(transactionTypeCode):
    try:
        list_SA_transactionTypeCode = ["INDV_REC"]
        if transactionTypeCode in list_SA_transactionTypeCode:
            file_name = 'api/rules/15.json'            
        else:
            string = ''
            for item in list_SA_transactionTypeCode:
                string += item + ", "
            raise Exception('transactionTypeCode for now should be limited to '+ string[:-2])
        return file_name
    except Exception as e:
        raise Exception('json_file_name function is throwing an error: ' + str(e))

"""
************************************************* Function used to define the json format of the individual error/warning message *******************************************************************
"""
def error_json_template(message_type, message, field_name, transaction_id, field_value):
    try:
        errormessage = message_type + "Message"
        errornumber = message_type + "Number"
        output_dict = {errormessage: message,
                        errornumber: "not yet implemented",
                        "tranId": transaction_id,
                        "fieldName": field_name,
                        "fieldValue": field_value}
        return output_dict
    except Exception as e:
        raise Exception('error_json_template function is throwing an error: ' + str(e))

"""
************************************************* Function which validates all the rules for form F99 using csv file *******************************************************************
"""
def func_validate(field_lists, data):
    try:
        errors_list = []
        warnings_list = []
        special_list = []
        str_field_not_in_json = " field is not provided"
        str_field_not_in_format = " field is not in the format of "
        str_field_not_length = " field should not be greater than "

        for field_list in field_lists:
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
                if field_list[1] == 'NUM':
                    if numeric(data.get(field_list[0])):
                        str_output = field_list[0] + str_field_not_in_format + field_list[1]
                        temp_list.append(str_output)
                if field_list[1] == 'AMT':
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
    except Exception as e:
        raise Exception('func_validate function is throwing an error: ' + str(e))

"""
************************************************* Function which validates all the rules for form F3x using json files *******************************************************************
"""
def func_json_validate(data):
    try:
        file_name = json_file_name(data.get('transactionTypeCode'))
        with open(file_name) as json_file:
            load_json = json.load(json_file)
            rules = copy.deepcopy(load_json)    
        output = {'errors': [], 'warnings': []}
        for rule in rules:
            for field_name, field_rule in rule.items():
                transaction_id = data.get('transactionId')

                if field_name in data and check_null_value(data.get(field_name)):
                    type_error_flag = False
                    if field_rule.get('field_type') == 'A/N':
                        if alpha_numeric(data.get(field_name)):
                            type_error_flag = True
                    if field_rule.get('field_type') == 'A/N_':
                        if alpha_numeric_underscore(data.get(field_name)):
                            type_error_flag = True
                    if field_rule.get('field_type') == 'A':
                        if alpha(data.get(field_name)):
                            type_error_flag = True
                    if field_rule.get('field_type') == 'NUM':
                        if numeric(data.get(field_name)):
                            type_error_flag = True
                    if field_rule.get('field_type') == 'AMT':
                        if amount(data.get(field_name)):
                            type_error_flag = True

                    if type_error_flag:
                        message = field_name + " field is not in " + field_rule.get('field_type') + " format"
                        message_type = "error"                
                        dict_temp = error_json_template(message_type, message, field_name, transaction_id, data.get(field_name))
                        output['errors'].append(dict_temp)
                        
                    if len(field_rule.get('value_check'))> 0:
                        if not data.get(field_name) in field_rule.get('value_check'):
                            error_string = ''
                            for value in field_rule.get('value_check'):
                                error_string += value + ", "
                            message = field_name + " field is not within the following acceptable values: [" + error_string[:-2] + "]"
                            message_type = "error"
                            dict_temp = error_json_template(message_type, message, field_name, transaction_id, data.get(field_name))
                            output['errors'].append(dict_temp)

                    if len(data.get(field_name)) > int(field_rule.get('field_size')):
                        message = field_name + " field has "+ str(len(data.get(field_name))) + " characters. Maximum expected characters are " + field_rule.get('field_size')
                        message_type = "error"
                        dict_temp = error_json_template(message_type, message, field_name, transaction_id, data.get(field_name))
                        output['errors'].append(dict_temp)

                else:
                    if field_rule.get('message_type') in ["error", "warning"]:
                        if not check_null_value(field_rule.get('additional_validation_key')):
                            validation_error_flag =  True
                            message = field_name + " field is missing"
                            message_type = field_rule.get('message_type')
                        else:
                            validation_error_flag = False
                            key = field_rule.get('additional_validation_key')
                            value = field_rule.get('additional_validation_value')
                            operator = field_rule.get('additional_validation_operator')
                            if key in data and check_null_value(data.get(key)):
                                if operator == ">":
                                    print("yup...yup" + field_name)                            
                                    if Decimal(data.get(key)) > Decimal(value):
                                        print("validate SUCCESS")
                                        validation_error_flag =  True
                                        message = field_name + " field is mandatory as " + key + " " + operator + " " + value
                                        message_type = "error"
                        if validation_error_flag:
                            dict_temp = error_json_template(message_type, message, field_name, transaction_id, "none")
                            if message_type == "error":
                                output['errors'].append(dict_temp)
                            else:
                                output['warnings'].append(dict_temp)
        return output

    except Exception as e:
        raise Exception('func_json_validate function is throwing an error: ' + str(e))

"""
******************************************************************************************************************************
VALIDATE API - SPRINT 8 - FNE 452 - BY PRAVEEN JINKA
******************************************************************************************************************************
"""
@app.route('/v1/validate', methods=['POST'])
def validate():

    try:
        if not 'form_type' in request.form:
            raise Exception('form_type input parameter is missing in request body')
            # error = json.dumps({'errors': ['Form Type parameter missing in request body']})
            # return json_response(error, 400)
        try:
            if 'json_validate' in request.files:
                json_data = request.files['json_validate']
                json_data.seek(0)
                json_data = json_data.read()
            else:
                raise Exception('json_validate input parameter is missing in request body')
                # error = json.dumps({'errors': ['validate parameter missing in request body']})
                # return json_response(error, 400)
            data = json.loads(json_data.decode("utf-8"))
        except Exception as e:
            raise Exception('Error while loading JSON file attachment on json_validate input parameter: ' + str(e))
            # error = json.dumps({'Error': 'Error while loading JSON file attachment on validate parameter. Error received: ' + str(e)})
            # return json_response(error, 400)

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

        """
        ************************************************* FORM F3X Valdation Rules *******************************************************************
        """
        if request.form.get('form_type') == "F3X":
            schedule_lists = ['SA']       
            for schedule_list in schedule_lists: 
                if 'schedules' in data.get('data') and data.get('data').get('schedules'):
                    if schedule_list in data.get('data').get('schedules') and data.get('data').get('schedules').get(schedule_list):
                        if len(data.get('data').get('schedules').get(schedule_list)) > 0:
                            for sa in data.get('data').get('schedules').get(schedule_list):
                                output = func_json_validate(sa)
                                errors.extend(output.get('errors'))
                                warnings.extend(output.get('warnings'))
                                if 'child' in sa and sa.get('child'):
                                    if len(sa.get('child')) > 0:
                                        for ch in sa.get('child'):
                                            child_output = func_json_validate(ch)
                                            errors.extend(child_output.get('errors'))
                                            warnings.extend(child_output.get('warnings'))
            result = {} 
            result['committeeId'] = data.get('data').get('committeeId')
            result['form_type'] = request.form.get('form_type')
            result['submissionId'] = 'Not yet Implemented'
            result['totalErrors'] = len(errors)
            result['totalWarnings'] = len(warnings)
            if len(errors) > 0:
                result['status'] = "VALIDATION FAILED"
            else:
                result['status'] = "VALIDATION SUCCESS"

        if request.form.get('form_type') == "F99":
            error = json.dumps({'headers': data.get('header'),
                                'errors': output.get('errors'),
                                'warnings': output.get('warnings')})
        else:                
            error = json.dumps({'result': result,
                                'errors': errors,
                                'warnings': warnings})
        return json_response(error,200)

    except Exception as e:
            error = json.dumps({'errors': 'validate API is throwing an error: '+str(e)})
            return json_response(error, 400)

"""
******************************************************************************************************************************
END - VALIDATE API
******************************************************************************************************************************
"""
