from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PGNViewSet, PGNVideoView


urlpatterns = [
    path('generate-chess-video/', PGNVideoView.as_view(), name='generate_chess_video'),
]
