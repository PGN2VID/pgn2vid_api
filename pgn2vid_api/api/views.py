from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PGN
from .serializers import PGNSerializer
import io

import chess
import chess.pgn
import chess.svg
from moviepy.video.io import ImageSequenceClip
from PIL import Image, ImageFilter
from io import BytesIO
import cairosvg
import numpy as np


from django.http import FileResponse
import tempfile
import os

class PGNVideoView(APIView):
    def post(self, request, *args, **kwargs):
        from .serializers import PGNSerializer
        
        serializer = PGNSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']
            
            try:
                # Lire le PGN depuis le texte reçu
                pgn = io.StringIO(content)
                game = chess.pgn.read_game(pgn)
                
                if not game:
                    return Response({"error": "Invalid PGN content."}, status=status.HTTP_400_BAD_REQUEST)
                
                board = game.board()
                moves = list(game.mainline_moves())
                frames = []
                
                for i, move in enumerate(moves):
                    board.push(move)
                    
                    # Générer SVG pour le coup
                    svg_board = chess.svg.board(board, size=600, colors={
                        "square light": "#e0f7fa",
                        "square dark": "#0288d1",
                        "square light lastmove": "#b3e5fc",
                        "square dark lastmove": "#0277bd",
                        "square light check": "#ffccbc",
                        "square dark check": "#ff5722",
                        "coord": "#000000"
                    })
                    
                    try:
                        # Convertir SVG en PNG
                        png_image = cairosvg.svg2png(bytestring=svg_board, output_width=1200, output_height=1200)
                        image = Image.open(BytesIO(png_image))
                        image = image.filter(ImageFilter.SMOOTH_MORE)
                        frames.append(np.array(image))
                    except Exception as e:
                        print(f"Erreur lors du traitement de la frame {i+1}: {e}")
                        continue
                
                if not frames:
                    return Response({"error": "No frames generated from the PGN."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Créer un fichier temporaire pour la vidéo
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_video:
                    video_path = tmp_video.name
                    clip = ImageSequenceClip.ImageSequenceClip(frames, fps=1)
                    clip.write_videofile(video_path, codec="libx264", bitrate="5000k")
                
                # Retourner la vidéo
                response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="chess_game.mp4"'
                
                # Supprimer le fichier temporaire après envoi
                # os.unlink(video_path)
                
                return response
            
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PGNViewSet(viewsets.ModelViewSet):
    queryset = PGN.objects.all()
    serializer_class = PGNSerializer
