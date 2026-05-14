from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class HabitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            'place': 'Home',
            'time': '08:00:00',
            'action': 'Read book',
            'duration': 60,
            'periodicity': 1,
            'is_pleasant': False
        }
        response = self.client.post(reverse('habit-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_duration_validation(self):
        data = {
            'place': 'Home',
            'time': '08:00:00',
            'action': 'Too long',
            'duration': 200,
            'periodicity': 1,
        }
        response = self.client.post(reverse('habit-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
