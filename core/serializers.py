from rest_framework.serializers import ModelSerializer

from .models import Comment, Post, Category


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
