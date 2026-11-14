from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Browsable directory for the public Boycott Israel v1 API modules.
    """
    return Response({
        "status": "ok",
        "message": "Boycott Israel API is running",
        "version": "v1",
        "endpoints": {
            "products": reverse('products-root', request=request, format=format),
            "blob": reverse('blob-root', request=request, format=format),
            "contact": reverse('contact-form', request=request, format=format),
            "admin": request.build_absolute_uri('/admin/'),
        }
    })
