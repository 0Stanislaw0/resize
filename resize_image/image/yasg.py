from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API",
      contact=openapi.Contact(email="stas.yyyy20@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

post_resize = openapi.Schema(
    type=openapi.IN_FORM,
    required=['image_file','height','width'],
    example={
        'image_file': 'image.jpeg',
        'height': 128,
        'width': 128,
    }
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
