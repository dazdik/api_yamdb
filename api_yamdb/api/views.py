import uuid

import django_filters
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Title, Genre, Category
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)
from .serializers import (
    GetTokenSerializer,
    SignUpSerializer,
    TitleSerializer,
    UserSerializer,
    UserRoleSerializer, GenresSerializer, CategorySerializer,
    TitleSerializerRead, TitleSerializerCreate
)
from users.models import User


#
# Create your views here.
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    # запрет на POST
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False,
        url_path='me',
        methods=('GET', 'PATCH',),
        permission_classes=(IsAuthenticated,),

    )
    def me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)

        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(
                role=user.role,
                confirmation_code=user.confirmation_code,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated and
            (self.request.user.is_admin or
             self.request.user.is_superuser)
        ):
            return UserSerializer
        return UserRoleSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        return Response(request.data, status=status.HTTP_200_OK)

    serializer.is_valid(raise_exception=True)
    user, email = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = str(uuid.uuid4())

    send_mail(
        'Регистрация на Yamdb',
        f'Используйте этот код {confirmation_code} для получения токена',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    username, confirmation_code = serializer.validated_data.values()
    user = get_object_or_404(User, username=username)

    if confirmation_code != str(user.confirmation_code):
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    refresh = RefreshToken.for_user(user)
    data = {'token': str(refresh.access_token)}

    return Response(data, status=status.HTTP_200_OK)
