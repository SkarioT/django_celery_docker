import code
from email import message
from http import client
from venv import create
from django.forms import SlugField, fields
from rest_framework import serializers
from .models import Client,Send_out,MessageInfo


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
                send_out_id = send,
                client_id = clien_t
            )
            print("message_info:\n",message_info)
        return send