from PIL import Image, ImageDraw, ImageFont
import numpy as np
import chess.pgn
import chess.svg
import cairosvg
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import concatenate_audioclips, concatenate_videoclips
import io
import os
import random

MOVE_SOUND = os.path.join('sounds', 'Move.mp3')
MUSICS_PATH = os.path.join('musics')


def resize_image(image, target_size):
    """Redimensionne une image PIL pour qu'elle ait la taille spécifiée."""
    return image.resize((target_size, target_size), Image.Resampling.LANCZOS)


def generate_frame(headers, image_size=600):
    """Crée une image d'introduction avec les headers du PGN, avec un texte centré horizontalement et verticalement."""
    # Créer une image noire
    width, height = image_size, image_size
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)

    # Charger une police par défaut
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default(size=40)

    # Construire les lignes à afficher
    lines = [f"{key}: {value}" for key, value in headers.items()]
    line_spacing = 30  # Espacement entre les lignes

    # Calculer la hauteur totale du texte
    total_text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines) + (len(lines) - 1) * line_spacing

    # Position verticale de départ pour centrer les lignes
    y_start = (height - total_text_height) // 2

    # Dessiner chaque ligne de texte, centrée horizontalement
    y_offset = y_start
    for line in lines:
        text_bbox = font.getbbox(line)
        text_width = text_bbox[2] - text_bbox[0]  # Largeur du texte
        x_position = (width - text_width) // 2  # Centrage horizontal
        
        draw.text((x_position, y_offset), line, fill="white", font=font)
        y_offset += (text_bbox[3] - text_bbox[1]) + line_spacing

    # Redimensionner et convertir en tableau NumPy
    image = resize_image(image, image_size)
    return np.array(image)

def add_player_names_to_frame(frame, white_player, black_player, image_size=600, padding=50):
    """Ajoute des noms de joueurs avec un espace (padding) au-dessus et en dessous de l'échiquier."""
    width, height = image_size+ 2 * padding, image_size + 2 * padding  # Ajouter un espace pour les noms
    new_image = Image.new("RGB", (width, height), "black")  # Créer une nouvelle image avec plus de hauteur
    original_image = Image.fromarray(frame)
    
    # Coller l'échiquier au centre vertical
    new_image.paste(original_image, (padding, padding))
    
    draw = ImageDraw.Draw(new_image)
    
    # Charger une police par défaut
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default(size=30)

    # Ajouter le nom du joueur Noir (en haut)
    black_text = f"{black_player}"
    black_text_width = font.getbbox(black_text)[2] - font.getbbox(black_text)[0]
    black_x_position = padding
    draw.text((black_x_position, 10), black_text, fill="white", font=font)

    # Ajouter le nom du joueur Blanc (en bas)
    white_text = f"{white_player}"
    white_text_width = font.getbbox(white_text)[2] - font.getbbox(white_text)[0]
    white_x_position = padding
    draw.text((white_x_position, height - padding + 10), white_text, fill="white", font=font)
    new_image = resize_image(new_image, image_size + 2* padding)
    return np.array(new_image)



def generate_chess_video_from_pgn(content, output_path, image_size=1024, video_fps=1, bitrate="150000k", random_music=False):
    """Génère une vidéo complète d'une partie d'échecs avec une introduction depuis un PGN."""

    selected_music_name = ""
    try:
        image_size -= 100
        # Charger le PGN
        pgn = io.StringIO(content)
        game = chess.pgn.read_game(pgn)
        if not game:
            raise ValueError("Invalid PGN content.")
        
        # Récupérer les noms des joueurs
        white_player = game.headers.get("White", "White")
        black_player = game.headers.get("Black", "Black")

        # Extraire les headers pour l'introduction
        headers = {key: game.headers.get(key, "") for key in ["Event", "Site", "Date", "White", "Black"]}

        # Générer la vidéo d'introduction
        intro_frame = generate_frame(headers, image_size=image_size+100)
        intro_clip = ImageClip(intro_frame, duration=5)

        # Générer la vidéo principale
        board = game.board()
        moves = list(game.mainline_moves())
        frames = []
        audio_clips = []

        for i, move in enumerate(moves):
            board.push(move)
            svg_board = chess.svg.board(board, size=image_size, lastmove=move)

            try:
                # Convertir SVG en PNG
                png_image = cairosvg.svg2png(bytestring=svg_board, output_width=image_size, output_height=image_size)
                image = Image.open(io.BytesIO(png_image))
                frame_with_names = add_player_names_to_frame(np.array(image), white_player, black_player, image_size)
                frames.append(frame_with_names)

                # Ajouter le son du coup
                audio_clip = AudioFileClip(MOVE_SOUND).subclip(0, 1/video_fps)
                audio_clips.append(audio_clip)
            except Exception as e:
                raise Exception(f"Erreur lors du traitement de la frame {i+1}: {e}")
        
        result = {key: game.headers.get(key, "") for key in ["Result"]}
        result_frame = generate_frame(result, image_size=image_size+100)
        result_clip = ImageClip(result_frame, duration=10)

        if not frames:
            raise ValueError("No frames generated from the PGN.")
            

        # Durée supplémentaire pour le dernier frame (en secondes)
        last_frame_duration = 10

        # Prolonger le dernier frame
        last_frame = frames[-1]  # Dernier frame
        last_frame_clip = ImageClip(last_frame, duration=last_frame_duration)

        # Créer le clip principal
        main_clip = ImageSequenceClip(frames[:-1], fps=video_fps)  # Séquence des frames normaux
        main_clip = concatenate_videoclips([main_clip, last_frame_clip])
        move_sounds = concatenate_audioclips(audio_clips)

        # Ajouter une musique de fond aléatoire si random_music est activé
        if random_music:
            music_files = [os.path.join(MUSICS_PATH, file) for file in os.listdir(MUSICS_PATH) if file.endswith(".mp3")]
            if not music_files:
                raise ValueError("No music files found in the specified folder.")
            
            selected_music = random.choice(music_files)
            selected_music_name = os.path.splitext(os.path.basename(selected_music))[0]

            selected_audio = AudioFileClip(selected_music)
            audio = selected_audio
            while selected_audio.duration < main_clip.duration+ + result_clip.duration:
                selected_audio = concatenate_audioclips([selected_audio, audio])

            background_music = selected_audio.subclip(0, min(selected_audio.duration, main_clip.duration+ + result_clip.duration))
            # background_music = background_music.volumex(0.3)  # Ajuster le volume de la musique
            
            # Superposer les deux pistes audio
            combined_audio = CompositeAudioClip([background_music, move_sounds])
            main_clip = main_clip.set_audio(combined_audio)
        else:
            main_clip = main_clip.set_audio(move_sounds)

        # Concaténer l'intro et la vidéo principale
        final_clip = concatenate_videoclips([intro_clip, main_clip, result_clip])
        final_clip.write_videofile(output_path, codec="libx264", bitrate=bitrate)

        return output_path, selected_music_name

    except Exception as e:
        raise Exception(f"Failed to generate video: {str(e)}")
