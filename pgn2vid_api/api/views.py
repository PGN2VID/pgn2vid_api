from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PGN, PlayersPGN
from .serializers import PGNSerializer

import os
import random
from datetime import datetime
import time
from django.conf import settings
import chess.pgn
from utils.video_generator import generate_chess_video_from_pgn

class PGNVideoView(APIView):
    def post(self, request, *args, **kwargs):
        from .serializers import PGNSerializer
        
        serializer = PGNSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']
            
            try:
                video_file_name = f"chess_game_{str(int(time.time()))}.mp4"
                video_path = os.path.join(settings.MEDIA_ROOT, video_file_name)

                if generate_chess_video_from_pgn(content, video_path):


                    video_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{video_file_name}"
                    
                    return Response({"video_url": video_url}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RandomPGNVideoView(APIView):
    def get(self, request, *args, **kwargs):

        today_pgn = PlayersPGN.objects.filter(
            generated=True,
            video_generation_date__date=datetime.today().date()  # Filtrer par la date de génération de la vidéo
        ).first()

        video_url = ''

        if not today_pgn:
            remainings_pgn = PlayersPGN.objects.filter(generated=False)

            today_pgn = random.choice(remainings_pgn)

            pgn_file = os.path.join("players_pgn", f'{today_pgn.player}/{today_pgn.pgn_file}')
            with open(pgn_file) as content:
                try:
                    video_file_name = f"{today_pgn.player.lower().replace(' ','')}_{today_pgn.pgn_file.split('.')[0]}.mp4"
                    video_path = os.path.join(settings.MEDIA_ROOT, video_file_name)

                    if generate_chess_video_from_pgn(content.read(), video_path):


                        video_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{video_file_name}"

                        today_pgn.generated = True
                        today_pgn.video_file_name = video_file_name
                        today_pgn.video_generation_date = datetime.today()

                        today_pgn.save()

                        
                        # return Response({"video_url": video_url}, status=status.HTTP_200_OK)
                
                except Exception as e:
                    return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            
            video_url = f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{today_pgn.video_file_name}"


        pgn_file = os.path.join("players_pgn", f'{today_pgn.player}/{today_pgn.pgn_file}')
        with open(pgn_file) as content:
            
            game = chess.pgn.read_game(content)
            content.seek(0)
            return Response({
                "video_url": video_url,
                "event": game.headers.get("Event", ""),
                "site": game.headers.get("Site", ""),
                "date": game.headers.get("Date", ""),
                "white": game.headers.get("White", ""),
                "black": game.headers.get("Black", ""),
                "result": game.headers.get("Result", ""),
                "pgn": content.read()
            }, status=status.HTTP_200_OK)



class PGNViewSet(viewsets.ModelViewSet):
    queryset = PGN.objects.all()
    serializer_class = PGNSerializer
