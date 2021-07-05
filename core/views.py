from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, ]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
