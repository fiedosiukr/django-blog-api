from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Post, Category


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        post = Post.objects.create(**validated_data)

        for category in categories_data:
            try:
                obj = Category.objects.get(name=category['name'])
            except Category.DoesNotExist:
                obj = Category.objects.create(name=category['name'])
            post.categories.add(obj)

        return post


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
