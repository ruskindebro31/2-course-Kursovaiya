from rest_framework import serializers
from .models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('author', 'views', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')
