from django.shortcuts import render
from rest_framework import viewsets

from .models import Title
from .serializers import TitleSerializer


#
# Create your views here.
class TitleViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
