from rest_framework import serializers
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class ReviewSerializeCreaate(ReviewSerializer):

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        # title = Title.objects.get(pk=title_id)
        if Review.objects.filter(title=title_id,
                                 author=self.context['request'].user).exists():
            raise serializers.ValidationError(
                "Unique constraint violated: You've already left review for this title")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
