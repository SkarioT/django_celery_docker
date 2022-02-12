"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sender import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # CRUD_API client
    # +дополнительная информация  - вывод всех клиентов
    path('api_v1/list_client/', views.ClientView.as_view()),
    #добавления нового клиента в справочник со всеми его атрибутами
    path('api_v1/create_client/',views.ClienCreate.as_view()),
    #обновления данных атрибутов клиента
    path('api_v1/update_client/<int:pk>',views.ClientUpdate.as_view()),
    #удаления клиента из справочника
    path('api_v1/delete_client/<int:pk>',views.ClientDelete.as_view()),

    # CRUD_API send_out
    # +дополнительная информация  - вывод всех рассылок
    path('api_v1/list_send/', views.Send_outView.as_view()),
    path('api_v1/create_send/',views.Send_outCreate.as_view()),
    #обновления атрибутов рассылки
    path('api_v1/update_send/<int:pk>',views.Send_outUpdate.as_view()),
    #удаления рассылки
    path('api_v1/delete_send/<int:pk>',views.Send_outDelete.as_view()),
    #получения детальной статистики отправленных сообщений по конкретной рассылке
    path('api_v1/details_send/<int:pk>',views.Send_outDetails.as_view()),

    #группировка по статусам, ВСЕХ сообщений
    path('api_v1/group_message_status/', views.Message_Info_View.as_view()),
    
    #получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
    path('api_v1/send_out_stistic/', views.Send_out_stistic_List.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
