import os
from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from rest_framework.test import APITestCase

from ..models import BaseModel, Media, MultipleAlbum, upload_to


class BaseModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='lolja',
            first_name='Oleg',
            last_name='Shmatko'
        )

        self.base_media = BaseModel.objects.create(
            media_user = self.user,
            media_text = 'lolja',
        )

        #base_media_logout = f'\nuser:  {self.user}\nbase_media: {self.base_media}'
        #print(base_media_logout)    

    def test_delete_user_base_model(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(BaseModel.objects.count(), 1)
        
        del_user = User.objects.get(pk=self.user.id)
        del_user.delete()

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(BaseModel.objects.count(), 0)

    def test_auto_now_data(self):
        self.assertEqual(self.base_media.media_date, date.today())

class MultipleAlbumTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='lolja',
            first_name='Oleg',
            last_name='Shmatko'
        )

        self.album_1 = MultipleAlbum.objects.create(
            media_user = self.user,
            media_text = 'lolja',
        )

        #base_media_logout = f'\nuser:  {self.user}\nbase_media: {self.base_media}'
        #print(base_media_logout)    

    def test_media_path(self):
        self.assertEqual(self.album_1.media_path, None)


class MediaTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create(
            username='lolja',
            first_name='Oleg',
            last_name='Shmatko'
        )

        self.album_1 = MultipleAlbum.objects.create(
            media_user = self.user,
            media_text = 'lolja',
        )

        self.file_name = 'test_models_file.txt'

        self.media_1 = Media.objects.create(
            media_user  = self.user,
            media_text  = 'lolja',
            media_path  = SimpleUploadedFile(f'{self.file_name}', b'Test file contents'),
            media_type  = 'photo',
        )
    def tearDown(self):
        now = datetime.now()
        if os.path.isfile(settings.BASE_DIR + settings.MEDIA_URL + str(self.media_1.media_path)):
            os.remove(settings.BASE_DIR + settings.MEDIA_URL + str(self.media_1.media_path))
        else:
            files = os.listdir(settings.BASE_DIR + settings.MEDIA_URL + now.strftime(f'media_storage/%Y/%m/%d/{self.user}/'))
            print(f"files: {files}")
        self.media_1.delete()
        self.album_1.delete()
        self.user.delete()

    def test_path_upload_to(self):
        now = datetime.now()
        expected_data = now.strftime(f'media_storage/%Y/%m/%d/{self.user}/{self.file_name}')
        self.assertEqual(expected_data, self.media_1.media_path)

    def test_add_media_in_album(self):
        self.media_1.media_album.add(self.album_1)
        self.assertIn(self.album_1, self.media_1.media_album.all())

    def test_media_type(self):
        expected_data = 'photo'
        self.assertEqual(str(self.media_1.media_type), expected_data)

