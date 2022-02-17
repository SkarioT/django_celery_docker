
import requests as r
import json
from requests.structures import CaseInsensitiveDict
from celery import shared_task

# from sender.models import MessageInfo



@shared_task
def send_message(id,phone,text):
    URL_SEND_OUT_MSG = f"https://probe.fbrq.cloud/v1/send/{id}"
    # id = id
    # phone = phone
    # text = text
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzY1NTQxMDQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkFsZW5rYU5vdm9yb25lZ2hza2F5In0.qDsPbj2T00b4LTbVtrjyCleY-BoTPvuObd83rEj4AGM"
    headers["Content-Type"] = "application/json"

    DATA = {"id": id, "phone": phone, "text": f"{text}"}
    data = json.dumps(DATA)
    print("id=",id)
    print("phone=",phone)
    print("text=",text)
    print("url=",URL_SEND_OUT_MSG)
    print("data=",data)

    try:
        resp = r.post(url=URL_SEND_OUT_MSG,data=data,headers=headers)
        print(resp)
    except:
        print("Проблемымы с соденинением")
        return False

    ok_resp = [200,201]
    bad_resp = [500,404,400]
    print("resp.status_code=",resp.status_code)
    if resp.status_code in ok_resp:
        # Если удаленный сервер ответил что всё ок = обновляю для каждого "ок" сообщения его статус
        print("id после того как всё ок =",id)
        # msg_info_upd = MessageInfo.objects.filter(pk = id).update(status = True)
        # print("MessageInfo.objects.filter(pk=id)=",msg_info_upd)

        print("всё ок, можно заносить в базу что всё ок")
        return True

    if resp.status_code in bad_resp:
        print(f"Всё плохо,  код ошибки = {resp.status_code}")
        return False

    
# send_message(1,78888888888,"текс для 88 спб")