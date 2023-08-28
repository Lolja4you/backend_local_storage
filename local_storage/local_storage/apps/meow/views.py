from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from .models import MeowModel
from .serializers import MeowSerializer


class MeowView(APIView):
    def get(self, request, format=None):
        print("API Was Called")
        return Response("API Response Success", status=200)

class MeowTaskView(viewsets.ModelViewSet):
    serializer_class = MeowSerializer
    def get_queryset(self):
        return MeowModel.objects.all()