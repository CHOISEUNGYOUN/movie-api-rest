from rest_framework import serializers

from movies import models

class MovieSerializer(serializers.ModelSerializer):
    genres   = serializers.SerializerMethodField()
    torrents = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = (
            "title",
            "url",
            "title_english",
            "title_long",
            "year",
            "rating",
            "genres",
            "runtime",
            "summary",
            "description_full",
            "synopsis",
            "language",
            "mpa_rating",
            "background_image",
            "background_image_original",
            "small_cover_image",
            "medium_cover_image",
            "large_cover_image",
            "date_uploaded",
            "date_added",
            "torrents",
        )
        
    def get_torrents(self, obj):
        torrents = models.Torrent.objects.filter(movie=obj.pk)
        torrents = [{
            "url"           : t.url,
            "quality"       : t.quality,
            "type"          : t.type,
            "seeds"         : t.seeds,
            "peers"         : t.peers,
            "size"          : t.size,
            "size_bytes"    : t.size_bytes,
            "date_uploaded" : t.date_uploaded,
        } for t in torrents]
        return torrents 

    def get_genres(self, obj):
        genres = obj.genres.values("genres")
        return [g["genres"] for g in genres ]
