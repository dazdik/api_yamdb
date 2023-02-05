from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, UserViewSet, get_token, signup
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
