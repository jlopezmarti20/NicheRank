from rest_framework import serializers
from .models import userInfo
from .models import Songs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=userInfo
        fields= ['name']

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Songs
        fields=('country','uri','name','artist','explicit','genres','danceability','energy','key','loudness','speechiness','acoustics','instrumentalness','liveliness','valence','tempo','duration_seconds')