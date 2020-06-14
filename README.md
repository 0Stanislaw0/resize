https://docs.google.com/document/d/1i1xxa2WpCFEellzIU8kI27StvWyTejqO5EiwoWYzg38/edit


## Выполнение тестового задания.

Использовал django потому что из предложенных технологий, знаком c ним больше всего.

django-rest-framework для реализации API.

celery для асинхронного выполнения ресайзинга.

redis в качестве брокера для celery.

и добавил drf-yasg для документации API.


Для работы с приложением выполните следующие шаги:

### 1. Создайте и активируйте виртуальное окружение:

###     
	virtualenv --python=python3.8 ./
	source ./bin/activate

### 2. Установите зависимости:

###     
	pip3 install -r requirements.txt

### 3. Запустите редис и  celery(проверьте настройки в settings.py):

###     
	redis-server
	celery worker -A resize_image --loglevel=info

### 4. Запустите сервер и перейдите на http://127.0.0.1:8000/swagger/:

###     
	python3 manage.py runserver






