from rest_framework import serializers
from .models import BlobPhoto, BlobVideo

class BlobPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlobPhoto
        fields = ['id', 'photoTitle', 'photo', 'created_at']

class BlobVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlobVideo
        fields = ['id', 'videoTitle', 'video', 'created_at']