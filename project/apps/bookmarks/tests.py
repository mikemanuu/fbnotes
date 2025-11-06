from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Bookmark

User = get_user_model()

class BookmarkAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        self.client.login(username="test", password="pass")

    def test_create_bookmark(self):
        url = reverse("bookmarks-list")  # DRF router name
        data = {"title": "title", "url": "https://example.com"}
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, 201)
        self.assertTrue(Bookmark.objects.filter(user=self.user).exists())
