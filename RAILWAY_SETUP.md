# Пошаговая настройка Railway для проекта в подпапке

## ⚠️ ВАЖНО: Настройка Root Directory

Главная проблема - Railway ищет файлы Django в корне, а они в папке `shop_project/`.

## Шаг 1: Убедитесь, что изменения запушены

```bash
# Проверьте статус
git status

# Если есть незакоммиченные изменения:
git add .
git commit -m "Fix Railway config - remove nixpacks.toml"
git push
```

## Шаг 2: Настройте Root Directory в Railway (КРИТИЧНО!)

1. **Откройте Railway Dashboard**
   - Зайдите на https://railway.app
   - Выберите ваш проект `up11`

2. **Перейдите в настройки сервиса:**
   - Нажмите на ваш сервис (не на проект, а на сам сервис)
   - Или перейдите в **Settings** → **Service**

3. **Найдите "Root Directory":**
   - Прокрутите вниз до секции **"Root Directory"**
   - По умолчанию там пусто или указан `.`

4. **Установите Root Directory:**
   - Введите: `shop_project`
   - **ВАЖНО:** Без слеша в начале и конце!
   - Нажмите **"Save"** или **"Update"**

5. **Railway автоматически перезапустит деплой**

## Шаг 3: Настройте переменные окружения

1. В Railway перейдите в **Settings** → **Variables**
2. Добавьте переменные (кнопка **"New Variable"**):

   ```
   DEBUG = False
   SECRET_KEY = ваш-новый-секретный-ключ
   ALLOWED_HOSTS = *.railway.app
   ```

   **Как сгенерировать SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Нажмите **"Save"** для каждой переменной

## Шаг 4: Добавьте PostgreSQL базу данных

1. В Railway Dashboard нажмите **"New"** (зеленая кнопка)
2. Выберите **"Database"** → **"Add PostgreSQL"**
3. Railway автоматически:
   - Создаст базу данных
   - Добавит переменную `DATABASE_URL` в ваш сервис
   - Подключит базу к сервису

## Шаг 5: Проверьте деплой

После настройки Root Directory Railway должен:
1. Найти `manage.py` в `shop_project/`
2. Найти `requirements.txt` в `shop_project/`
3. Правильно собрать проект
4. Запустить через `Procfile`

## Шаг 6: После успешного деплоя

Выполните миграции через Railway Shell:

1. Откройте ваш сервис
2. Нажмите на три точки (⋮) → **"Open Shell"**
3. Выполните команды:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

Или через Railway CLI:
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

## Если ошибка сохраняется

### Вариант A: Очистите кэш Railway

1. В Settings → Service найдите **"Clear Build Cache"**
2. Нажмите и подтвердите
3. Перезапустите деплой

### Вариант B: Проверьте структуру файлов

Убедитесь, что в корне репозитория есть:
- ✅ `Procfile` (с командой `cd shop_project && ...`)
- ✅ `railway.json` (упрощенный)
- ❌ НЕТ `nixpacks.toml` (должен быть удален)

А в `shop_project/` есть:
- ✅ `manage.py`
- ✅ `requirements.txt`
- ✅ `shop_project/settings.py`

### Вариант C: Используйте Render.com

Если Railway продолжает вызывать проблемы, попробуйте Render.com:
- Проще настраивается для подпапок
- Подробная инструкция в `DEPLOY.md`

## Структура файлов должна быть:

```
AplhaTruck/                    (корень репозитория)
├── Procfile                   ← здесь
├── railway.json                ← здесь
├── runtime.txt                 ← здесь
└── shop_project/               ← Root Directory в Railway
    ├── manage.py
    ├── requirements.txt
    ├── shop_project/
    │   ├── settings.py
    │   └── wsgi.py
    └── ...
```

