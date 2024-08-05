# dataprocesshub

## Описание проекта
Сервис для обработки загружаемых документов, который позволяет зарегистрированным пользователям загружать документы через API. Администратор платформы получает уведомление по электронной почте при загрузке нового документа и может подтверждать или отклонять документы через Django admin. После этого пользователи получают уведомления по электронной почте о статусе их документов. Для обработки уведомлений используется система очередей.

## Функционал

1. **Загрузка документов зарегистрированными пользователями через API.**
2. **Уведомление администратора по электронной почте при загрузке нового документа.**
3. **Просмотр, подтверждение и отклонение загруженных документов через Django admin.**
4. **Уведомление пользователей по электронной почте о статусе их документов (подтвержден или отклонен).**
5. **Использование системы очередей для обработки уведомлений.** 

## ВАЖНО!!!
При добавлении документа зарегистрированным пользователем, создается запись о документе в базе данных, сам файл отправляется в облачное хранилище Yandex Cloud, если администратор отклоняет документ, запись остается в базе данных, но файл из облачного хранилища удаляется!

## Технические требования

- **Фреймворк**: Django, Django Rest Framework (DRF)
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose
- **Очередь сообщений**: Celery
- **Отправка уведомлений**: Отправка email через SMTP-сервер Gmail
- **Документация**: Автогенерируемая документация API с использованием Swagger
- **Качество кода**: Соблюдение стандартов PEP8, покрытие тестами не менее 75%

## Установка и запуск проекта

Склонируйте репозиторий с проектом: https://github.com/AleksandrZaec/dataprocesshub.git

Создайте файл .env в корневой директории проекта и добавьте в него переменные окружения на основе файла .env_example:

Запустите проект с использованием Docker Compose: docker-compose up --build

После того как контейнеры будут запущены, создайте суперпользователя для доступа к админ-панели Django: docker-compose exec app python3 manage.py createsuperuser

Также создайте администратора: docker-compose exec app python3 manage.py createadmin --email <почта администратора на которую будут приходить уведомления> --password <пароль администратора>

Откройте браузер и перейдите по адресу http://localhost:8000/admin, чтобы войти в админ-панель с использованием учетных данных суперпользователя или администратора

Документация API доступна по адресу http://localhost:8000/swagger/.

## Запуск тестов и генерация отчета о покрытии

docker-compose run --rm app coverage run --source='.' manage.py test

docker-compose run --rm app coverage report
