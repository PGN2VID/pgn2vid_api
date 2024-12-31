from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PGNViewSet, PGNVideoView, RandomPGNVideoView


urlpatterns = [
    path('generate-chess-video/', PGNVideoView.as_view(), name='generate_chess_video'),
    path('game-of-the-day/', RandomPGNVideoView.as_view(), name='game_of_the_day'),
]
