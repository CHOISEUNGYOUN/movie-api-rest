import json

from rest_framework.generics import ListAPIView

from . import models, serializers

class MissingRequiredValue(Exception):
        pass

class MovieListView(ListAPIView):

    serializer_class = serializers.MovieSerializer

    def get_queryset(self):
        print(self.request.query_params)
        queryset = models.Movie.objects.all()
        page     = int(self.request.query_params.get("page", 1))
        limit    = int(self.request.query_params.get("limit", 20))
        limit    = limit if limit <= 50 else 20
        end      = 0
        if page == 1:
            offset = 0
            end    = limit
        else:
            offset = (page - 1) * limit
            end    = page * limit

        order_by = self.request.query_params.get("order_by", "desc")
        sort_by  = self.request.query_params.get("sort_by", "date_added")
        filter_queries = self.request.query_params
        movie_filter = {}
        for k,v in filter_queries.items():
            if k == "minimum_rating":
                movie_filter[f] = v
            if k == "genre":
                genre = models.Genre.objects.get(genres=v).id
                movie_filter["genres"] = genre
        
        filtered_movie = queryset.filter(**movie_filter)
        
        if order_by == "desc":
            filtered_movie = filtered_movie.order_by(f"-{sort_by}")
        else:
            filtered_movie = filtered_movie.order_by(f"{sort_by}")

        return filtered_movie[offset:end]
