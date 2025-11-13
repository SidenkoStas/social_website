# social_website

## Оглавление
- [Обзор проекта](#обзор-проекта)
- [Технологии](#технологии)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Использование](#использование)

## Обзор проекта
Это веб-сайт, разработанный на Python с использованием Django. Проект предназначен для сохранения изображений из различных сайтов
с использование JS закладки. Пользователи могут просматривать изображения друг друга и ставить лайки.

## Технологии
- Python
- Django
- Easy thumbnails
- HTML, CSS, JavaScript
- Redis

## Установка
1. Клонируйте репозиторий:

```git
git clone https://github.com/SidenkoStas/social_website.git
```
2. Создайте виртуальное окружение и активируйте его:

```
python -m venv env
source env/bin/activate # Linux/macOS
env\Scripts\activate # Windows
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Создайте файл .env для переменных окружения формата:
```
SECRET_KEY=XXXXXXXX
DEBUG=XXXX
EMAIL_HOST=XXXXXXXX
EMAIL_HOST_USER=XXXXXXXX
EMAIL_HOST_PASSWORD=XXXXXXXX
EMAIL_PORT=XXXXXXXX
EMAIL_USE_SSL=XXXX
DEFAULT_FROM_EMAIL=XXXXXXXX

GOOGLE_OAUTH2_KEY=XXXXXXXX
GOOGLE_OAUTH2_SECRET=XXXXXXXX
```

5. Настройте возможность регистрации через Google

6. Установите образ Redis для docker (установите его, если не присутствует)
```
docker pull redis
```
7. Запустите контенер с Redis:
```
docker run -it --rm --name redis -p 6379:6379 redis
```

## Запуск проекта
1. Выполните миграции базы данных:
```python
python manage.py migrate
```
2. Запустите один из серверов разработки:
```python
python manage.py runserver
python manage.py runserver_plus --cert-file -cert.crt
```
3. Перейдите в браузере по адресу `http://127.0.0.1:8000`

## Использование
Для пользованием сервиса необходима регистрация для пользователей. С главной страницы пользователя перетащите закладку "Добавь" к себе, для сохранения изображений с других сайтов.

