from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


def upload_to(user, filename):
    now = datetime.now()
    return now.strftime(f'media_storage/%Y/%m/%d/{user.media_user}/{filename}')

class BaseModel(models.Model):
    media_user    = models.ForeignKey(User, on_delete=models.CASCADE)
    media_date    = models.DateField(auto_now=True)
    media_text    = models.TextField(help_text="note" ,verbose_name='note')

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'

class MultipleAlbum(BaseModel):
    media_path    = None

    def __str__(self):
        return f'Album: {self.media_text}'

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

class Media(BaseModel):
    MEDIA_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    media_path    = models.FileField(upload_to=upload_to)
    media_type = models.CharField(max_length=5, choices=MEDIA_CHOICES)
    media_album = models.ManyToManyField(MultipleAlbum, related_name='media_albums_multiple', null=True, blank=True)

    def __str__(self) -> str:
        return f'note: {self.media_text} -- path: {self.media_path}'
     
    
    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'