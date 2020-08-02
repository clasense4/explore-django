from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Photo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Photo
        exclude = ['file']


class UserPhotoSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'name', 'captions', 'image_small', 'image_medium', 'image_large', 'published_at']
