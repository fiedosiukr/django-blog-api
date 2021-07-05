from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


class PostViewSetTest(APITestCase):

    def setUp(self):
        self.staffuser = User.objects.create(
            username='staffuser', password='staffpass', is_staff=True)
        self.normaluser = User.objects.create(
            username='normaluser', password='normpass', is_staff=False)
        self.post = Post.objects.create(
            title='Title', content='Content', author=self.staffuser)
        self.data = {
            "categories": [{"name": "Random"}, {"name": "Special"}],
            "title": "Second post",
            "content": "Content",
            "is_active": "true"
        }

    def test_get_posts(self):
        """
        Ensures anyone can display all posts.
        """
        url = reverse('posts-list')
        response = self.client.get(url)
        result = response.json()
        serializer = PostSerializer(self.post)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, result)

    def test_valid_create_post(self):
        """
        Ensures that staff user is able to create a post.
        """
        url = reverse('posts-list')
        self.client.force_login(user=self.staffuser)
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, 'Second post')

    def test_invalid_create_post(self):
        """
        Ensures that normal iser is not able to create a post.
        """
        url = reverse('posts-list')
        self.client.force_login(user=self.normaluser)
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.last().title, 'Title')

    def test_valid_get_single_post(self):
