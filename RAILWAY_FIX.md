# Исправление ошибки деплоя на Railway

## Проблема
Railway не может найти файлы Django, потому что проект находится в подпапке `shop_project/`.

## Решение

Я создал конфигурационные файлы в корне репозитория:
- `Procfile` - команда запуска
- `railway.json` - конфигурация Railway
- `nixpacks.toml` - конфигурация сборки
- `runtime.txt` - версия Python

## Шаги для исправления:

### 1. Добавьте файлы в Git и закоммитьте:

```bash
# Перейдите в корень репозитория (где находится папка shop_project)
cd C:\УП11.01\AplhaTruck

# Добавьте новые файлы
git add Procfile railway.json nixpacks.toml runtime.txt

# Закоммитьте
git commit -m "Add Railway configuration for subdirectory deployment"

# Запушьте
git push
```

### 2. В Railway настройте переменные окружения:

1. Откройте ваш проект в Railway
2. Перейдите в Settings → Variables
3. Добавьте:
   - `DEBUG=False`
   - `SECRET_KEY` (сгенерируйте новый)
   - `ALLOWED_HOSTS=*.railway.app,your-app.railway.app`

### 3. Добавьте PostgreSQL базу данных:

1. В Railway нажмите "New" → "Database" → "Add PostgreSQL"
2. Railway автоматически создаст переменную `DATABASE_URL`

### 4. Перезапустите деплой:

Railway автоматически перезапустит деплой после пуша. Или нажмите "Redeploy" вручную.

## Альтернативное решение (если не работает):

Если Railway все еще не может собрать проект, можно настроить Root Directory:

1. В Railway откройте Settings → Service
2. Найдите "Root Directory"
3. Установите: `shop_project`
4. Обновите `Procfile` в `shop_project/`:
   ```
   web: gunicorn shop_project.wsgi:application --bind 0.0.0.0:$PORT
   ```

## Проверка после деплоя:

После успешного деплоя выполните:

```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

Или через веб-интерфейс Railway:
1. Откройте ваш сервис
2. Нажмите на три точки → "Open Shell"
3. Выполните команды выше

