from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Post.objects.filter(
                Q(is_active=True) | Q(author=self.request.user))
        else:
            qs = Post.objects.filter(is_active=True)
        return qs

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
