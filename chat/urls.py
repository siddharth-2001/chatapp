from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", views.index, name="index"),
    path("lobby/<str:p_room_name>/<str:p_token>/", views.room, name="room"),
    path("chat/start/", views.CreateChatView.as_view(), name='create-chat' ),
    path("chat/send/", views.SendMessageView.as_view(), name = "send-message"),
]