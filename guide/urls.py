# guide/urls.py
from django.urls import path
from .views import UserLocationView, MatchingUsersView

urlpatterns = [
    path('location/', UserLocationView.as_view(), name='user_location'),
    path('match-users/', MatchingUsersView.as_view(), name='match_users'),
]
