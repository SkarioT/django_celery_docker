
from .models import Client

#__________django-rest_________
from .serializator import *
from rest_framework.generics import *
#---------------------------------




#for Client
class ClientView(ListAPIView):
    """
    Список всех клиентов
    """
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClienCreate (CreateAPIView):
    """
    Создание нового клиента
    """
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClientUpdate (UpdateAPIView):
    """
    Изменение параметров клиента
    """
    queryset = Client.objects.all()
    serializer_class = ClienSerializator

class ClientDelete (DestroyAPIView):
    """
    Удаление клиента
    """
    queryset = Client.objects.all()
    serializer_class = ClienSerializator


# for Send out
class Send_outView(ListAPIView):
    """
    Список всех рассылок
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_out_stistic_List(ListAPIView):
    """
    Получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_out_stistic_Serializator


class Send_outCreate (CreateAPIView):
    """
    Создание новой рассылки
    """
    # queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator
    
class Send_outUpdate (UpdateAPIView):
    """
    Изменение параметров рассылки
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_outDelete (DestroyAPIView):
    """
    Удаление клиента
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_outSerializator

class Send_outDetails (RetrieveAPIView):
    """
    Получения детальной статистики отправленных сообщений по конкретной рассылке
    """
    queryset = Send_out.objects.all()
    serializer_class = Send_out_Details_Serializator


class Message_Info_View(ListAPIView):
    """
    Группировка всех сообщений по статусам
    """
    queryset = MessageInfo.objects.all()[:1]
    serializer_class = MessageInfoGROUPSerializator



