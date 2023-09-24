from django.urls import path
from .views import RecommendView


urlpatterns = [
    path('suggested-freinds/<int:p_user_id>', RecommendView.as_view())
]