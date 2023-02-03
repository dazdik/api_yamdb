from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenresViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('category', CategoryViewSet)
router.register('genres', GenresViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
]
