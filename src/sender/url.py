from django.urls import path
from . import views

urlpatterns = [
    # path('category', api.CategoryListAPIView.as_view(), name='api_categories'),
    # path('authors', api.AuthorListAPIView.as_view(), name='api_authors'),
    # path('books', api.BookListAPIView.as_view(), name='api_books'),

    path('list_client/', views.ClientView.as_view(),name='api_list_client'),
    #добавления нового клиента в справочник со всеми его атрибутами
    path('create_client/',views.ClienCreate.as_view(),name='create_client'),
    #обновления данных атрибутов клиента
    path('update_client/<int:pk>',views.ClientUpdate.as_view(),name="update_client"),
    # #удаления клиента из справочника
    path('delete_client/<int:pk>',views.ClientDelete.as_view(),name='delete_client'),

    # # CRUD_API send_out
    # # +дополнительная информация  - вывод всех рассылок
    path('list_send/', views.Send_outView.as_view(),name='list_send'),
    path('create_send/',views.Send_outCreate.as_view(),name='create_send'),
    # #обновления атрибутов рассылки
    path('update_send/<int:pk>',views.Send_outUpdate.as_view(),name='update_send'),
    # #удаления рассылки
    path('delete_send/<int:pk>',views.Send_outDelete.as_view(),name='delete_send'),
    # #получения детальной статистики отправленных сообщений по конкретной рассылке
    path('details_send/<int:pk>',views.Send_outDetails.as_view(),name='details_send'),

    # #группировка по статусам, ВСЕХ сообщений
    path('group_message_status/', views.Message_Info_View.as_view(),name='group_message_status'),
    
    # #получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
    path('send_out_stistic/', views.Send_out_stistic_List.as_view(),name='send_out_stistic'),
]