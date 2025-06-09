from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlobPhoto, BlobVideo
from .serializers import BlobPhotoSerializer, BlobVideoSerializer

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
    
class BlobPhotoListCreateView(generics.ListCreateAPIView):
    queryset = BlobPhoto.objects.all().order_by('-created_at')
    serializer_class = BlobPhotoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['photoTitle']

class BlobPhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlobPhoto.objects.all()
    serializer_class = BlobPhotoSerializer
    lookup_field = 'pk'

class BlobVideoListCreateView(generics.ListCreateAPIView):
    queryset = BlobVideo.objects.all().order_by('-created_at')
    serializer_class = BlobVideoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['videoTitle']

class BlobVideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlobVideo.objects.all()
    serializer_class = BlobVideoSerializer
    lookup_field = 'pk'