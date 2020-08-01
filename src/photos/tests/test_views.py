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
        self.user_token = response.data['token']

    def test_00_get_auth_token_user(self):
        # Get auth token
        response = client.post(
            '/api-token-auth/',
            {'username':'fajri1','password':'passwordfajri1'},
            format='json'
        )
        self.assertIs(True, status.is_success(response.status_code))

    def test_01_get_user_photo_no_result(self):
        # New created user doesn't have any photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        response = client.get(
            '/api/v1/photo/'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 0)

    def test_02_post_published_photo_user(self):
        # Post a new published photo
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
        obj_id = response.data['id']
        self.assertIs(status.is_success(response.status_code), True)

        # Get all photo
        response = client.get(
            '/api/v1/photo/'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

        # Get individual photo
        response = client.get(
            '/api/v1/photo/' + str(obj_id) + '/'
        )
        self.assertIs(status.is_success(response.status_code), True)

    def test_03_post_draft_photo_user(self):
        # Post a new draft photo
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
        obj_id = response.data['id']
        self.assertIs(status.is_success(response.status_code), True)

        # TODO: Get all photo with status draft with query string
        # TODO: Get individual photo

    def test_04_bad_request_post(self):
        # Post a bad request photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                '/api/v1/photo/',
                {
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                },
                format='multipart'
            )
        self.assertIs(status.is_client_error(response.status_code), True)

