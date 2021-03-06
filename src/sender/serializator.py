from .models import Client,Send_out,MessageInfo
import pytz
import re

#_________celery____
from django_celery_beat.models import PeriodicTask,ClockedSchedule
import json
#------------------------
#__________django-rest_________
from rest_framework import serializers
#---------------------------------



#проверка на ввод российского номера
regex_phone = re.compile('^((\+7|7)+([0-9]){10})$')
#проверяю TZ для клиента
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

    #проверяю на дату создания
    def validate(self, data):
        #проверка на то,что дата начала рассылки должна быть МЕНЬШЕ датаы окончания
        if data['start_date_time'] >= data['end']:
            raise serializers.ValidationError(f"The end date must be greater than the start date. end({data['end']}) <= start({data['start_date_time']})")
        
        print(data['filter_code'],data['filter_tag'])
        
        # проверка на параметры фильтра, если ни кого по заданном параметрам не найдено - ошибка
        client = Client.objects.filter(code = data['filter_code'],tag = data['filter_tag'])
        if len(client) == 0:
            print("Ошибка, нет подходящих пользователей")
            raise serializers.ValidationError(f"Don't find Client for conditions: filter_code = {data['filter_code']} & filter_tag = {data['filter_tag']} ")
        # else:
        #     for client_t in client:
        #         pass
        return data

    def create(self, validated_data):
        send = Send_out.objects.create(
            start_date_time = validated_data.get('start_date_time',None),
            filter_code = validated_data.get('filter_code',None),
            filter_tag = validated_data.get('filter_tag',None),
            text_msg = validated_data.get('text_msg',None),
            end = validated_data.get('end',None),

        )

        
        #после создания рассылки, сразу получаю информацию для кого её необходимо сделать
        client = Client.objects.filter(code=validated_data.get('filter_code'),tag = validated_data.get('filter_tag'))
        #клиентов подходящих под рассылку может быть >1
        for clien_t in client:
            #из поля "Часовой пояс" получаю его timezone
            ctz= str(clien_t.tz)

            if ctz.startswith("-"):
                ctz = ctz.replace('-','')
                ptz = pytz.timezone(f'Etc/GMT+{ctz}')
            else:
                ctz = ctz.replace('+','')
                ptz = pytz.timezone(f'Etc/GMT-{ctz}')
            

            clinet_tz_start = (send.start_date_time).replace(tzinfo=ptz)
            clinet_tz_end = (send.end).replace(tzinfo=ptz)
            
            
            #для каждого клиента создаю сообщение
            message_info = MessageInfo.objects.create(
                create = clinet_tz_start,
                send_out_id = send,
                client_id = clien_t
            )

            print("id сообщения=",message_info.id)
            print("Номер телефона=",clien_t.phone_number)
            print("Текст сообщения для рассылки:\n",send.text_msg)
            print("дата начала рассылки",clinet_tz_start)
            print("дата окончания рассылки",clinet_tz_end)



            clocked_,created = ClockedSchedule.objects.get_or_create(
                clocked_time = clinet_tz_start
            )

            pt,createdd= PeriodicTask.objects.get_or_create(
            clocked = clocked_,
            name = f'{message_info.id} {clien_t.phone_number} {clinet_tz_start}',          
            task = 'sender.tasks.send_message',  
            start_time = clinet_tz_start,
            expires = clinet_tz_end,
            one_off = True,
            enabled = True,
            args =[],
            kwargs = json.dumps({ "id" :f"{message_info.id}",
                    "phone":f"{clien_t.phone_number}",
                    "text" : f"{send.text_msg}"
                    })
            )
            print("PT_id=",pt.id)
            print("PT_task=",pt.task)
            print("-"*20)

        return send

    def update(self,instance, validated_data):

        #обновляю параметры рассылки    
        instance.start_date_time = validated_data.get('start_date_time')
        instance.filter_code = validated_data.get('filter_code')
        instance.filter_tag = validated_data.get('filter_tag')
        instance.text_msg = validated_data.get('text_msg')
        instance.end = validated_data.get('end',instance.end)
        instance.save()

        # после обновления рассылки сразу получаю информацию кому её необходимо сделать
        # возможно параметры изменились
        print("instance_code_2", instance.filter_code)
        
        
        client_news = Client.objects.filter(code = validated_data.get('filter_code'),tag = validated_data.get('filter_tag'))
        print("Find Client:\n",client_news)
        #клиентов подходящих под рассылку может быть >1
        for clien_t in client_news:
            print("id:",clien_t.id)
            print("phone:",clien_t.phone_number)
            
            #для каждого клиента создаю сообщение
            ctz = str(clien_t.tz)
            if ctz.startswith("-"):
                ctz = ctz.replace('-','')
                ptz = pytz.timezone(f'Etc/GMT+{ctz}')
            else:
                ctz = ctz.replace('+','')
                ptz = pytz.timezone(f'Etc/GMT-{ctz}')
            print("ptz=",ptz)


            clinet_tz_start = (instance.start_date_time).replace(tzinfo=ptz)
            clinet_tz_end = (instance.end).replace(tzinfo = ptz)
            message_info,created = MessageInfo.objects.filter(pk = clien_t.id).update_or_create(
                create = clinet_tz_start,
                send_out_id = instance,
                client_id = clien_t
            )
            print("message_info:\n",message_info)

            clocked_,created = ClockedSchedule.objects.get_or_create(
                clocked_time = clinet_tz_start
            )

            pt,createdd = PeriodicTask.objects.get_or_create(
            clocked = clocked_,
            name =f'{message_info.id} {clien_t.phone_number} {clinet_tz_start}',          
            task ='sender.tasks.send_message',  
            start_time = clinet_tz_start,
            expires = clinet_tz_end,
            one_off = True,
            enabled = True,
            args = [],
            kwargs = json.dumps({ "id" :f"{message_info.id}",
                    "phone":f"{clien_t.phone_number}",
                    "text" : f"{instance.text_msg}"
                    })
            )
           


        return instance

class Send_out_Details_Serializator(serializers.ModelSerializer):
    message_out_list = serializers.SerializerMethodField()
    def get_message_out_list(self, instance):
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