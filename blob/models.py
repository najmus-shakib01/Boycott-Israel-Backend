from django.db import models
import uuid

class BlobPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photoTitle = models.TextField(db_index=True)
    photo = models.CharField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["photoTitle"]),
        ]

    def __str__(self):
        return f'{self.photoTitle}'

class BlobVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    videoTitle = models.TextField(db_index=True)
    video = models.CharField(max_length=2000, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["videoTitle"]),
        ]

    def __str__(self):
        return f'{self.videoTitle}'