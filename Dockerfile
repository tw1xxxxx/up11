FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements.txt и установка зависимостей
COPY shop_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY shop_project/ .

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Запуск приложения
CMD gunicorn shop_project.wsgi:application --bind 0.0.0.0:$PORT

