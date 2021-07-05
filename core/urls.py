from core.models import Post
from rest_framework.routers import DefaultRouter

from .views import PostViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = router.urls
