FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements.txt и установка зависимостей
# Используем production requirements без Windows-специфичных пакетов
COPY requirements-production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY shop_project/ .

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Запуск приложения
# Создаем скрипт запуска для правильной обработки переменной PORT
RUN echo '#!/bin/sh\nset -e\npython manage.py migrate --noinput || true\nexec gunicorn shop_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]

