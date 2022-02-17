
import requests as r
from celery import shared_task

from sender.models import MessageInfo



@shared_task
def send_message(id,phone,text):
    URL_SEND_OUT_MSG = f"http://192.168.0.107:8008/send/{id}"
    DATA = {

            "id": f"{id}",
            "phone": f"{phone}",
            "text": f"Text for {text}",
        }

    print("Ссылка:\n",URL_SEND_OUT_MSG)
    print("data=\n",DATA)
    try:
        resp = r.post(url=URL_SEND_OUT_MSG,data=DATA)
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
        msg_info_upd = MessageInfo.objects.filter(pk = id).update(status = True)
        print("MessageInfo.objects.filter(pk=id)=",msg_info_upd)

        print("всё ок, можно заносить в базу что всё ок")
    if resp.status_code in bad_resp:
        print(f"Всё плохо,  код ошибки = {resp.status_code}")

    return True

