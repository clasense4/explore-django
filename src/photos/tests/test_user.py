import json
from rest_framework import status
from django.test import TestCase
# from photos.models import Photo
from rest_framework.test import APIClient

client = APIClient()
BASE_URL = '/api/v1/'


class UserTests(TestCase):
    user_token = ''

    def setUp(self):
        # Register new user
        response = client.post(
            '/registration/',
            {'username':'fajri2','password1':'passwordfajri2','password2':'passwordfajri2'},
            format='json'
        )
        self.user_token = response.data['token']

    def test_01_get_user_photos(self):
        # Create client
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)

        # Get all photos by user, initially it must show 0 data
        response = client.get(
            BASE_URL + 'user/fajri2'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 0)

        # Get all photos by random user
        response = client.get(
            BASE_URL + 'user/randomusernotexists'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # New published photo
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
                {
                    'name': 'sapi australia published',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'p',
                },
                format='multipart'
            )
        obj_id_published = response.data['id']
        self.assertIs(status.is_success(response.status_code), True)

        # New draft photo
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
                {
                    'name': 'sapi australia draft',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'd',
                },
                format='multipart'
            )
        draft_obj_id = response.data['id']
        self.assertIs(status.is_success(response.status_code), True)

        # Show public photos, must only show 1 result
        response = client.get(
            BASE_URL + 'user/fajri2'
        )

        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)