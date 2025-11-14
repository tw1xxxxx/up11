# Быстрый деплой на Railway (5 минут)

## Шаг 1: Подготовка репозитория

```bash
# Инициализируйте Git (если еще не сделано)
git init
git add .
git commit -m "Initial commit"

# Создайте репозиторий на GitHub и загрузите код
git remote add origin https://github.com/ваш-username/ваш-репозиторий.git
git push -u origin main
```

## Шаг 2: Деплой на Railway

1. Зайдите на https://railway.app
2. Войдите через GitHub
3. Нажмите "New Project" → "Deploy from GitHub repo"
4. Выберите ваш репозиторий
5. Railway автоматически определит Django проект

## Шаг 3: Настройка переменных окружения

В настройках проекта Railway добавьте:

```
DEBUG=False
SECRET_KEY=сгенерируйте-новый-секретный-ключ
ALLOWED_HOSTS=*.railway.app,your-app.railway.app
```

**Как сгенерировать SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Шаг 4: Настройка базы данных

1. В Railway нажмите "New" → "Database" → "Add PostgreSQL"
2. Railway автоматически создаст переменную `DATABASE_URL`
3. Она будет автоматически использована проектом

## Шаг 5: Выполнение миграций

После первого деплоя:

1. В Railway откройте ваш проект
2. Нажмите на сервис → "Deployments" → "View Logs"
3. Или используйте CLI:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py collectstatic --noinput
   railway run python manage.py createsuperuser
   ```

## Готово! 🎉

Ваш сайт будет доступен по адресу: `https://your-app.railway.app`

---

## Альтернатива: Render.com

1. Зайдите на https://render.com
2. New → Web Service → Подключите GitHub
3. Настройки:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn shop_project.wsgi:application`
4. Добавьте PostgreSQL базу данных
5. Настройте переменные окружения (как в Railway)

---

## Важные замечания

⚠️ **Не забудьте:**
- Установить `DEBUG=False` в production
- Использовать новый `SECRET_KEY`
- Настроить `ALLOWED_HOSTS` правильно
- Выполнить миграции после деплоя
- Создать суперпользователя

📖 **Подробная инструкция:** см. `DEPLOY.md`

