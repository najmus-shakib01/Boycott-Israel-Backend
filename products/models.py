from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=500)
    logo = models.CharField(max_length=2000, default='')

    def __str__(self):
         return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    owned_by = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name}"