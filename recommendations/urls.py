from django.urls import path
from .views import ReccomendView


urlpatterns = [
    path('suggested-freinds/<int:p_user_id>', ReccomendView.as_view())
]