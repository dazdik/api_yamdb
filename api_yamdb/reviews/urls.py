from rest_framework import routers
from django.urls import path, include

from reviews.views import CommentViewSet, ReviewViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
# router_v1.register(r'review', ReviewViewSet, basename='Review')
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'title', TitleViewSet, basename='Title')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls))
]
