from django.db import models

class PGN(models.Model):
    content = models.TextField(help_text="Texte complet au format PGN")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PGN du {self.uploaded_at}"
