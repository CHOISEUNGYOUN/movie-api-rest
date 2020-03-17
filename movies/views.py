import json

from rest_framework.generics import ListAPIView

from . import models, serializers

class MissingRequiredValue(Exception):
        pass

class MovieListView(ListAPIView):

    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
