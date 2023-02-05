import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.'
            )

        if not re.match(r'^[\w.@+-]', value):
            raise serializers.ValidationError(
                f'Неверный формат {value}.'
            )
        return value


class UserRoleSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role', )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate_username(self, username):
        return UserSerializer.validate_username(self, username)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError('Пользователь не существует')
        if confirmation_code is None:
            raise serializers.ValidationError('Код отстутствует')
        return data


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
