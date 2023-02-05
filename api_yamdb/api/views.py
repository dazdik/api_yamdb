import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from .models import Category, Genre, Title
from .serializers import (
    TitleSerializerCreate,
    CategorySerializer,
    GenresSerializer,
    TitleSerializerRead
)
from rest_framework.pagination import PageNumberPagination


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
