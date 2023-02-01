from django.shortcuts import render
from rest_framework import viewsets

from .models import Title, Category
from .serializers import TitleSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


#
# Create your views here.
class TitleViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'name', 'category')


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
