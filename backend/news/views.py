from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Article, Comment
from .serializers import CategorySerializer, ArticleSerializer, CommentSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Article.objects.filter(is_published=True)
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if instance.author == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied()


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def article_comments(request, article_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=article_id, is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST' and request.user.is_authenticated:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
