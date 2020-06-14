from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT)
from .tasks import make_thumbnails
from celery.contrib.abortable import AbortableAsyncResult
from time import sleep

class TestApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.image = SimpleUploadedFile("file.jpg", b"file_content", content_type="multipart/form-data") 
        self.data = {'height': 1280,'width': 1280,'image_file':self.image}
        self.task = make_thumbnails.delay('~/Изображения/CalBX-T48fY.jpg', thumbnails=[(128, 128)]) # указать путь к изображению

    def tearDown(self):
        self.client = None
        self.image = None
        self.data = None
        self.task = None
        

    def test_send_image(self):

        response = self.client.post('/send/', self.data)
        self.assertEqual(response.status_code,HTTP_201_CREATED)

    def test_send_image_fail(self):

        response = self.client.post('/send/', {'height': 1280,
                                               'width': 10000,
                                               'image_file':self.image})
        response2 = self.client.post('/send/', {'height': 0,
                                               'width': 1280,
                                               'image_file':self.image})
        response3 = self.client.post('/send/', {'height': 1280,
                                               'width': 1280,
                                               'image_file':""})

        self.assertEqual(response.status_code,HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code,HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code,HTTP_400_BAD_REQUEST)
    
    def test_get_task_id(self):
        task = self.task
        response = self.client.get(f'/get/{task.id}/')
        self.assertEqual(response.status_code,HTTP_204_NO_CONTENT)
        sleep(1)
        response2 = self.client.get(f'/get/{task.id}/')
        self.assertEqual(response2.status_code,HTTP_200_OK)
        self.assertEqual(task.status,"SUCCESS")

    
    def test_get_task_id_fail(self):
        response = self.client.get(f'/get/999/')
        self.assertEqual(response.status_code,HTTP_204_NO_CONTENT)


    def test_cansel_task(self):
        response = self.client.delete(f'/cansel_task/{self.task.id}/')
        self.assertEqual(response.status_code,HTTP_204_NO_CONTENT)
