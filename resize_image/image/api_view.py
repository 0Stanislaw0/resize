import os
import logging
from celery import current_app
from celery.contrib.abortable import AbortableAsyncResult
from django.conf import settings
from .tasks import make_thumbnails
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .yasg import post_resize


logger = logging.getLogger(__name__)

@swagger_auto_schema(method='post',
    request_body=post_resize,
    responses={
        '201': 'CREATED'
    },
    operation_id='Постановка задачи на изменение размера',)
@api_view(["post"])
def send_image(request):
    if request.POST and request.FILES:
        file_path = os.path.join(
            settings.IMAGES_DIR, request.FILES['image_file'].name)
        with open(file_path, 'wb+') as fp:
            for chunk in request.FILES['image_file']:
                fp.write(chunk)
        try:
            h = int(request.POST.get('height'))
            w = int(request.POST.get('width'))
        except ValueError as e:
            return Response(status=HTTP_400_BAD_REQUEST)
            
        if 9999 > h > 1 and 9999 > w > 1:
            task = make_thumbnails.delay(file_path, thumbnails=[(h, w)])
            return Response({
                'task_id': task.id,
                'task_status': task.status},
                status=HTTP_201_CREATED)
        else:
            logger.debug("Введены некорректные данные")
            return Response(status=HTTP_400_BAD_REQUEST)

    return Response(status=HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
    responses={
        '200': 'OK',
        '204': 'NO_CONTENT'
    },
    operation_id='Получение статуса задачи',)
@api_view(["get"])
def get_image(request, task_id):
    task = current_app.AsyncResult(task_id)
    if task.status == 'SUCCESS':
        logger.info(task.id+'  '+ task.status)
        return Response({
            'task_status': task.status,
            'task_id': task.id,
            'result': task.get()
        },status=HTTP_200_OK)

    return Response({
        'task_status': task.status,
        'task_id': task.id},
        status=HTTP_204_NO_CONTENT)

@swagger_auto_schema(method='delete',
    responses={
        '204': 'NO_CONTENT'
    },
    operation_id='Удаление задачи',)
@api_view(["delete"])
@permission_classes((AllowAny,))
def cansel_task(request, task_id):
    abortable_task = AbortableAsyncResult(task_id)
    abortable_task.abort()
    return Response({
        'result': 'Task was canseled'},
        status=HTTP_204_NO_CONTENT)


