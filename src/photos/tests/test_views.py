import json
from rest_framework import status
from django.test import TestCase
# from photos.models import Photo
from rest_framework.test import APIClient

client = APIClient()
BASE_URL = '/api/v1/'


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
            BASE_URL + 'photos'
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
                BASE_URL + 'photos',
                {
                    'name': 'sapi australia',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'p',
                },
                format='multipart'
            )
        obj_id = response.data['id']
        published_at = response.data['published_at']
        self.assertIs(status.is_success(response.status_code), True)
        self.assertNotEqual(published_at, None)

        # Get all photo
        response = client.get(
            BASE_URL + 'photos'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

        # Get individual photo
        response = client.get(
            BASE_URL + 'photo/' + str(obj_id)
        )
        self.assertIs(status.is_success(response.status_code), True)

    def test_03_post_draft_photo_user(self):
        # Post a new draft photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
                {
                    'name': 'sapi australia',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'd',
                },
                format='multipart'
            )
        obj_id = response.data['id']
        published_at = response.data['published_at']
        self.assertIs(status.is_success(response.status_code), True)
        self.assertEqual(published_at, None)

        # Update photo status to published
        photo_status = 'p' #published
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            {
                'status': photo_status,
            },
            format='json'
        )
        self.assertIs(status.is_success(response.status_code), True)
        self.assertEqual(photo_status, response.data['status'])

    def test_04_bad_request_post(self):
        # Post a bad request photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
                {
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                },
                format='multipart'
            )
        self.assertIs(status.is_client_error(response.status_code), True)

    def test_05_unknown_photo_id(self):
        # Photo is not found
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        response = client.get(
            BASE_URL + 'photo/qweasdzxc/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_06_update_captions_and_status(self):
        # Post a new published photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
                {
                    'name': 'sapi australia',
                    'file': fp,
                    'captions': 'Sapi australia #sapi',
                    'status': 'p',
                },
                format='multipart'
            )
        obj_id = response.data['id']
        photo_status = response.data['published_at']
        self.assertIs(status.is_success(response.status_code), True)
        self.assertNotEqual(photo_status, None)

        # Update the captions
        captions = 'Sapi bandung #sapi'
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            {
                'captions': captions,
            },
            format='json'
        )
        self.assertIs(status.is_success(response.status_code), True)
        self.assertEqual(captions, response.data['captions'])

        # Update photo status to draft
        photo_status = 'd' #draft
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            {
                'status': photo_status,
            },
            format='json'
        )
        self.assertIs(status.is_success(response.status_code), True)
        self.assertEqual(photo_status, response.data['status'])

        # Update captions and publish status
        photo_status = 'p' #published
        captions = 'Sapi bandung juara #sapi #juara'
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            {
                'captions': captions,
                'status': photo_status,
            },
            format='json'
        )
        self.assertIs(status.is_success(response.status_code), True)
        self.assertEqual(photo_status, response.data['status'])
        self.assertEqual(captions, response.data['captions'])

        # Update other field than captions
        error_message = 'only allow captions and status'
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            {
                'name': 'sapi bandung',
            },
            format='json'
        )
        self.assertIs(status.is_client_error(response.status_code), True)
        self.assertEqual(error_message, response.data['error'])

        # Bad request
        response = client.put(
            BASE_URL + 'photo/' + str(obj_id),
            '{"foo"}',
            format='json'
        )
        self.assertIs(status.is_client_error(response.status_code), True)

    def test_07_delete_photo(self):
        # Post a new published photo
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)
        with open('photos/tests/sapi.jpg', 'rb') as fp:
            response = client.post(
                BASE_URL + 'photos',
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

        # Delete the photo
        response = client.delete(
            BASE_URL + 'photo/' + str(obj_id)
        )
        self.assertIs(status.is_success(response.status_code), True)

        # Get deleted photo
        response = client.get(
            BASE_URL + 'photo/' + str(obj_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_08_get_filter_query_params(self):
        # Create client
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_token)

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

        # Get all photos, must return 2 records
        response = client.get(
            BASE_URL + 'photos'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 2)

        # Get all published photo, must return 1 record
        response = client.get(
            BASE_URL + 'photos?status=p'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

        # Get all draft photos, must return 1 record
        response = client.get(
            BASE_URL + 'photos?status=d'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

        # Get all photos sort asc
        response = client.get(
            BASE_URL + 'photos?sort=asc'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 2)

        # Get all photos sort desc
        response = client.get(
            BASE_URL + 'photos?sort=desc'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 2)

        # Get all published photo with sort, must return 1 record
        response = client.get(
            BASE_URL + 'photos?status=p&sort=asc'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)

        # Get all draft photos with sort, must return 1 record
        response = client.get(
            BASE_URL + 'photos?status=d&sort=desc'
        )
        photo_count = len(response.data)
        self.assertIs(status.is_success(response.status_code), True)
        self.assertIs(photo_count, 1)
