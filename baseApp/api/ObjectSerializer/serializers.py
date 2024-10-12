from rest_framework import serializers
from image_recognition_app.models import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'  # Includes all fields