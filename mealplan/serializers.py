from rest_framework import *
from .models import *

class NutrisiSerializer(serializers.ModelSerializer):
    menu = serializers.CharField(source="menu.nama_menu", read_only=True)
    class Meta:
        model = Nutrisi
        fields = ["menu", "kalori", "protein", "lemak", "serat"]