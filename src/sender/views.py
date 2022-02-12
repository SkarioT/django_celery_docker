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
    """
    Список всех рассылок
    """
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


class Send_outDetails (RetrieveAPIView):
    """
    получения детальной статистики отправленных сообщений по конкретной рассылке
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_out_Details_Serializator


class Message_Info_View(ListAPIView):
    """
    группировка всех сообщений по статусам
    """
    queryset = MessageInfo.objects.all()[:1]
    serializer_class = MessageInfoGROUPSerializator

class Send_out_stistic_List(ListAPIView):
    """
    получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_out_stistic_Serializator
