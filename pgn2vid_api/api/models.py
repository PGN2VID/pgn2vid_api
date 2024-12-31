from django.db import models

class PGN(models.Model):
    content = models.TextField(help_text="Texte complet au format PGN")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PGN du {self.uploaded_at}"
    
class PlayersPGN(models.Model):
    player = models.TextField(help_text="Nom du joueur")
    pgn_file = models.TextField("Nom du fichier pgn")
    generated = models.BooleanField(default=False)
    video_generation_date = models.DateTimeField(null=True, blank=True, help_text="Date de génération de la vidéo")
    video_file_name = models.CharField(max_length=255, null=True, blank=True, help_text="Nom du fichier vidéo généré")

    def __str__(self):
        return f"{self.player} - {self.pgn_file}"
