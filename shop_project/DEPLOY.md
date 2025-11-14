# Инструкция по деплою проекта AlphaTruck

## Подготовка проекта

### 1. Установка зависимостей для production

Создайте файл `requirements-production.txt` с минимальными зависимостями:

```bash
pip freeze > requirements-production.txt
```

Или используйте существующий `requirements.txt`, но убедитесь, что в нем есть:
- `gunicorn` или `waitress` (для Windows)
- `whitenoise` (для статических файлов)
- `psycopg2-binary` (если используете PostgreSQL)
- `mysqlclient` (если используете MySQL)

### 2. Настройка переменных окружения

Создайте файл `.env` (не коммитьте его в Git!):

```env
DEBUG=False
SECRET_KEY=ваш-секретный-ключ-сгенерируйте-новый
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Варианты деплоя

### Вариант 1: Railway (Рекомендуется - простой и быстрый)

1. **Регистрация:**
   - Зайдите на https://railway.app
   - Войдите через GitHub

2. **Подключение проекта:**
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий

3. **Настройка переменных окружения:**
   - В настройках проекта добавьте переменные:
     - `DEBUG=False`
     - `SECRET_KEY` (сгенерируйте новый)
     - `ALLOWED_HOSTS=your-app.railway.app`
   - Railway автоматически создаст PostgreSQL базу данных

4. **Настройка базы данных:**
   - Railway автоматически предоставит `DATABASE_URL`
   - Добавьте его в переменные окружения

5. **Деплой:**
   - Railway автоматически задеплоит при пуше в GitHub
   - После деплоя выполните миграции:
     ```bash
     railway run python manage.py migrate
     railway run python manage.py collectstatic --noinput
     ```

### Вариант 2: Render.com

1. **Регистрация:**
   - Зайдите на https://render.com
   - Войдите через GitHub

2. **Создание Web Service:**
   - New → Web Service
   - Подключите ваш GitHub репозиторий
   - Настройки:
     - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command:** `gunicorn shop_project.wsgi:application`
     - **Environment:** Python 3

3. **Создание PostgreSQL базы:**
   - New → PostgreSQL
   - Скопируйте Internal Database URL

4. **Настройка переменных окружения:**
   - В настройках Web Service добавьте:
     - `DEBUG=False`
     - `SECRET_KEY`
     - `ALLOWED_HOSTS=your-app.onrender.com`
     - `DATABASE_URL` (из PostgreSQL)

5. **Деплой:**
   - Render автоматически задеплоит при пуше
   - После первого деплоя выполните миграции через Shell

### Вариант 3: PythonAnywhere

1. **Регистрация:**
   - Зайдите на https://www.pythonanywhere.com
   - Создайте бесплатный аккаунт

2. **Загрузка проекта:**
   - Откройте Bash консоль
   - Клонируйте репозиторий:
     ```bash
     git clone https://github.com/yourusername/yourrepo.git
     ```

3. **Настройка виртуального окружения:**
   ```bash
   cd yourrepo/shop_project
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Настройка базы данных:**
   - Используйте встроенную MySQL или SQLite
   - Обновите `settings.py` с настройками базы

5. **Настройка Web App:**
   - Перейдите в раздел Web
   - Создайте новое приложение
   - Укажите путь к WSGI файлу: `/home/yourusername/yourrepo/shop_project/shop_project/wsgi.py`
   - Настройте статические файлы:
     - URL: `/static/`, Directory: `/home/yourusername/yourrepo/shop_project/staticfiles`
     - URL: `/media/`, Directory: `/home/yourusername/yourrepo/shop_project/media`

6. **Выполнение миграций:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

### Вариант 4: VPS (Ubuntu/Debian)

1. **Подключение к серверу:**
   ```bash
   ssh user@your-server-ip
   ```

2. **Установка зависимостей:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

3. **Клонирование проекта:**
   ```bash
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo/shop_project
   ```

4. **Настройка виртуального окружения:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Настройка PostgreSQL:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE yourdb;
   CREATE USER youruser WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE yourdb TO youruser;
   \q
   ```

6. **Настройка Gunicorn:**
   Создайте файл `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=youruser
   Group=www-data
   WorkingDirectory=/home/youruser/yourrepo/shop_project
   ExecStart=/home/youruser/yourrepo/shop_project/venv/bin/gunicorn \
           --access-logfile - \
           --workers 3 \
           --bind unix:/run/gunicorn.sock \
           shop_project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

7. **Настройка Nginx:**
   Создайте файл `/etc/nginx/sites-available/yourproject`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location /static/ {
           alias /home/youruser/yourrepo/shop_project/staticfiles/;
       }

       location /media/ {
           alias /home/youruser/yourrepo/shop_project/media/;
       }

       location / {
           proxy_pass http://unix:/run/gunicorn.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Запуск сервисов:**
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Общие шаги для всех вариантов

### 1. Обновление settings.py для production

Убедитесь, что в `settings.py` есть поддержка переменных окружения:

```python
import os
from pathlib import Path

# Получение переменных окружения
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# База данных
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}
```

### 2. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

### 3. Выполнение миграций

```bash
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

## Безопасность

⚠️ **ВАЖНО для production:**

1. **Никогда не коммитьте:**
   - `SECRET_KEY`
   - Пароли от базы данных
   - `.env` файлы

2. **Установите `DEBUG=False`** в production

3. **Используйте HTTPS** (SSL сертификат)

4. **Настройте `ALLOWED_HOSTS`** правильно

5. **Используйте сильный `SECRET_KEY`**

## Проверка после деплоя

1. Откройте сайт в браузере
2. Проверьте, что статические файлы загружаются
3. Проверьте, что медиа-файлы отображаются
4. Проверьте работу форм и API
5. Проверьте логи на наличие ошибок

## Полезные команды

```bash
# Просмотр логов (Railway)
railway logs

# Просмотр логов (Render)
# Через веб-интерфейс в разделе Logs

# Выполнение команд на сервере (Railway)
railway run python manage.py migrate

# Выполнение команд на сервере (Render)
# Через веб-интерфейс в разделе Shell
```

## Поддержка

При возникновении проблем проверьте:
- Логи приложения
- Логи веб-сервера
- Настройки базы данных
- Переменные окружения
- Статические файлы

