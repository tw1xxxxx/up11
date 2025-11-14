# Простое исправление ошибки Railway

## Проблема
Ошибка: `undefined variable 'pip'` в nixpacks.toml

## Решение

Я упростил конфигурацию. Теперь Railway будет автоматически определять Django проект.

### Что изменено:
1. ✅ Удален `nixpacks.toml` (вызывал ошибку)
2. ✅ Упрощен `railway.json` (Railway сам определит сборку)
3. ✅ Оставлен `Procfile` (команда запуска)

## Шаги для применения:

### 1. Добавьте изменения в Git:

```bash
# В корне репозитория (где папка shop_project)
git add .
git commit -m "Fix Railway configuration - remove nixpacks.toml"
git push
```

### 2. В Railway настройте Root Directory:

**ВАЖНО:** Это ключевой шаг!

1. Откройте ваш проект в Railway
2. Перейдите в **Settings** → **Service**
3. Найдите поле **"Root Directory"**
4. Введите: `shop_project`
5. Нажмите **Save**

### 3. Настройте переменные окружения:

В Railway → **Settings** → **Variables** добавьте:

```
DEBUG=False
SECRET_KEY=ваш-новый-секретный-ключ
ALLOWED_HOSTS=*.railway.app
```

**Как сгенерировать SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Добавьте PostgreSQL:

1. В Railway нажмите **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway автоматически создаст переменную `DATABASE_URL`

### 5. Перезапустите деплой:

После настройки Root Directory Railway автоматически перезапустит деплой.

## Альтернатива (если Root Directory не помогает):

Если ошибка сохраняется, можно переместить все файлы Django в корень репозитория, но это более сложный вариант.

## После успешного деплоя:

Выполните миграции через Railway Shell:

1. Откройте ваш сервис в Railway
2. Нажмите на три точки → **"Open Shell"**
3. Выполните:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

Или через CLI:
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

