from django.urls import include, path

from .views import UserListView, CreateUserView, CustomAuthToken, LogOutUserView


urlpatterns = [
    path('online-users/', UserListView.as_view(), name='user-list'),
    path('register/', CreateUserView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('logout/', LogOutUserView.as_view())
]