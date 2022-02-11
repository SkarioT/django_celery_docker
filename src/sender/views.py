from pyexpat import model
from django.shortcuts import render
from rest_framework.generics import *

from .models import Client
from .serializator import *

from rest_framework.views import APIView
from rest_framework.response import Response



#for Client
class ClientView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClienCreate (CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClientUpdate (UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClientDelete (DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClienSerializator


# for Send out
class Send_outView(ListAPIView):
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_outCreate (CreateAPIView):
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_outUpdate (UpdateAPIView):
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_outDelete (DestroyAPIView):
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Message_Info_View(APIView):
    def get(self,*args, **kwargs):
        queryset = MessageInfo.objects.all().order_by("status")

        # serializer_class = MessageInfoSerializator(queryset,many=True)
        serializer_class = MessageInfoGROUPSerializator(queryset,many=True)

 
        return Response(serializer_class.data)