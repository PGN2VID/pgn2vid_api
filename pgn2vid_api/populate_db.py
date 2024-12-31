import os
import django

# Configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pgn2vid_api.settings")
django.setup()

from api.models import PlayersPGN

INPUT_DIR = "players_pgn"  

def populate_db():  
    for player_dir in os.listdir(INPUT_DIR):
        player_path = os.path.join(INPUT_DIR, player_dir)

        if os.path.isdir(player_path):

            for pgn_file in os.listdir(player_path):
                if pgn_file.endswith(".pgn"):
                    pgn_file_path = os.path.join(player_path, pgn_file)

                    PlayersPGN.objects.create(
                        player=player_dir,
                        pgn_file=pgn_file,
                        generated=False
                    )
                    print(f"Ajouté : {player_dir} - {pgn_file}")

populate_db()
