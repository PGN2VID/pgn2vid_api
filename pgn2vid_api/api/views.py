from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PGN
from .serializers import PGNSerializer

import os
from django.conf import settings
from utils.video_generator import generate_chess_video_from_pgn

class PGNVideoView(APIView):
    def post(self, request, *args, **kwargs):
        from .serializers import PGNSerializer
        
        serializer = PGNSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']
            
            try:
                video_filename = f"chess_game_{int(os.path.getmtime(__file__))}.mp4"
                video_path = os.path.join(settings.MEDIA_ROOT, video_filename)

                if generate_chess_video_from_pgn(content, video_path):


                    video_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{video_filename}"
                    
                    return Response({"video_url": video_url}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PGNViewSet(viewsets.ModelViewSet):
    queryset = PGN.objects.all()
    serializer_class = PGNSerializer
