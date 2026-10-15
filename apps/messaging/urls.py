from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('send/<int:user_id>/', views.send_message_view, name='send_message'),
    path('compose/<int:receiver_id>/', views.compose_message_view, name='compose'),
    path('compose/', views.compose_message_view, name='compose_general'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('<int:pk>/', views.message_detail_view, name='detail'),
]