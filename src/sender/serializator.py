from turtle import update
from django.forms import SlugField, fields
from rest_framework import serializers
from .models import Client,Send_out,MessageInfo
from django.utils import timezone
import datetime
import pytz
import re


#проверка на ввод российского номера
regex_phone = re.compile('^((\+7|7)+([0-9]){10})$')
#проверяю TZ
regex_tz = re.compile('^((\-|\+|)+([0-9]{1,2}))$')


class ClienSerializator(serializers.ModelSerializer):
    phone_number = serializers.RegexField(regex= regex_phone,max_length=11, min_length=11)
    tz = serializers.RegexField(regex= regex_tz,max_length=3, min_length=1)
    class Meta:
        model = Client
        fields = '__all__'

class Send_outSerializator(serializers.ModelSerializer):
    start_date_time = serializers.DateTimeField()
    end = serializers.DateTimeField()
    class Meta:
        model = Send_out
        fields = 'pk','start_date_time','filter_code','filter_tag','text_msg','end'

    def create(self, validated_data):
        #создаю рассылку
        send = Send_out.objects.create(
            start_date_time=validated_data.get('start_date_time',None),
            filter_code=validated_data.get('filter_code',None),
            filter_tag=validated_data.get('filter_tag',None),
            text_msg=validated_data.get('text_msg',None),
            end=validated_data.get('end',None),

        )
        # print("send_time_new_obj",send.start_date_time)
        #после создания рассылки сразу получаю информацию кому её необходимо сделать
        client = Client.objects.filter(code=validated_data.get('filter_code'),tag=validated_data.get('filter_tag'))
        print("Find Client:\n",client)
        print("Find Client LEN:\n",len(client))
        # print(**validated_data)
        # if len(client) == 0:
            # return Send_out(**validated_data)


        #добавить проверку, найдены ли вообще клиенты под такие параметры
        #если нет - вернуть ошибку



        #клиентов подходящих под рассылку может быть >1
        for clien_t in client:
            print("id:",clien_t.id)
            print("phone:",clien_t.phone_number)
            
            #для каждого клиента создаю сообщение
            ctz= str(clien_t.tz)
            if ctz.startswith("-"):
                ctz = ctz.replace('-','')
                ptz=pytz.timezone(f'Etc/GMT+{ctz}')
            else:
                ctz = ctz.replace('+','')
                ptz=pytz.timezone(f'Etc/GMT-{ctz}')
            print("ptz=",ptz)
            message_info = MessageInfo.objects.create(
                create = datetime.datetime.now(tz=ptz),
                send_out_id = send,
                client_id = clien_t
            )
            print("message_info:\n",message_info)
           
        return send

    def update(self,instance, validated_data):
        # обновляю рассылку
        #через relation_name удаляю ТОЛЬКО те рассылки которые со статусом False
        insta_objs = instance.message_send_out_id.all()
        for obj in insta_objs:
            if obj.status:
                print("obj.status",obj.status)
            else:
                obj.delete()

        #обновляю параметры рассылки    
        instance.start_date_time=validated_data.get('start_date_time')
        instance.filter_code=validated_data.get('filter_code')
        instance.filter_tag=validated_data.get('filter_tag')
        instance.text_msg=validated_data.get('text_msg')
        instance.end=validated_data.get('end',instance.end)
        instance.save()

        # после обновления рассылки сразу получаю информацию кому её необходимо сделать
        print("instance_code_2", instance.filter_code)
        
        
        client_news = Client.objects.filter(code=validated_data.get('filter_code'),tag=validated_data.get('filter_tag'))
        print("Find Client:\n",client_news)
        #клиентов подходящих под рассылку может быть >1
        for clien_t in client_news:
            print("id:",clien_t.id)
            print("phone:",clien_t.phone_number)
            
            #для каждого клиента создаю сообщение
            ctz= str(clien_t.tz)
            if ctz.startswith("-"):
                ctz = ctz.replace('-','')
                ptz=pytz.timezone(f'Etc/GMT+{ctz}')
            else:
                ctz = ctz.replace('+','')
                ptz=pytz.timezone(f'Etc/GMT-{ctz}')
            print("ptz=",ptz)
            message_info = MessageInfo.objects.filter(pk=clien_t.id).update_or_create(
                create = datetime.datetime.now(tz=ptz),
                send_out_id = instance,
                client_id = clien_t
            )
            print("message_info:\n",message_info)
           


        return instance

class Send_out_Details_Serializator(serializers.ModelSerializer):
    message_out_list = serializers.SerializerMethodField()
    def get_message_out_list(self, instance):
        # print('get_clien_list instance',instance)
        message_obj = MessageInfo.objects.filter(send_out_id = instance.id)
        return MessageInfoSerializator(message_obj, many=True).data
    class Meta:
        model = Send_out
        fields = '__all__'



class MessageInfoSerializator(serializers.ModelSerializer):
    send_out_id = serializers.SlugRelatedField(slug_field="text_msg",read_only=True)
    client_id = serializers.SlugRelatedField(slug_field="phone_number",read_only=True)
    class Meta:
        model = MessageInfo
        fields = '__all__'
  


class MessageInfoGROUPSerializator(serializers.ModelSerializer):

    group_True = serializers.SerializerMethodField()
    group_False = serializers.SerializerMethodField()

    def get_group_True(self, instance):
        status = MessageInfo.objects.filter(status="1")
        return MessageInfoSerializator(status, many=True).data

    def get_group_False(self, instance):
        # print("instance:\n",instance)
        status = MessageInfo.objects.filter(status="0")
        print("status_get_group_False",status)
        return MessageInfoSerializator(status, many=True).data
    
    class Meta:
        model = MessageInfo
        # fields = '__all__'
        fields = 'group_True','group_False'


class Send_out_stistic_Serializator(serializers.ModelSerializer):
    msg_group_status_True_counter = serializers.SerializerMethodField()
    msg_group_status_True_details = serializers.SerializerMethodField()
    
    msg_group_status_False_counter = serializers.SerializerMethodField()
    msg_group_status_False_details   = serializers.SerializerMethodField()
    

    def get_msg_group_status_True_counter(self, instance):
        counter = MessageInfo.objects.filter(status="1",send_out_id = instance.id).count()
        return counter

    def get_msg_group_status_False_counter(self, instance):
        counter = MessageInfo.objects.filter(status="0",send_out_id = instance.id).count()
        return counter


    def get_msg_group_status_True_details(self, instance):
        status = MessageInfo.objects.filter(status="1",send_out_id = instance.id)
        return MessageInfoSerializator(status, many=True).data

    def get_msg_group_status_False_details(self, instance):
        status = MessageInfo.objects.filter(status="0",send_out_id = instance.id)
        return MessageInfoSerializator(status, many=True).data

    class Meta:
        model = Send_out
        fields = '__all__'