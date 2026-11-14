from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "status": "healthy",
        "service": "Boycott Israel Backend API",
        "endpoints": {
            "admin": "/admin/",
            "products": "/api/v1/products/list/",
            "categories": "/api/v1/products/categories/",
            "photos": "/api/v1/blob/blob-photo/",
            "videos": "/api/v1/blob/blob-video/",
            "contact": "/api/v1/contact/",
        }
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/blob/', include('blob.urls')),
    path('api/v1/contact/', include('contact.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
