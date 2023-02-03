from pprint import pprint

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Title, Category, Genre
from django.forms.models import model_to_dict


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении."""
    category = CategorySerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    # rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = ('id',)


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при создании."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')
