import json

from django.urls import reverse_lazy

from clients.models import User
from clients.tests.factories import UserFactory
from clients.utils import WithLoginTestCase


class TestViews(WithLoginTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self) -> None:
        self.user1 = UserFactory(email='email1@email.com')
        self.user2 = UserFactory(email='email2@email.com', gender='famale')
        super().setUp()

    def test_create_client(self):
        data = {
            "username": "user32233",
            "password": "password",
            "first_name": "user2322",
            "last_name": "user2322",
            "email": "email22@email.com",
        }

        url = reverse_lazy('clients:create_client')
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        user = User.objects.filter(username=data['username']).first()   # type: User
        self.assertEqual(response.data['username'], user.username, response.data)
        self.assertEqual(response.data['first_name'], user.first_name, response.data)
        self.assertEqual(response.data['last_name'], user.last_name, response.data)
        self.assertEqual(response.data['email'], user.email, response.data)

    def test_like(self):

        self.auth_user(self.user1)
        url = reverse_lazy('clients:like', kwargs=dict(pk=self.user2.pk))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

        self.auth_user(self.user2)
        url = reverse_lazy('clients:like', kwargs=dict(pk=self.user1.pk))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_list(self):
        # все пользователи
        url = reverse_lazy('clients:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # фильтр
        url = reverse_lazy('clients:list') + '?gender=famale'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, response.data)
        self.assertEqual(response.data[0]['id'], self.user2.pk, response.data)