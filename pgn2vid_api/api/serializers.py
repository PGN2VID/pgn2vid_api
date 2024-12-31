from rest_framework import serializers
from .models import PGN
from utils.helpers import is_pgn_valid

class PGNSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGN
        fields = '__all__'

    def validate_content(self, value):
        """
        Valide que le texte respecte un format PGN valide avec python-chess.
        """
        try:
            if not is_pgn_valid(value):
                raise serializers.ValidationError("Le PGN n'est pas valide.")
        except Exception as e:
            raise serializers.ValidationError(f"Erreur de validation PGN : {str(e)}")
        
        return value
