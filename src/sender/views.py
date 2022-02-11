from pyexpat import model
from django.shortcuts import render
from rest_framework.generics import *
from .models import Client
from .serializator import *




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