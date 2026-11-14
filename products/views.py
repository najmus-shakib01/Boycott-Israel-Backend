from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Category, Company, Product
from .serializers import CategorySerializer, CompanySerializer, ProductSerializer

class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })

@method_decorator(cache_page(60 * 15), name='get')
@method_decorator(cache_control(public=True, max_age=300, s_maxage=1800, stale_while_revalidate=86400), name='get')
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().only("id", "name")
    serializer_class = CategorySerializer

@method_decorator(cache_control(public=True, max_age=60, s_maxage=300, stale_while_revalidate=86400), name='get')
class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Company.objects.all().only("id", "name", "logo")
        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(name__istartswith=search)

        return queryset

@method_decorator(cache_control(public=True, max_age=60, s_maxage=300, stale_while_revalidate=86400), name='get')
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name', 'company__name']
    search_fields = ['company__name', 'category__name', 'description', 'owned_by']

    def get_queryset(self):
        queryset = Product.objects.select_related(
            "company",
            "category",
        ).all().order_by("-created_at")

        category = self.request.query_params.get('category')
        company = self.request.query_params.get('company')
        custom_search = self.request.query_params.get('search')

        if category and category != "all":
            queryset = queryset.filter(category__name=category)

        if company and company != "all":
            queryset = queryset.filter(company__name=company)

        if custom_search:
            queryset = queryset.filter(company__name__istartswith=custom_search)

        return queryset

@method_decorator(cache_control(public=True, max_age=120, s_maxage=600, stale_while_revalidate=86400), name='get')
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("company", "category").all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
