from django.db import models
import uuid

class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.count}'