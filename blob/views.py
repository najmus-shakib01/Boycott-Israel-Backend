from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlobPhoto, BlobVideo
from .serializers import BlobPhotoSerializer, BlobVideoSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def blob_root(request, format=None):
    """
    Blob & Media Gallery API Root
    Directory of endpoints for Gaza photo and video gallery.
    """
    return Response({
        "status": True,
        "message": "Blob Media Gallery API Root",
        "data": {
            "photos": {
                "url": reverse('blob-photo', request=request, format=format),
                "methods": ["GET", "POST"],
                "description": "গাজার ফটো গ্যালারির তালিকা (ফিল্টার: search=photoTitle, page=1)",
            },
            "videos": {
                "url": reverse('blob-video', request=request, format=format),
                "methods": ["GET", "POST"],
                "description": "গাজার ভিডিও গ্যালারির তালিকা (ফিল্টার: search=videoTitle, page=1)",
            },
        }
    })


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

@method_decorator(cache_control(public=True, max_age=120, s_maxage=600, stale_while_revalidate=86400), name='get')
class BlobPhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = BlobPhotoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['photoTitle']

    def get_queryset(self):
        queryset = BlobPhoto.objects.all().only(
            "id", "photoTitle", "photo", "created_at"
        ).order_by("-created_at")
        return queryset

@method_decorator(cache_control(public=True, max_age=300, s_maxage=1800, stale_while_revalidate=86400), name='get')
class BlobPhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlobPhoto.objects.all().only("id", "photoTitle", "photo", "created_at")
    serializer_class = BlobPhotoSerializer
    lookup_field = 'pk'

@method_decorator(cache_control(public=True, max_age=120, s_maxage=600, stale_while_revalidate=86400), name='get')
class BlobVideoListCreateView(generics.ListCreateAPIView):
    serializer_class = BlobVideoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['videoTitle']

    def get_queryset(self):
        queryset = BlobVideo.objects.all().only(
            "id", "videoTitle", "video", "created_at"
        ).order_by("-created_at")
        return queryset

@method_decorator(cache_control(public=True, max_age=300, s_maxage=1800, stale_while_revalidate=86400), name='get')
class BlobVideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlobVideo.objects.all().only("id", "videoTitle", "video", "created_at")
    serializer_class = BlobVideoSerializer
    lookup_field = 'pk'
