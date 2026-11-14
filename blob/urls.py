from django.urls import path
from .views import (
    blob_root,
    BlobPhotoListCreateView,
    BlobPhotoRetrieveUpdateDestroyView, 
    BlobVideoListCreateView,
    BlobVideoRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', blob_root, name='blob-root'),
    path('blob-photo/', BlobPhotoListCreateView.as_view(), name='blob-photo'),
    path('blob-photo/<uuid:pk>/', BlobPhotoRetrieveUpdateDestroyView.as_view(), name='blob-photo-detail'),
    path('blob-video/', BlobVideoListCreateView.as_view(), name='blob-video'),
    path('blob-video/<uuid:pk>/', BlobVideoRetrieveUpdateDestroyView.as_view(), name='blob-video-detail'),
]
