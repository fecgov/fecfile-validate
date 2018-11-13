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
def validate_f99(request):
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
                'committeeid': request.data.get('committeeid'),
                'committeename': request.data.get('committeename'),
                'street1': request.data.get('street1'),
                'street2': request.data.get('street2'),
                'city': request.data.get('city'),
                'state': request.data.get('state'),
                'text': request.data.get('text'),
                'reason' :request.data.get('reason'),
                'zipcode': request.data.get('zipcode'),
                'treasurerlastname': request.data.get('treasurerlastname'),
                'treasurerfirstname': request.data.get('treasurerfirstname'),
                'treasurermiddlename': request.data.get('treasurermiddlename'),
                'treasurerprefix': request.data.get('treasurerprefix'),
                'treasurersuffix': request.data.get('treasurersuffix'),
                'email_on_file' : request.data.get('email_on_file'),
                'file': request.data.get('file'),
            }
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:        
        comm = Committee.objects.get(committeeid=request.data.get('committeeid'))

    except Committee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    errormess = []

    if comm.committeename!=request.data.get('committeename'):
        errormess.append('Committee Name does not match the Form 1 data.')
        
    if comm.street1!=request.data.get('street1'):
        errormess.append('Street1 does not match the Form 1 data.')
            
    if 'street2' in request.data and comm.street2!=request.data.get('street2'):
        errormess.append('Street2 does not match the Form 1 data.')
        
    if comm.city!=request.data.get('city'):
        errormess.append('City does not match the Form 1 data.')
            
    if comm.state!=request.data.get('state'):
        errormess.append('State does not match the Form 1 data.')
    
    if comm.zipcode!=int(request.data.get('zipcode')):
        errormess.append('Zipcode does not match the Form 1 data.')

    if comm.treasurerlastname!=request.data.get('treasurerlastname'):
        errormess.append('Treasurer Last Name does not match the Form 1 data.')
            
    if comm.treasurerfirstname!=request.data.get('treasurerfirstname'):
        errormess.append('Treasurer First Name does not match the Form 1 data.')
        
    if 'treasurermiddlename' in request.data and comm.treasurermiddlename!=request.data.get('treasurermiddlename'):
        errormess.append('Treasurer Middle Name does not match the Form 1 data.')
        
    if 'treasurerprefix' in request.data and comm.treasurerprefix!=request.data.get('treasurerprefix'):
        errormess.append('Treasurer Prefix does not match the Form 1 data.')
        
    if 'treasurersuffix' in request.data and comm.treasurersuffix!=request.data.get('treasurersuffix'):
        errormess.append('Treasurer Suffix does not match the Form 1 data.')
        
    if len(request.data.get('text'))>20000:
        errormess.append('Text greater than 20000.')

    if len(request.data.get('text'))==0:
        errormess.append('Text field is empty.')
        
    conditions = [request.data.get('reason')=='MST', request.data.get('reason')=='MSM', request.data.get('reason')=='MSI', request.data.get('reason')=='MSW']
    if not any(conditions):
        errormess.append('Reason does not match the pre-defined codes.')
    
    #pdf validation for type, extension and size
    if 'file' in request.data:
        valid_mime_types = ['application/pdf']
        file = request.data.get('file')
        file_mime_type = magic.from_buffer(file.read(1024), mime=True)
        if file_mime_type not in valid_mime_types:
            errormess.append('This is not a pdf file type. Kindly open your document using a pdf reader before uploading it.')
        valid_file_extensions = ['.pdf']
        ext = os.path.splitext(file.name)[1]
        if ext.lower() not in valid_file_extensions:
            errormess.append('Unacceptable file extension. Only files with .pdf extensions are accepted.')
        if file._size > 33554432:
            errormess.append('The File size is more than 32 MB. Kindly reduce the size of the file before you upload it.')    
            
    if len(errormess)==0:
        errormess.append('Validation successful!')
        return JsonResponse(errormess, status=200, safe=False)
    else:
        return JsonResponse(errormess, status=400, safe=False)
