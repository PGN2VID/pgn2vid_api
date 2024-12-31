import chess
import chess.pgn
import chess.svg
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from PIL import Image, ImageFilter
import io
from io import BytesIO
import cairosvg
import numpy as np
import os


def generate_chess_video_from_pgn(content, output_path, image_size=600, video_fps=1, bitrate="5000k"):
    """Génère une vidéo d'une partie d'échecs depuis un PGN."""
    try:
        pgn = io.StringIO(content)
        game = chess.pgn.read_game(pgn)
        
        if not game:
            raise ValueError("Invalid PGN content.")
        
        board = game.board()
        moves = list(game.mainline_moves())
        frames = []

        for i, move in enumerate(moves):
            board.push(move)
            # Générer SVG pour le coup
            svg_board = chess.svg.board(board, size=600)
            
            try:
                # Convertir SVG en PNG
                png_image = cairosvg.svg2png(bytestring=svg_board, output_width=1200, output_height=1200)
                image = Image.open(BytesIO(png_image))
                image = image.filter(ImageFilter.SMOOTH_MORE)
                frames.append(np.array(image))
            except Exception as e:
                raise Exception(f"Erreur lors du traitement de la frame {i+1}: {e}")

        if not frames:
            raise ValueError("No frames generated from the PGN.")

        clip = ImageSequenceClip(frames, fps=video_fps)
        clip.write_videofile(output_path, codec="libx264", bitrate=bitrate)

        return True

    except Exception as e:
        raise Exception(f"Failed to generate video: {str(e)}")
