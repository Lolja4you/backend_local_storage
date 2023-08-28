import os
from datetime import datetime, date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from rest_framework.test import APITestCase


from ..models import Media, MultipleAlbum, upload_to
from ..serializers import MultipleFileSerializer

class MultipleFileSerializerTestCase(APITestCase):
    
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

        self.media_1 = Media.objects.create(
            media_user  = self.user,
            media_text  = 'lolja',
            media_path  =  SimpleUploadedFile('test_file.txt', b'Test file contents'),
            media_type  = 'photo',
        )

        #print(f'media_path: {self.media_1.media_path}')

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
    
    def test_is_valid_data(self):
        self.assertTrue(MultipleFileSerializer(self.media_1).is_valid)
    
    def test_MultipleFileSerializer(self):
        serializer = MultipleFileSerializer(instance=self.media_1)
        serialized_data = serializer
        expected_data = {
            'id'         : self.media_1.id,
            'media_date' : datetime.now().strftime('%Y-%m-%d'),
            'media_text' : 'lolja',
            'media_path' : self.media_1.media_path,
            'media_type' : 'photo',
            'media_user' : self.user.id,
            'media_album': [],
        }
        print(f'\nexpected_data: {expected_data}')
        print(f'\ndata: {serialized_data}')
