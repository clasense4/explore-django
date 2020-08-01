import json
from rest_framework import status
from django.test import TestCase
# from photos.models import Photo
from rest_framework.test import APIClient

client = APIClient()


class RegisterUserTests(TestCase):

    user_token = ''

    def setUp(self):
        # Register new user
        response = client.post(
            '/registration/',
            {'username':'fajri1','password1':'passwordfajri1','password2':'passwordfajri1'},
            format='json'
        )
        print(response.data)
        self.user_token = response.data['token']

    def test_00_get_auth_token_user(self):
        response = client.post(
            '/api-token-auth/',
            {'username':'fajri1','password':'passwordfajri1'},
            format='json'
        )
        self.assertIs(True, status.is_success(response.status_code))
        # self.assertEqual(self.user_token, response.data['token'])

    def test_01_get_user_photo_no_result(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        response = client.get(
            '/api/v1/photo/'
        )

        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 0)

    def test_02_post_published_photo_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                '/api/v1/photo/',
                {
                    'name': 'sapi australia',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'p',
                },
                format='multipart'
            )

        print(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        response = client.get(
            '/api/v1/photo/'
        )

        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

    def test_03_post_draft_photo_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                '/api/v1/photo/',
                {
                    'name': 'sapi australia',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'd',
                },
                format='multipart'
            )

        print(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        response = client.get(
            '/api/v1/photo/'
        )

        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)
