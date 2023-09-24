from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, logout

from .models import CustomUser as User
from .serializers import UserSerializer

# Create your views here.

class UserListView(generics.ListAPIView):
   authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
   permission_classes = [IsAuthenticated]

   l_user = get_user_model()

   queryset = l_user.objects.filter(is_online = True)
   serializer_class = UserSerializer
   

class CreateUserView(APIView):
   def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class LogOutUserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        user = request.user
        user.is_online = False
        user.save()
        logout(request)

        return Response({"status": "Logged out"}, status=status.HTTP_200_OK)
        

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
    
        user.is_online = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })