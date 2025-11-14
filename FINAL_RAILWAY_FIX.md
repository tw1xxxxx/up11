# Финальное исправление для Railway

## Проблема
Nixpacks не может определить план сборки, потому что Django файлы находятся в подпапке `shop_project/`.

## Решение

Я создал правильный `nixpacks.toml`, который явно указывает пути к файлам в подпапке.

### Что изменено:

1. ✅ Создан `nixpacks.toml` с правильными путями
2. ✅ Обновлен `Procfile` для работы из подпапки
3. ✅ Упрощен `railway.json`

## Шаги для применения:

### 1. Закоммитьте и запушьте изменения:

```bash
git add nixpacks.toml Procfile railway.json
git commit -m "Add nixpacks.toml with correct paths for subdirectory"
git push
```

### 2. Railway автоматически перезапустит деплой

После пуша Railway должен:
- Найти `nixpacks.toml` в корне
- Использовать правильные пути к файлам в `shop_project/`
- Успешно собрать проект

### 3. Настройте переменные окружения:

В Railway → **Settings** → **Variables** добавьте:

```
DEBUG=False
SECRET_KEY=ваш-новый-секретный-ключ
ALLOWED_HOSTS=*.railway.app
```

### 4. Добавьте PostgreSQL:

1. В Railway нажмите **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway автоматически создаст `DATABASE_URL`

## Если все еще не работает:

### Альтернатива 1: Переместить файлы в корень

Если Nixpacks продолжает вызывать проблемы, можно переместить ключевые файлы:

1. Скопировать `manage.py`, `requirements.txt` в корень
2. Обновить пути в `settings.py`
3. Но это более сложный вариант

### Альтернатива 2: Использовать Render.com

Render.com лучше работает с подпапками:
- Автоматически определяет структуру
- Проще настраивается
- Подробная инструкция в `DEPLOY.md`

## После успешного деплоя:

Выполните миграции через Railway Shell:

```bash
cd shop_project
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Или через Railway CLI:
```bash
railway run bash -c "cd shop_project && python manage.py migrate"
railway run bash -c "cd shop_project && python manage.py collectstatic --noinput"
railway run bash -c "cd shop_project && python manage.py createsuperuser"
```

