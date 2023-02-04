from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.models import Title
from reviews.models import Review
from reviews.permissions import OwnerOrModeratorOrAdmin
from reviews.serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrModeratorOrAdmin)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrModeratorOrAdmin)
    pagination_class = LimitOffsetPagination

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


# class TitleViewSet(ModelViewSet):
#     serializer_class = TitleSerializer
#     queryset = Title.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
