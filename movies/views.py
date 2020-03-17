import json

from django.http                  import JsonResponse
from django.views                 import View

from . import models

class MissingRequiredValue(Exception):
        pass

class MovieListView(View):
    
    def get(self, request):
        pass
