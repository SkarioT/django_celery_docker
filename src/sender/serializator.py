from django.forms import SlugField, fields
from rest_framework import serializers
from .models import Client,Send_out,MessageInfo
import datetime
import pytz



class ClienSerializator(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class Send_outSerializator(serializers.ModelSerializer):
    start_date_time = serializers.DateTimeField()
    end = serializers.DateTimeField()
    class Meta:
        model = Send_out
        fields = 'start_date_time','filter_code','filter_tag','text_msg','end'

    def create(self, validated_data):
        print("validated_data:",validated_data)

        #создаю рассылку
        send = Send_out.objects.create(
            start_date_time=validated_data.get('start_date_time',None),
            filter_code=validated_data.get('filter_code',None),
            filter_tag=validated_data.get('filter_tag',None),
            text_msg=validated_data.get('text_msg',None),
            end=validated_data.get('end',None),

        )
        print("Send_out:\n",send)
        
        
        #после создания рассылки сразу получаю информацию кому её необходимо сделать
        client = Client.objects.filter(code=validated_data.get('filter_code'),tag=validated_data.get('filter_tag'))
        print("Find Client:\n",client)
        #клиентов подходящих под рассылку может быть >1
        for clien_t in client:
            print("id:",clien_t.id)
            print("phone:",clien_t.phone_number)
            
            #для каждого клиента создаю сообщение
            message_info = MessageInfo.objects.create(
                create = datetime.datetime.now(tz=pytz.timezone(f'Etc/GMT-{clien_t.tz}')),
                send_out_id = send,
                client_id = clien_t
            )
            print("message_info:\n",message_info)
           
        return send

class Send_out_Details_Serializator(serializers.ModelSerializer):
    message_out_list = serializers.SerializerMethodField()
    def get_message_out_list(self, instance):
        print('get_clien_list instance',instance)
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