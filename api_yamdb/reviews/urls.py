from rest_framework import routers
from django.urls import path, include

from reviews.views import CommentViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
# router_v1.register(r'review', ReviewViewSet, basename='Review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
# router_v1.register(r'title', TitleViewSet, basename='Title')

urlpatterns = [
    path('auth/', include('djoser.urls')), # just for debug, delete before prod review
    path('auth/', include('djoser.urls.jwt')), # just for debug, delete before prod review
    path('', include(router_v1.urls))
]
