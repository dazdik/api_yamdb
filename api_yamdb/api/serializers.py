from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Titles, Category, Genres, GenresTitle
from django.forms.models import model_to_dict


class GenresSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Genres
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    #genre = GenresSerializer(many=True)

    class Meta:
        model = Titles
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        cat = model_to_dict(
            get_object_or_404(
                Category,
                slug=ret['category']
            ),
            fields=('name', 'slug')
        )
        ret['category'] = cat
        return ret

    # def create(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     else:
    #         genres = validated_data.pop('genre')
    #         title = Title.objects.create(**validated_data)
    #         for genre in genres:
    #             current_genre, status = Genres.objects.get_or_create(
    #                 **genre)
    #             GenresTitle.objects.create(
    #                 genre=current_genre, title=title)
    #         return title
