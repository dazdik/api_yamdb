from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet

router = DefaultRouter()
router.register('title', TitleViewSet)
router.register('category', CategoryViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
]
