# GameAPI
GameAPI — це RESTful backend на Django + DRF для простого гейм-сервісу з авторизацією по токену, логікою гри та історією результатів.
## Технології
- Python 3.11
- Django 5.2
- Django REST Framework
- MySQL 8
- Docker + Docker Compose
- Gunicorn
## Запуск
Для запуску клонуйте репозиторій та виконайте наступну команду:
```bash
docker compose up -d --build --no-deps
```
Всі ендпоінти виконані знідно ТЗ.

На запуску раняться тести, які перевіряють коректність роботи API.

.env файл доданий для простого запуску, зазвичай я його не додаю в репозиторій, але тут він є для зручності.