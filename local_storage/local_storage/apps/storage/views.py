from rest_framework import viewsets, exceptions, generics
from rest_framework.response import Response
from rest_framework import permissions


from .models import MultipleAlbum, Media
from .permissions import IsAuthenticatedModeratorAndAuthor
from .serializers import (
    MultipleAlbumSerializer,
    FileAllSerializer,
    FilePutSerializer,
    FileRetrieveSerializer,
    FilePostSerializer,
    UserSerializer
)


class MultipleFileUploadView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedModeratorAndAuthor]

    def return_determine_type_files(self, file_type):
        video_extensions = ['mp4', 'avi', 'mov', 'mkv',
                            'wmv', 'flv', 'webm', 'mpeg', '3gp', 'ogg', 'rm']
        photo_extensions = ["png", "jpg", "jpeg", "gif", "bmp", "tiff"]

        if file_type.split('.')[-1] in video_extensions:
            return 'video'
        elif file_type.split('.')[-1] in photo_extensions:
            return 'photo'
        else:
            raise exceptions.ValidationError('error: invalid file type')

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return FileAllSerializer
        elif self.request.method == 'POST':
           return FilePostSerializer
        elif self.request.method == 'RETRIEVE':
           return FileRetrieveSerializer
        elif self.request.method == 'PUT':
           return FilePutSerializer
        else:
            return FileAllSerializer

    def get_queryset(self):
        return Media.objects.filter(media_user=self.request.user)

    def perform_create(self, serializer):
       file_type = str(self.request.__dict__['_files']['media_path'])
       serializer.save(
           media_type=self.return_determine_type_files(file_type),
           media_user=self.request.user,
       )


class MultipleAlbumView(viewsets.ModelViewSet):
    serializer_class = MultipleAlbumSerializer

    def get_queryset(self):
        return MultipleAlbum.objects.all()


class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
