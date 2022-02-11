from pyexpat import model
from django.shortcuts import render
from rest_framework.generics import *
from .models import Client
from .serializator import *



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