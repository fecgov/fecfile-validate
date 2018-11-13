from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Committee
from .serializers import CommitteeSerializer
import json
import os
from django.views.decorators.csrf import csrf_exempt
import logging
import datetime
import magic
from django.http import JsonResponse

# Create your views here.
# Exception handling is taken care to validate the committeinfo
logger = logging.getLogger(__name__)
# validate api for Form 99


@api_view(['POST'])
def validate_f99(data.json):
    # # get all comm info
    # if request.method == 'GET':
    #     comm_info = CommitteeInfo.objects.all()
    #     serializer = CommitteeInfoSerializer(comm_info, many=True)
    #     return Response(serializer.data)

    # insert a new record for a comm_info
    if request.method == 'POST':
        with open('data.json') as f:
            data = json.load(f)
            data = {
                'committeeid': data.get('committeeid'),
                'committeename': data.get('committeename'),
                'street1': data.get('street1'),
                'street2': data.get('street2'),
                'city': data.get('city'),
                'state': data.get('state'),
                'text': data.get('text'),
                'reason': data.get('reason'),
                'zipcode': data.get('zipcode'),
                'treasurerlastname': data.get('treasurerlastname'),
                'treasurerfirstname': data.get('treasurerfirstname'),
                'treasurermiddlename': data.get('treasurermiddlename'),
                'treasurerprefix': data.get('treasurerprefix'),
                'treasurersuffix': data.get('treasurersuffix'),
                'email_on_file': data.get('email_on_file'),
                'file': data.get('file'),
            }
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:        
        comm = Committee.objects.get(committeeid=request.data.get('committeeid'))

    except Committee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    errormess = []

    if comm.committeename!=data.get('committeename'):
        errormess.append('Committee Name does not match the Form 1 data.')
        
    if comm.street1!=data.get('street1'):
        errormess.append('Street1 does not match the Form 1 data.')
            
    if 'street2' in data and comm.street2!=data.get('street2'):
        errormess.append('Street2 does not match the Form 1 data.')
        
    if comm.city != data.get('city'):
        errormess.append('City does not match the Form 1 data.')

    if comm.state != data.get('state'):
        errormess.append('State does not match the Form 1 data.')

    if comm.zipcode != int(data.get('zipcode')):
        errormess.append('Zipcode does not match the Form 1 data.')

    if comm.treasurerlastname != data.get('treasurerlastname'):
        errormess.append('Treasurer Last Name does not match the Form 1 data.')

    if comm.treasurerfirstname != data.get('treasurerfirstname'):
        errormess.append(
            'Treasurer First Name does not match the Form 1 data.')

    if 'treasurermiddlename' in data and comm.treasurermiddlename != data.get('treasurermiddlename'):
        errormess.append(
            'Treasurer Middle Name does not match the Form 1 data.')

    if 'treasurerprefix' in data and comm.treasurerprefix != data.get('treasurerprefix'):
        errormess.append('Treasurer Prefix does not match the Form 1 data.')

    if 'treasurersuffix' in data and comm.treasurersuffix != data.get('treasurersuffix'):
        errormess.append('Treasurer Suffix does not match the Form 1 data.')

    if len(data.get('text')) > 20000:
        errormess.append('Text greater than 20000.')

    if len(data.get('text')) == 0:
        errormess.append('Text field is empty.')

    conditions = [data.get('reason') == 'MST', data.get('reason') == 'MSM', data.get('reason') == 'MSI', data.get('reason') == 'MSW']
    if not any(conditions):
        errormess.append('Reason does not match the pre-defined codes.')

    # pdf validation for type, extension and size
    if 'file' in data:
        valid_mime_types = ['application/pdf']
        file = data.get('file')
        file_mime_type = magic.from_buffer(file.read(1024), mime=True)
        if file_mime_type not in valid_mime_types:
            errormess.append(
                'This is not a pdf file type. Kindly open your document using a pdf reader before uploading it.')
        valid_file_extensions = ['.pdf']
        ext = os.path.splitext(file.name)[1]
        if ext.lower() not in valid_file_extensions:
            errormess.append(
                'Unacceptable file extension. Only files with .pdf extensions are accepted.')
        if file._size > 33554432:
            errormess.append(
                'The File size is more than 32 MB. Kindly reduce the size of the file before you upload it.')    
            
    if len(errormess)==0:
        errormess.append('Validation successful!')
        return JsonResponse(errormess, status=200, safe=False)
    else:
        return JsonResponse(errormess, status=400, safe=False)
