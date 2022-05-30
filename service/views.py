from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from service.models import *
from .serializers import InformationSerializer

@api_view(['GET'])
def getData(request):
     information = Information.objects.all()
     serializer = InformationSerializer(information, many=True)
     return Response(serializer.data)

@api_view(['post'])
def addPerson(request):
     serializer = InformationSerializer(data=request.data)
     if serializer.is_valid():
          serializer.save()
     return Response(serializer.data)