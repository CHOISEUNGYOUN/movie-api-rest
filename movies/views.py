import json

from rest_framework.generics import ListAPIView

from . import models, serializers

class MissingRequiredValue(Exception):
        pass

class MovieListView(ListAPIView):

    serializer_class = serializers.MovieSerializer

    def get_queryset(self):
        queryset = models.Movie.objects.all()
        return queryset

class TorrentListView(ListAPIView):

    serializer_class = serializers.MovieSerializer

    def get_queryset(self):
        queryset = models.Torrent.objects.all()
        return queryset
