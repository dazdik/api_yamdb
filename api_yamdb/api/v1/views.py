import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from api.v1.permissions import (
    IsAdmin, IsAdminOrReadOnly,
    OwnerOrModeratorOrAdmin
)
from api.v1 import serializers
from api.v1.mixins import CreateDestroyViewSet
from api.v1.filters import TitleFilter
from users.models import User


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-rating')
    serializer_class = serializers.TitleSerializerCreate
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return serializers.TitleSerializerCreate
        return serializers.TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с пользователями.
    Администратор имеет полные права доступа.
    Пользователь может просматривать и редактировать свой аккаунт.
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    # запрет на PUT
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
            serializer = serializers.UserSerializer(user, data=request.data,
                                                    partial=True)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(
                role=user.role,
                confirmation_code=user.confirmation_code,
            )
            return Response(serializer.data)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated and
            (
                self.request.user.is_admin
                or self.request.user.is_superuser
            )
        ):
            return serializers.UserSerializer
        return serializers.UserRoleSerializer


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    """
    Вью-функция регистрации нового пользователя.
    Отправка кода подтверждения на почту.
    """

    serializer = serializers.SignUpSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data)

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
    """Получение токена для авторизации."""

    serializer = serializers.GetTokenSerializer(data=request.data)
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование отзывов."""
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrModeratorOrAdmin)
    pagination_class = PageNumberPagination

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ReviewSerializerCreate
        return serializers.ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def perform_update(self, serializer):
        serializer.save(title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrModeratorOrAdmin)
    pagination_class = PageNumberPagination

    def get_review(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
