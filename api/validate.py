import json
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE


app = Flask(__name__)

"""
************************************************* Functions to check if fields exist in JSON *******************************************************************
"""
def check_form_type(data):
    if 'formType' in data:
        if len(data.get('formType')) == 3:
            return True, "Success"
    return False, "formType"

def check_committee_id(data):
    if 'committeeId' in data:
        if len(data.get('committeeId')) == 9:
            return True, "Success"
    return False, "committeeId"

def check_committee_name(data):
    if 'committeeName' in data:
        if len(data.get('committeeName')) <= 200:
            return True, "Success"
    return False, "committeeName"

def check_street1(data):
    if 'street1' in data:
        if len(data.get('street1')) <= 34:
            return True, "Success"
    return False, "street1"

def check_street2(data):
    if 'street2' in data:
        if len(data.get('street2')) > 34:
            return False, "street2"
    return True, "Success"

def check_city(data):
    if 'city' in data:
        if len(data.get('city')) <= 30:
            return True, "Success"
    return False, "city"

def check_state(data):
    if 'state' in data:
        if len(data.get('state')) == 2:
            if not any(char.isdigit() for char in data.get('state')):
                return True, "Success"
    return False, "state"

def check_zipcode(data):
    if 'zipCode' in data:
        if len(data.get('zipCode')) == 5 or len(data.get('zipCode')) == 9:
            return True, "Success"
    return False, "zipCode"

def check_treasurer_last_name(data):
    if 'treasurerLastName' in data:
        if len(data.get('treasurerLastName')) <= 30:
            return True, "Success"
    return False, "treasurerLastName"

def check_treasurer_first_name(data):
    if 'treasurerFirstName' in data:
        if len(data.get('treasurerFirstName')) <= 20:
            return True, "Success"
    return False, "treasurerFirstName"

def check_treasurer_middle_name(data):
    if 'treasurerMiddleName' in data:
        if len(data.get('treasurerMiddleName')) > 20:
            return False, "treasurerMiddleName"
    return True, "Success"

def check_treasurer_prefix(data):
    if 'treasurerPrefix' in data:
        if len(data.get('treasurerPrefix')) > 10:
            return False, "treasurerPrefix"
    return True, "Success" 

def check_treasurer_suffix(data):
    if 'treasurerSuffix' in data:
        if len(data.get('treasurerSuffix')) > 10:
            return False, "treasurerSuffix"
    return True, "Success" 

def check_date_signed(data):
    if 'dateSigned' in data:
        if len(data.get('dateSigned')) == 8:
            if data.get('dateSigned').isdigit():
                return True, "Success"
        return False, "dateSigned"
    return True, "Success"

def check_f99_reason_type(data):
    f99_reason_list = ["MSI", "MST", "MSM", "MSW"]
    if 'f99ReasonType' in data:
        if not (data.get('f99ReasonType') in f99_reason_list):
            return False, "f99ReasonType"
    return True, "Success"

def check_text(data):
    if 'text' in data:
        if len(data.get('data')) > 20000:
            return False, "text"
    return True, "Success"

def check_attachment_extension(data):
    if 'hasAttachment' in data:
        if data.get('hasAttachment'):
            if 'attachmentName' in data:
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
            json_data = request.files.get('json_validate').read()
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
