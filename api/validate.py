import json
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE
import re
import csv
import copy
from decimal import Decimal
app = Flask(__name__)

"""
************************************************* GLOBAL LISTS used *******************************************************************************************
"""
EXCLUDED_FROM_FIELD_CHECK = ['lineNumber', 'transactionTypeIdentifier', 'child']

list_SA_similar_INDV_REC = ["INDV_REC", "PARTN_MEMO", "IK_REC", "REATT_FROM", "REATT_MEMO", "RET_REC", "EAR_REC",
                            "CON_EAR_UNDEP", "CON_EAR_DEP", "IND_RECNT_REC", "IND_NP_RECNT_ACC", "IND_NP_HQ_ACC", "IND_NP_CONVEN_ACC",
                            "IND_REC_NON_CONT_ACC", "JF_TRAN_IND_MEMO", "JF_TRAN_NP_RECNT_IND_MEMO", "JF_TRAN_NP_CONVEN_IND_MEMO", 
                            "JF_TRAN_NP_HQ_IND_MEMO", "EAR_REC_RECNT_ACC", "EAR_REC_CONVEN_ACC", "EAR_REC_HQ_ACC"]
list_SA_similar_PAR_CON = ["PARTN_REC", "TRIB_REC", "TRIB_NP_RECNT_ACC", "TRIB_NP_HQ_ACC", "TRIB_NP_CONVEN_ACC", 
                            "BUS_LAB_NON_CONT_ACC", "JF_TRAN_TRIB_MEMO", "JF_TRAN_NP_RECNT_TRIB_MEMO", "JF_TRAN_NP_CONVEN_TRIB_MEMO", 
                            "JF_TRAN_NP_HQ_TRIB_MEMO"]
list_SA_similar_COND_EARM_PAC = ["EAR_MEMO", "PAC_CON_EAR_UNDEP", "PAC_CON_EAR_DEP", "PAC_EAR_REC", "PAC_EAR_MEMO", "PARTY_IK_REC", "PAC_IK_REC", "PARTY_REC", 
                                "PAC_REC", "PAC_NON_FED_REC", "PAC_NON_FED_RET", "PAC_RET", "PARTY_RET", "TRAN", "PARTY_RECNT_REC", "PAC_RECNT_REC", 
                                "TRIB_RECNT_REC", "PARTY_NP_RECNT_ACC", "PAC_NP_RECNT_ACC", 
                                "PARTY_NP_HQ_ACC", "PAC_NP_HQ_ACC", "PARTY_NP_CONVEN_ACC", "PAC_NP_CONVEN_ACC", "OTH_CMTE_NON_CONT_ACC", "IK_TRAN","IK_TRAN_FEA", 
                                "JF_TRAN", "JF_TRAN_PARTY_MEMO", "JF_TRAN_PAC_MEMO", 
                                "JF_TRAN_NP_RECNT_ACC", "JF_TRAN_NP_RECNT_PAC_MEMO", "JF_TRAN_NP_CONVEN_ACC", "JF_TRAN_NP_CONVEN_PAC_MEMO", "JF_TRAN_NP_HQ_ACC", 
                                "JF_TRAN_NP_HQ_PAC_MEMO", "EAR_REC_RECNT_ACC_MEMO", "EAR_REC_CONVEN_ACC_MEMO", "EAR_REC_HQ_ACC_MEMO"]
list_SA_similar_OFFSET = ["OFFSET_TO_OPEX"]
list_SA_similar_OTH_REC = ["OTH_REC"] 
list_SA_similar_REF_NFED_CAN = ["REF_TO_OTH_CMTE"]
list_SA_similar_REF_FED_CAN = ["REF_TO_FED_CAN"]

list_SB_similar_OP_EXP = ["OPEXP", "HQ_ACC_DIS", "CO_ACC_DIS"]
list_SB_similar_IK_OUT = ["IK_OUT"]
list_SB_similar_IK_TF_OUT = ["IK_TRAN_OUT", "IK_TRAN_FEA_OUT"]
list_SB_similar_EAR_OUT = ["CON_EAR_UNDEP_MEMO", "CON_EAR_DEP_MEMO", "PAC_CON_EAR_UNDEP_MEMO", "PAC_CON_EAR_DEP_OUT"]
list_SB_similar_IK_OUT_PTY = ["PARTY_IK_OUT", "PAC_IK_OUT"]
list_f3x_total = list_SA_similar_INDV_REC + list_SA_similar_PAR_CON + list_SB_similar_OP_EXP + list_SB_similar_IK_OUT + list_SB_similar_IK_TF_OUT + list_SB_similar_EAR_OUT + list_SA_similar_COND_EARM_PAC + list_SB_similar_IK_OUT_PTY + list_SA_similar_OFFSET + list_SA_similar_OTH_REC + list_SA_similar_REF_NFED_CAN + list_SA_similar_REF_FED_CAN

list_f3x_schedules = ['SA','SB']
dict_parent_child_association = {
                            "PARTN_REC":["PARTN_MEMO"], "IK_REC":["IK_OUT"], "REATT_FROM":["REATT_MEMO"], "EAR_REC":["EAR_MEMO"], "CON_EAR_DEP":["CON_EAR_DEP_MEMO"], 
                            "CON_EAR_UNDEP":["CON_EAR_UNDEP_MEMO"], "PARTY_IK_REC":["PARTY_IK_OUT"], 
                            "PAC_IK_REC":["PAC_IK_OUT"], "PAC_CON_EAR_DEP":["PAC_CON_EAR_DEP_OUT"], "PAC_CON_EAR_UNDEP":["PAC_CON_EAR_UNDEP_MEMO"], 
                            "PAC_EAR_REC":["PAC_EAR_MEMO"], "JF_TRAN":["JF_TRAN_PAC_MEMO", "JF_TRAN_IND_MEMO", "JF_TRAN_PARTY_MEMO", "JF_TRAN_TRIB_MEMO"], 
                            "IK_TRAN":["IK_TRAN_OUT"], "IK_TRAN_FEA":["IK_TRAN_FEA_OUT"], 
                            "JF_TRAN_NP_RECNT_ACC":["JF_TRAN_NP_RECNT_TRIB_MEMO", "JF_TRAN_NP_RECNT_IND_MEMO", "JF_TRAN_NP_RECNT_PAC_MEMO"], 
                            "JF_TRAN_NP_CONVEN_ACC":["JF_TRAN_NP_CONVEN_TRIB_MEMO", "JF_TRAN_NP_CONVEN_PAC_MEMO", "JF_TRAN_NP_CONVEN_IND_MEMO"], 
                            "JF_TRAN_NP_HQ_ACC":["JF_TRAN_NP_HQ_IND_MEMO", "JF_TRAN_NP_HQ_TRIB_MEMO", "JF_TRAN_NP_HQ_PAC_MEMO"], 
                            "EAR_REC_RECNT_ACC":["EAR_REC_RECNT_ACC_MEMO"], "EAR_REC_CONVEN_ACC":["EAR_REC_CONVEN_ACC_MEMO"], "EAR_REC_HQ_ACC":["EAR_REC_HQ_ACC_MEMO"],
                            }

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
def capital_alpha_numeric(value):
    try:
        return not bool(re.match('^[\x20-\x60\x7B-\x7D]+$', value))
    except Exception as e:
        raise Exception('capital_alpha_numeric function is throwing an error: ' + str(e))

def alpha_numeric(value):
    try:
        return not bool(re.match('^[\x20-\x7E]+$', value))
        # if len(value) > 1:
        #     return not bool(re.match('^[a-zA-Z0-9]([ ]*[a-zA-Z0-9])+$', value))
        # else:
        #     return not bool(re.match('^[a-zA-Z0-9]+$', value))
    except Exception as e:
        raise Exception('alpha_numeric function is throwing an error: ' + str(e))

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
        return not bool(re.match('^-?[0-9.]+$', str(value)))
    except Exception as e:
        raise Exception('amount function is throwing an error: ' + str(e))

def date_check(value):
    try:
        return not bool(re.match('^-?[0-9/]+$', str(value)))
    except Exception as e:
        raise Exception('amount function is throwing an error: ' + str(e))    

"""
************************************************* Function used to find the file based on the transactionTypeIdentifier *******************************************************************
"""
def json_file_name(transactionTypeIdentifier):
    try:
        error_flag = False
        file_name = 'api/rules/'        
        if transactionTypeIdentifier in list_SA_similar_INDV_REC:
            file_name += 'SA_INDV_REC.json'            
        elif transactionTypeIdentifier in list_SA_similar_PAR_CON:
            file_name += 'SA_PAR_CON.json'
        elif transactionTypeIdentifier in list_SB_similar_OP_EXP:
            file_name += 'SB_OP_EXP.json'
        elif transactionTypeIdentifier in list_SB_similar_IK_OUT:
            file_name += 'SB_IK_OUT.json'
        elif transactionTypeIdentifier in list_SB_similar_IK_TF_OUT:
            file_name += 'SB_IK_TF_OUT.json'
        elif transactionTypeIdentifier in list_SB_similar_EAR_OUT:
            file_name += 'SB_EARM_OUT.json'
        elif transactionTypeIdentifier in list_SA_similar_COND_EARM_PAC:
            file_name += 'SA_COND_EARM_PAC.json'
        elif transactionTypeIdentifier in list_SB_similar_IK_OUT_PTY:
            file_name += 'SB_IK_OUT_PTY.json'
        elif transactionTypeIdentifier in list_SA_similar_OFFSET:
            file_name += 'SA_OFFSET.json'
        elif transactionTypeIdentifier in list_SA_similar_OTH_REC:
            file_name += 'SA_OTH_REC.json'
        elif transactionTypeIdentifier in list_SA_similar_REF_NFED_CAN:
            file_name += 'SA_REF_NFED_CAN.json'
        elif transactionTypeIdentifier in list_SA_similar_REF_FED_CAN:
            file_name += 'SA_REF_FED_CAN.json'                              
        else:
            error_flag = True
            error_string = ', '.join(list_f3x_total)
            file_name = 'transactionTypeIdentifier should be limited to these values: [' + error_string + ']'
        return error_flag, file_name
    except Exception as e:
        raise Exception('json_file_name function is throwing an error: ' + str(e))

"""
************************************************* Function used to define the json format of the individual error/warning message *******************************************************************
"""
def error_json_template(message_type, message, field_name, field_value, transaction_id):
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
        transaction_id = data.get('transactionId')
        output = {'errors': [], 'warnings': []}
        # JSON file name function gathers the file name
        file_flag, file_name = json_file_name(data.get('transactionTypeIdentifier'))
        if file_flag:
            message = file_name
            message_type = "error"
            dict_temp = error_json_template(message_type, message, "transactionTypeIdentifier", data.get('transactionTypeIdentifier'), transaction_id)
            output['errors'].append(dict_temp)
        else:
            with open(file_name) as json_file:
                load_json = json.load(json_file)
                rules = copy.deepcopy(load_json)        
            for rule in rules:
                for field_name, field_rule in rule.items():
                    if field_name in data and check_null_value(data.get(field_name)):
                        type_error_flag = False
                        if field_rule.get('field_type') == 'A/N':
                            if field_name == 'transactionId':     
                                if capital_alpha_numeric(data.get(field_name)):
                                    type_error_flag = True
                            else:
                                if alpha_numeric(data.get(field_name)):
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
                        if field_rule.get('field_type') == 'DATE':
                            if date_check(data.get(field_name)):
                                type_error_flag = True

                        if type_error_flag:
                            if field_name == 'transactionId':
                                message = field_name + " field is not in " + field_rule.get('field_type') + " format. In case of alphabets, only uppercase are allowed for this field."
                            else:
                                message = field_name + " field is not in " + field_rule.get('field_type') + " format"
                            message_type = "error"                
                            dict_temp = error_json_template(message_type, message, field_name, data.get(field_name), transaction_id)
                            output['errors'].append(dict_temp)
                            
                        if len(field_rule.get('value_check'))> 0:
                            if not data.get(field_name) in field_rule.get('value_check'):
                                error_string = ', '.join(field_rule.get('value_check'))
                                message = field_name + " field is not within the following acceptable values: [" + error_string + "]"
                                message_type = "error"
                                dict_temp = error_json_template(message_type, message, field_name, data.get(field_name), transaction_id)
                                output['errors'].append(dict_temp)

                        if len(str(data.get(field_name))) > int(field_rule.get('field_size')):
                            message = field_name + " field has "+ str(len(data.get(field_name))) + " characters. Maximum expected characters are " + field_rule.get('field_size')
                            message_type = "error"
                            dict_temp = error_json_template(message_type, message, field_name, data.get(field_name), transaction_id)
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
                                        if Decimal(data.get(key)) > Decimal(value):
                                            validation_error_flag =  True
                                            message = field_name + " field is mandatory as " + key + " " + operator + " " + value
                                            message_type = "error"
                                    if operator == "IND >":
                                        if data.get('entityType') == 'IND':
                                            if Decimal(data.get(key)) > Decimal(value):
                                                validation_error_flag =  True
                                                message = field_name + " field is mandatory as " + key + " " + operator + " " + value
                                                message_type = "error"
                                    if operator == "not in":
                                        if not data.get(key) in value:
                                            validation_error_flag =  True
                                            error_value = ', '.join(value)
                                            message = field_name + " field is mandatory as " + key + " " + operator + " [" + error_value + "]"
                                            message_type = "error"
                                    if operator == "in":
                                        if data.get(key) in value:
                                            validation_error_flag =  True
                                            error_value = ', '.join(value)
                                            message = field_name + " field is mandatory as " + key + " " + operator + " [" + error_value + "]"
                                            message_type = "error"
                            if validation_error_flag:
                                dict_temp = error_json_template(message_type, message, field_name, "none", transaction_id)
                                if message_type == "error":
                                    output['errors'].append(dict_temp)
                                else:
                                    output['warnings'].append(dict_temp)
            # Code to check if there are any additional fields in the data apart from the format specs and throwing an error if there are such fields. 
            # This has to be uncommented once JSON builder is implemented based on this logic.
            for key, value in data.items():
                check_flag = True
                for rule in rules:
                    for field_name in rule:
                        if key == field_name or key in EXCLUDED_FROM_FIELD_CHECK:
                            check_flag = False
                    if not check_flag:
                        break
                if check_flag:
                    message = key + " field is not expected for this transaction type code: " + data.get('transactionTypeIdentifier')
                    message_type = "error"
                    field_dict_temp = error_json_template(message_type, message, key, "none", transaction_id)
                    output['errors'].append(field_dict_temp)

        return output
    except Exception as e:
        raise Exception('func_json_validate function is throwing an error: ' + str(e))

def child_validation(parent, list_parent):
    try:
        output = {"errors": [], "warnings": []}
        # validating if the transactionTypeIdentifier of a transaction can be a valid parent based on the established parent child relationships defined in dict_parent_child_association
        if parent.get('transactionTypeIdentifier') in list_parent:
            for ch in parent.get('child'):
                # validatiing if the child transactionTypeIdentifier is a part established parent child relationships for the respective parent transactionTypeIdentifier
                if not ch.get('transactionTypeIdentifier') in dict_parent_child_association.get(parent.get('transactionTypeIdentifier')):
                    child_transaction_codes_string = ', '.join(dict_parent_child_association.get(parent.get('transactionTypeIdentifier')))
                    message = ch.get('transactionTypeIdentifier') + " transaction type cannot be a child of "+ parent.get('transactionTypeIdentifier') + " as per rules in dict_parent_child_association dictionary definition. Expected values are: [" + child_transaction_codes_string + "]"
                    message_type = "error"
                    dict_temp = error_json_template(message_type, message, "transactionTypeIdentifier", ch.get('transactionTypeIdentifier'), ch.get('transactionId'))
                    output['errors'].append(dict_temp)
                # validating if child backReferenceTransactionIdNumber is same as parent transactionId
                if ch.get('backReferenceTransactionIdNumber') != parent.get('transactionId'):
                    message = "Child backReferenceTransactionIdNumber field should match parent transactionId:"+ parent.get('transactionId')
                    message_type = "error"
                    dict_temp = error_json_template(message_type, message, "backReferenceTransactionIdNumber", ch.get('backReferenceTransactionIdNumber'), ch.get('transactionId'))
                    output['errors'].append(dict_temp)                                   
                child_output = func_json_validate(ch)
                output['errors'].extend(child_output.get('errors'))
                output['warnings'].extend(child_output.get('warnings'))
        else:
            message = parent.get('transactionTypeIdentifier') + " transaction type cannot have a child transaction as per rules in dict_parent_child_association dictionary definition"
            message_type = "error"
            dict_temp = error_json_template(message_type, message, "transactionTypeIdentifier", parent.get('transactionTypeIdentifier'), parent.get('transactionId'))
            output['errors'].append(dict_temp)
        return output
    except Exception as e:
        raise Exception('child_validation function is throwing an error: ' + str(e))
        
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
        forms_list = ['F99', 'F3X']
        if not request.form.get('form_type') in forms_list:
            error_string = ', '.join(forms_list)
            raise Exception('form_type input parameter can only have the following values: [' + error_string + ']. Input Received: ' + request.form.get('form_type'))
        try:
            if 'json_validate' in request.files:
                json_data = request.files['json_validate']
                json_data.seek(0)
                json_data = json_data.read()
            else:
                raise Exception('json_validate input parameter is missing in request body')
            data = json.loads(json_data.decode("utf-8"))
        except Exception as e:
            raise Exception('Error while loading JSON file attachment on json_validate input parameter: ' + str(e))

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
            list_parent= []
            for parent, child in dict_parent_child_association.items():
                list_parent.append(parent)
            for schedule_list in list_f3x_schedules: 
                if 'schedules' in data.get('data') and data.get('data').get('schedules'):
                    if schedule_list in data.get('data').get('schedules') and data.get('data').get('schedules').get(schedule_list):
                        if len(data.get('data').get('schedules').get(schedule_list)) > 0:
                            for sa in data.get('data').get('schedules').get(schedule_list):
                                output = func_json_validate(sa)
                                errors.extend(output.get('errors'))
                                warnings.extend(output.get('warnings'))
                                if 'child' in sa and sa.get('child'):
                                    if len(sa.get('child')) > 0:
                                        # Child Transactions validations in function child_output function
                                        child_output = child_validation(sa, list_parent)
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
