from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=500, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=500, db_index=True)
    logo = models.CharField(max_length=2000, default='')

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
         return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='products',
        db_index=True,
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        db_index=True,
    )
    owned_by = models.CharField(max_length=500, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["company", "category"]),
        ]

    def __str__(self):
        return f"{self.company.name}"