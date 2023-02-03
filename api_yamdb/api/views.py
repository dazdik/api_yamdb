from rest_framework import viewsets
from rest_framework import viewsets, mixins, filters
from .models import Category, Genre, Title
from .serializers import (
    TitleSerializerCreate,
    CategorySerializer,
    GenresSerializer,
    TitleSerializerRead
)
from rest_framework.pagination import PageNumberPagination


# from django_filters.rest_framework import DjangoFilterBackend
class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    # permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(CreateDestroyViewSet):
    """
    Класс для работы с Post url запросами и передачей данных в PostSerializer
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
