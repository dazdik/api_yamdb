from rest_framework import serializers
from .models import Title, Category


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
