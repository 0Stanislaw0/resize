from django.urls import path, include
from . import api_view
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('send/', api_view.send_image, name='send'),
    path('get/<str:task_id>/', api_view.get_image, name='get'),
    path('cansel_task/<str:task_id>/', api_view.cansel_task, name='cansel'),
]

urlpatterns+=doc_urls