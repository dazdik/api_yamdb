from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, UserViewSet, get_token, signup

router = DefaultRouter()
router.register('title', TitleViewSet)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
