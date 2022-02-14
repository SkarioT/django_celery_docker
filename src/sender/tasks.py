from urllib import response
import requests as r
import random
import time

from celery import shared_task
from django.conf import settings





@shared_task
def send_message():
    randaome_name = random.randrange(70000000000,79999999999)
    id = random.randint(1,99999)
    URL_CREATE_MSG=f"http://192.168.0.107:8008/send/{id}"
    EXAMPLE_CITY = {

            "id": f"{id}",
            "phone": f"{randaome_name}",
            "text": f"Text for {randaome_name}",
        }

    print("Ссылка:\n",URL_CREATE_MSG)
    print("data=\n",EXAMPLE_CITY)
    resp = r.post(url=URL_CREATE_MSG,data=EXAMPLE_CITY)
    f_n = str(resp.status_code)+"_"+str(randaome_name)
    # print("f_n=",f_n)
    file_name = settings.BASE_DIR / 'req' / f_n
    # file_name = str(resp.status_code)+"_"+str(randaome_name)
    with open(file_name,"w") as f:
        f.write(str(EXAMPLE_CITY))
    return True

