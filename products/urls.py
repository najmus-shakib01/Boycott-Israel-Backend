from django.urls import path
from .views import (
    products_root,
    CategoryListCreateView,
    CompanyListCreateView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', products_root, name='products-root'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('list/', ProductListCreateView.as_view(), name='product-list'),
    path('list/<uuid:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
