from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from .models import Category, Genre, Title
from .serializers import TitleSerializer, CategorySerializer, GenresSerializer
from rest_framework.pagination import PageNumberPagination


# from django_filters.rest_framework import DjangoFilterBackend


#
# Create your views here.
class TitlesViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        category_type = self.request.data.get('category')
        category = get_object_or_404(Category, slug=category_type)
        return serializer.save(category=category)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
