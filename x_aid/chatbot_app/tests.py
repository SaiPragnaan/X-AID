from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import io
import json
import os
import sys
from chatbot_app.models import Chat

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(PROJECT_ROOT, "ML"))

from scripts.chat_generation import text_generation
from scripts.image_prediction import predict

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_chatbot_message(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("chatbot"), json.dumps({"message": "Hello"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.json())

    def test_chatbot_image(self):
        self.client.login(username="testuser", password="testpass")
        img = Image.new("RGB", (224, 224))
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG")
        img_io.seek(0)

        response = self.client.post(reverse("chatbot"), {"image": img_io}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertIn("bot_reply", response.json())

    def test_login_success(self):
        """Test valid login."""
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "testpass"})
        self.assertRedirects(response, reverse("chatbot"))

    def test_login_failure(self):
        response = self.client.post(reverse("login"), {"username": "wronguser", "password": "wrongpass"})
        self.assertContains(response, "Invalid username or password.")

    def test_register_success(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "securepass",
            "password2": "securepass"
        })
        self.assertRedirects(response, reverse("chatbot"))
    
    def test_register_password_mismatch(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "password1",
            "password2": "password2"
        })
        self.assertContains(response, "Passwords don&#x27;t match")


    def test_logout(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))


BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
class ChatbotLogicTests(TestCase):
    def test_text_generation(self):
        response = text_generation("How does a person get Heart Attack ?")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

    def test_image_prediction(self):
        img = Image.open(os.path.join(BASE_DIR,"x_aid/test_images/pneumonia1.jpeg"))
        prediction = predict(img)
        self.assertIn("pneumonia", prediction.lower())  

