from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Media, MultipleAlbum


class FileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class FileRetrieveSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Media
        fields = "__all__"


class FilePostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Media
        fields = ('media_text', 'media_path', 'media_album')


class FilePutSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.media_text = validated_data.get(
            'media_text', instance.media_text)
        instance.media_path = validated_data.get(
            'media_path', instance.media_path)
        media_album = validated_data.get('media_album')
        if media_album:
            instance.media_album.set(media_album)
        instance.save()
        return instance

    class Meta:
        model = Media
        fields = ('media_text', 'media_album',)


class MultipleAlbumSerializer(serializers.ModelSerializer):
    media_albums_multiple = FileAllSerializer(many=True, read_only=True)

    class Meta:
        model = MultipleAlbum
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Дополнительная логика, если требуется
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Определение пользователя (user) возвращается вместе с токеном
    @classmethod
    def get_token(cls, user):  # Вместе с обновлениями полученного токена Django REST Framework Simple JWT переименовал этот метод на обновленную версию
        token = super().get_token(user)
        # Добавьте свои нужные поля пользователя
        token['user_id'] = user.id
        return token
