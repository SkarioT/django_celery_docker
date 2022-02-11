from datetime import tzinfo
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
    class Meta:
        model = Send_out
        fields = '__all__'

    def create(self, validated_data):

        #всю эту логику надо закинуть в celery

        print("validated_data:",validated_data)
        send = Send_out.objects.create(
            start_date_time=validated_data.get('start_date_time',None),
            filter_code=validated_data.get('filter_code',None),
            filter_tag=validated_data.get('filter_tag',None),
            text_msg=validated_data.get('text_msg',None),
            end=validated_data.get('end',None),

        )
        print("Send_out:\n",send)
        
        client = Client.objects.filter(code=validated_data.get('filter_code'),tag=validated_data.get('filter_tag'))
        print("Find Client:\n",client)
        for clien_t in client:
            print("id:",clien_t.id)
            print("phone:",clien_t.phone_number)
            
            message_info = MessageInfo.objects.create(
                create = datetime.datetime.now(tz=pytz.timezone(f'Etc/GMT-{clien_t.tz}')),
                send_out_id = send,
                client_id = clien_t
            )
            print("message_info:\n",message_info)
        return send

class MessageInfoSerializator(serializers.ModelSerializer):
    # status = serializers.CharField(read_only=True)
    class Meta:
        model = MessageInfo
        fields = '__all__'


class MessageInfoGROUPSerializator(serializers.ModelSerializer):
    group_True = serializers.SerializerMethodField()
    group_False = serializers.SerializerMethodField()

    def get_group_True(self, instance):
        # print("instans_True",instance.status)
        status = MessageInfo.objects.filter(status="1")
        return MessageInfoSerializator(status, many=True).data

    #разобраться в выводе, как сделать вывод с групировкой не по кол-ву раз

    def get_group_False(self, instance):
        status = MessageInfo.objects.filter(status="0")
        print(MessageInfoSerializator(status, many=True).data)
        return MessageInfoSerializator(status, many=True).data
    
    class Meta:
        model = MessageInfo
        fields = 'group_True','group_False'
