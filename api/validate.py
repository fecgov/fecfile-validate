import json
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE


app = Flask(__name__)

"""
************************************************* Functions to check if fields exist in JSON *******************************************************************
"""
def check_form_type(data):
    if 'form_type' in data and data.get('form_type'):
        if len(data.get('form_type')) == 3:
            return True, "Success"
    return False, "form_type"

def check_committee_id(data):
    if 'committeeid' in data and data.get('committeeid'):
        if len(data.get('committeeid')) == 9:
            return True, "Success"
    return False, "committeeid"

def check_committee_name(data):
    if 'committeename' in data and data.get('committeename'):
        if len(data.get('committeename')) <= 200:
            return True, "Success"
    return False, "committeename"

def check_street1(data):
    if 'street1' in data and data.get('street1'):
        if len(data.get('street1')) <= 34:
            return True, "Success"
    return False, "street1"

def check_street2(data):
    if 'street2' in data and data.get('street2'):
        if len(data.get('street2')) > 34:
            return False, "street2"
    return True, "Success"

def check_city(data):
    if 'city' in data and data.get('city'):
        if len(data.get('city')) <= 30:
            return True, "Success"
    return False, "city"

def check_state(data):
    if 'state' in data and data.get('state'):
        if len(data.get('state')) == 2:
            if not any(char.isdigit() for char in data.get('state')):
                return True, "Success"
    return False, "state"

def check_zipcode(data):
    if 'zipcode' in data and data.get('zipcode'):
        if len(data.get('zipcode')) == 5 or len(data.get('zipcode')) == 9:
            return True, "Success"
    return False, "zipcode"

def check_treasurer_last_name(data):
    #null values are being taken care of
    if 'treasurerlastname' in data and data.get('treasurerlastname'):
        if len(data.get('treasurerlastname')) <= 30:
            return True, "Success"
    return False, "treasurerlastname"

def check_treasurer_first_name(data):
    if 'treasurerfirstname' in data and data.get('treasurerfirstname'):
        if len(data.get('treasurerfirstname')) <= 20:
            return True, "Success"
    return False, "treasurerfirstname"

def check_treasurer_middle_name(data):
    if 'treasurermiddlename' in data and data.get('treasurermiddlename'):
        if len(data.get('treasurermiddlename')) > 20:
            return False, "treasurermiddlename"
    return True, "Success"

def check_treasurer_prefix(data):
    if 'treasurerprefix' in data and data.get('treasurerprefix'):
        if len(data.get('treasurerprefix')) > 10:
            return False, "treasurerprefix"
    return True, "Success" 

def check_treasurer_suffix(data):
    if 'treasurersuffix' in data and data.get('treasurersuffix'):
        if len(data.get('treasurersuffix')) > 10:
            return False, "treasurersuffix"
    return True, "Success" 

def check_date_signed(data):
    if 'datesigned' in data and data.get('datesigned'):
        if len(data.get('datesigned')) == 8:
            if data.get('datesigned').isdigit():
                return True, "Success"
        return False, "datesigned"
    return True, "Success"

def check_f99_reason_type(data):
    f99_reason_list = ["MSI", "MST", "MSM", "MSW"]
    if 'reason' in data and data.get('reason'):
        if not (data.get('reason') in f99_reason_list):
            return False, "reason"
    return True, "Success"

def check_text(data):
    if 'text' in data and data.get('text'):
        if len(data.get('text')) > 20000:
            return False, "text"
    return True, "Success"

def check_attachment_extension(data):
    if 'hasAttachment' in data and data.get('hasAttachment'):
        if data.get('hasAttachment'):
            if 'attachmentName' in data and data.get('attachmentName'):
                if data.get('attachmentName').endswith('.pdf'):
                    return True, "Success"
            return False, "attachment"
    return True, "Success"


"""
************************************************* Functions to check Cha *******************************************************************
"""

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
        data = json.loads(json_data.decode("utf-8"))
    errors = []
    error_message = " is required"
    warnings = []
    warnings_message = " is expected but not required"

    """
    ************************************************* FORM 99 Valdation Rules *******************************************************************
    """
    if request.form.get('form_type') == "F99":

        status, message = check_form_type(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_committee_id(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_committee_name(data.get('data'))
        if not status:
            warnings.append(message)

        status, message = check_street1(data.get('data'))
        if not status:
            warnings.append(message)

        status, message = check_street2(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_city(data.get('data'))
        if not status:
            warnings.append(message)

        status, message = check_state(data.get('data'))
        if not status:
            warnings.append(message)

        status, message = check_zipcode(data.get('data'))
        if not status:
            warnings.append(message)

        status, message = check_treasurer_last_name(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_treasurer_first_name(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_treasurer_middle_name(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_treasurer_prefix(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_treasurer_suffix(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_date_signed(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_f99_reason_type(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_text(data.get('data'))
        if not status:
            errors.append(message)

        status, message = check_attachment_extension(data.get('data'))
        if not status:
            errors.append(message)

        """
        ************************************************* END - FORM 99 Valdation Rules *******************************************************************
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
******************************************************************************************************************************
END - VALIDATE API
******************************************************************************************************************************
"""
