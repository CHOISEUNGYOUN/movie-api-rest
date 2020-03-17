from rest_framework import serializers

from movies import models

class TorrentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Torrent
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    genres = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.Genre
        fields = ('genres',)

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = models.Movie
        fields = '__all__'
        depth = 1
