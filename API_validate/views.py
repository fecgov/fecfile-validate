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
import requests


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
        #incoming_file = requests.get(request.data.get('upload'))
        import ipdb; ipdb.set_trace()
        f99_obj = json.loads(request.data['upload'])        
        #return JsonResponse({'success':'Data validated!'}, status=200, safe=False)
        
        #with open('data.json') as f:            
        data = {
            'committeeid': f99_obj.get('committeeid'),
            'committeename': f99_obj.get('committeename'),
            'street1': f99_obj.get('street1'),
            'street2': f99_obj.get('street2'),
            'city': f99_obj.get('city'),
            'state': f99_obj.get('state'),
            'text': f99_obj.get('text'),
            'reason' :f99_obj.get('reason'),
            'zipcode': f99_obj.get('zipcode'),
            'treasurerlastname': f99_obj.get('treasurerlastname'),
            'treasurerfirstname': f99_obj.get('treasurerfirstname'),
            'treasurermiddlename': f99_obj.get('treasurermiddlename'),
            'treasurerprefix': f99_obj.get('treasurerprefix'),
            'treasurersuffix': f99_obj.get('treasurersuffix'),
            'email_on_file' : f99_obj.get('email_on_file'),
            'file': f99_obj.get('file'),
        }
            
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:        
        comm = Committee.objects.get(committeeid=f99_obj.get('committeeid'))

    except Committee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    errormess = []

    if comm.committeename!=f99_obj.get('committeename'):
        errormess.append('Committee Name does not match the Form 1 data.')
        
    if comm.street1!=f99_obj.get('street1'):
        errormess.append('Street1 does not match the Form 1 data.')
            
    if 'street2' in request.data and comm.street2!=f99_obj.get('street2'):
        errormess.append('Street2 does not match the Form 1 data.')
        
    if comm.city!=f99_obj.get('city'):
        errormess.append('City does not match the Form 1 data.')
            
    if comm.state!=f99_obj.get('state'):
        errormess.append('State does not match the Form 1 data.')
    
    if comm.zipcode!=int(f99_obj.get('zipcode')):
        errormess.append('Zipcode does not match the Form 1 data.')

    if comm.treasurerlastname!=f99_obj.get('treasurerlastname'):
        errormess.append('Treasurer Last Name does not match the Form 1 data.')
            
    if comm.treasurerfirstname!=f99_obj.get('treasurerfirstname'):
        errormess.append('Treasurer First Name does not match the Form 1 data.')
        
    if 'treasurermiddlename' in request.data and comm.treasurermiddlename!=f99_obj.get('treasurermiddlename'):
        errormess.append('Treasurer Middle Name does not match the Form 1 data.')
        
    if 'treasurerprefix' in request.data and comm.treasurerprefix!=f99_obj.get('treasurerprefix'):
        errormess.append('Treasurer Prefix does not match the Form 1 data.')
        
    if 'treasurersuffix' in request.data and comm.treasurersuffix!=f99_obj.get('treasurersuffix'):
        errormess.append('Treasurer Suffix does not match the Form 1 data.')
        
    if len(f99_obj.get('text'))>20000:
        errormess.append('Text greater than 20000.')

    if len(f99_obj.get('text'))==0:
        errormess.append('Text field is empty.')
        
    # conditions = [f99_obj.get('reason')=='MST', f99_obj.get('reason')=='MSM', f99_obj.get('reason')=='MSI', f99_obj.get('reason')=='MSW']
    # if not any(conditions):
    #     errormess.append('Reason does not match the pre-defined codes.')
        
    # #pdf validation for type, extension and size
    # if 'file' in request.data:
    #     valid_mime_types = ['application/pdf']
    #     file = f99_obj.get('file')
    #     file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    #     if file_mime_type not in valid_mime_types:
    #         errormess.append('This is not a pdf file type. Kindly open your document using a pdf reader before uploading it.')
    #     valid_file_extensions = ['.pdf']
    #     ext = os.path.splitext(file.name)[1]
    #     if ext.lower() not in valid_file_extensions:
    #         errormess.append('Unacceptable file extension. Only files with .pdf extensions are accepted.')
    #     if file._size > 33554432:
    #         errormess.append('The File size is more than 32 MB. Kindly reduce the size of the file before you upload it.')    

            

    if len(errormess)==0:
        errormess.append('Validation successful!')
        return JsonResponse(errormess, status=200, safe=False)
    else:
        return JsonResponse(errormess, status=400, safe=False)

    
