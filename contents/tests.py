import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, Type, User


class ArticleAuthoringAPITests(APITestCase):
    def setUp(self):
        self.article_list_url = reverse("articles")
        self.image_upload_url = reverse("article-upload-image")
        self.category = Type.objects.create(name="DIY")

        self.author_user = User.objects.create_user(
            username="author-user",
            email="author@example.com",
            first_name="Author",
            last_name="User",
            profession="Writer",
            phone_number="1234567890",
            is_author=True,
            password="Passw0rd!123",
        )

        self.regular_user = User.objects.create_user(
            username="regular-user",
            email="regular@example.com",
            first_name="Regular",
            last_name="User",
            profession="Reader",
            phone_number="0987654321",
            is_author=False,
            password="Passw0rd!123",
        )

    def _get_test_image(self, name="cover.png"):
        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2p7xkAAAAASUVORK5CYII="
        )
        return SimpleUploadedFile(name, png_bytes, content_type="image/png")

    def test_unauthenticated_user_cannot_create_article(self):
        payload = {
            "title": "Unauthorized create",
            "content": "<p>Body</p>",
            "type": self.category.id,
            "image": self._get_test_image(),
        }

        response = self.client.post(
            self.article_list_url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_author_user_cannot_create_article(self):
        self.client.force_authenticate(user=self.regular_user)
        payload = {
            "title": "Forbidden create",
            "content": "<p>Body</p>",
            "type": self.category.id,
            "image": self._get_test_image(),
        }

        response = self.client.post(
            self.article_list_url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_create_article(self):
        self.client.force_authenticate(user=self.author_user)
        payload = {
            "title": "My first article",
            "content": "<p>Hello from author</p>",
            "type": self.category.id,
            "image": self._get_test_image(),
        }

        response = self.client.post(
            self.article_list_url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().author, self.author_user)

    def test_rich_content_is_sanitized(self):
        self.client.force_authenticate(user=self.author_user)
        payload = {
            "title": "Sanitized article",
            "content": '<p>Safe</p><script>alert("xss")</script>',
            "type": self.category.id,
            "image": self._get_test_image(),
        }

        response = self.client.post(
            self.article_list_url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("<p>Safe</p>", response.data["content"])
        self.assertNotIn("<script>", response.data["content"])

    def test_author_can_upload_rich_text_image(self):
        self.client.force_authenticate(user=self.author_user)
        response = self.client.post(
            self.image_upload_url,
            {"image": self._get_test_image(name="inline.png")},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("url", response.data)
