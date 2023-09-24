from django.shortcuts import render, HttpResponse
from rest_framework import views, status
from .serializers import CreateChatSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom
from django.core import exceptions
from django.contrib.auth import get_user_model

def index(request):
    return render(request, "chat/index.html")

def room(request, p_room_name,p_token):

    try:

        l_chat_room = ChatRoom.objects.get(room_name = p_room_name)

        l_user_model = get_user_model()

        l_user = l_user_model.objects.get(auth_token = p_token)

        if l_chat_room.user1 != l_user and l_chat_room.user2 != l_user:
            return HttpResponse("You do not have the access rights to this page.", status = status.HTTP_401_UNAUTHORIZED)

        return render(request, "chat/room.html", {"room_name": p_room_name, "token":p_token})
    
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("Cannot find the user or the chat room.", status=status.HTTP_400_BAD_REQUEST)
    
    except:
        return HttpResponse("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SendMessageView(views.APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Extract the sender, recipient, and message from the request
        l_user_model = get_user_model()
        recipient_id = request.data['recipient_phone']
        message = request.data['message']

        try:
            l_recipient = l_user_model.objects.get(phone = recipient_id)
        except exceptions.ObjectDoesNotExist:
            Response({"status": "Recipient does not exist"}, status=status.HTTP_400_BAD_REQUEST)



        if l_recipient.is_online == False:
            Response({"status": "Recipient is offline."}, status=status.HTTP_400_BAD_REQUEST)
        
        l_chat_room = None

        try:
            l_chat_room = ChatRoom.objects.get(user1 = request.user, user2 = l_recipient)

        except exceptions.ObjectDoesNotExist:
            try:

                l_chat_room = ChatRoom.objects.get(user2 = request.user, user1 = l_recipient)
            
            except:

                return Response({"status" : "Initiate a chat with this user first"}, status=status.HTTP_400_BAD_REQUEST)            
        

        room_group_name = 'chat_' + l_chat_room.room_name

        channel_layer = get_channel_layer()
       
        async_to_sync(channel_layer.group_send)(
            room_group_name, {"type": "chat.message", "message": message}
        )
       
        return Response({"status": "Message sent successfully."}, status=status.HTTP_200_OK)
      



class CreateChatView(views.APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):

        l_user_model = get_user_model()

        l_serializer = CreateChatSerializer(data=request.data)

        if l_serializer.is_valid():

            l_sender = request.user

            try:
                l_recipient = l_user_model.objects.get(phone = l_serializer.validated_data['recipient'])

            except exceptions.ObjectDoesNotExist:

                return Response({"message" : "The user you are trying to chat to does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            l_sender_phone = int(l_sender.phone)
            l_recipient_phone = int(l_recipient.phone)
           
            l_room_name = f"private_chat_{min(l_sender_phone, l_recipient_phone)}_{max(l_sender_phone , l_recipient_phone)}"
            l_room_group_name = f"chat_{l_room_name}"

            ChatRoom.objects.get_or_create(room_name = l_room_name, user1 = l_sender, user2 = l_recipient)

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_add)(l_room_group_name, f"user_{l_sender}")
            async_to_sync(channel_layer.group_add)(l_room_group_name, f"user_{l_recipient}")

            return Response({"room_name": l_room_name}, status=status.HTTP_201_CREATED)
        
        return Response(l_serializer.errors, status=status.HTTP_400_BAD_REQUEST)