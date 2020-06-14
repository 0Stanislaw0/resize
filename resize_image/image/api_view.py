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




logger = logging.getLogger(__name__)

@api_view(["post"])
@permission_classes((AllowAny,))
def send_image(request):
    if request.POST and request.FILES:
        file_path = os.path.join(
            settings.IMAGES_DIR, request.FILES['image_file'].name)
        with open(file_path, 'wb+') as fp:
            for chunk in request.FILES['image_file']:
                fp.write(chunk)
        h = int(request.POST.get('height'))
        w = int(request.POST.get('width'))
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


@api_view(["get"])
@permission_classes((AllowAny,))
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


@api_view(["delete"])
@permission_classes((AllowAny,))
def cansel_task(request, task_id):
    abortable_task = AbortableAsyncResult(task_id)
    abortable_task.abort()
    return Response({
        'result': 'Task was canseled'},
        status=HTTP_200_OK)


