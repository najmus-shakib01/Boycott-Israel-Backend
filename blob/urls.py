from django.urls import path
from .views import (
    BlobPhotoListCreateView,
    BlobPhotoRetrieveUpdateDestroyView, 
    BlobVideoListCreateView,
    BlobVideoRetrieveUpdateDestroyView
)

urlpatterns = [
    path('blob-photo/', BlobPhotoListCreateView.as_view(), name='blob-photo'),
    path('blob-photo/<uuid:pk>/', BlobPhotoRetrieveUpdateDestroyView.as_view(), name='blob-photo-detail'),

    path('blob-video/', BlobVideoListCreateView.as_view(), name='blob-video'),
    path('blob-video/<uuid:pk>/', BlobVideoRetrieveUpdateDestroyView.as_view(), name='blob-video-detail'),
]