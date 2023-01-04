# Проектная работа 10 спринта

https://github.com/lppavli/notifications_sprint_1

В рамках проекта были реализованы следующие задачи:
- API имитирующее регистрацию пользователя и подтверждение его учетной записи (user_api)
- API для генерации email-рассылки администратором (admin_api)
- Работа с очередями RabbitMQ (consumer)
- Модуль для работы с Websoket (websoket)

Сборка проекта:
```
docker-compose up -d --build
```
Миграции
```
cd notifications_api
alembic upgrade head
```