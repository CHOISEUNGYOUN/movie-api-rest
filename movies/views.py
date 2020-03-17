from rest_framework          import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views    import APIView
from rest_framework.response import Response

from . import models, serializers

class MovieListView(ListCreateAPIView):

    serializer_class = serializers.MovieSerializer

    def post(self, request):
        data = request.data
        serializer = serializers.MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_m = models.Movie.objects.create(
            url                       = data.get("url",""),
            title                     = data["title"],
            title_english             = data.get("title_english",""),
            title_long                = data.get("title_long",""),
            year                      = int(data["year"]),
            rating                    = int(data["rating"]),
            runtime                   = int(data.get("runtime",0)),
            summary                   = data["summary"],
            description_full          = data.get("description_full",""),
            synopsis                  = data.get("synopsis",""),
            language                  = data.get("language",""),
            mpa_rating                = data.get("mpa_rating",""),
            background_image          = data.get("background_image",""),
            background_image_original = data.get("background_image_original",""),
            small_cover_image         = data.get("small_cover_image",""),
            medium_cover_image        = data.get("medium_cover_image",""),
            large_cover_image         = data.get("large_cover_image",""),
            )
        if "genre" not in data:
            return Response(data="Genre is required", status=status.HTTP_400_BAD_REQUEST)

        if models.Genre.objects.filter(genres=data["genre"]).exists():
            genre = models.Genre.objects.get(genres=data["genre"])
        else:
            genre = models.Genre.objects.create(genres=data["genre"])
        new_m.genres.add(genre)

        return Response(data="Upload succeeded", status=status.HTTP_201_CREATED)

    def get_queryset(self):
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
