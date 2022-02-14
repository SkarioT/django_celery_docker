
from .models import Client

#__________django-rest_________
from .serializator import *
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
#---------------------------------

#_________celery____
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from . import tasks
#------------------------



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

#__________________________________
class CreatePeriodicTask(APIView):

    def get(self, request, format=None):

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
            )
        old_cleaner = PeriodicTask.objects.all()
        print("old_cleaner\n\n\n\n\n",old_cleaner)
        old_cleaner.delete()
        pt,createdd= PeriodicTask.objects.get_or_create(
        interval=schedule,                  # we created this above.
        name='Importing contacts',          # simply describes this periodic task.
        task='sender.tasks.send_message',  # name of task.
        expires=datetime.now() + timedelta(seconds=31)
        )
        print("pt_expires=",pt)
        print("expires=datetime.utcnow() + timedelta(seconds=31)", datetime.utcnow() + timedelta(seconds=31))

        return Response(datetime.utcnow() + timedelta(seconds=31))