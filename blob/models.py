from django.db import models
import uuid

class BlobPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photoTitle = models.TextField()
    photo = models.CharField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.photoTitle}'
    
class BlobVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    videoTitle = models.TextField()
    video = models.CharField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.videoTitle}'