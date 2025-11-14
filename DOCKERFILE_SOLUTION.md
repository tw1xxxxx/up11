# Решение: Использование Dockerfile вместо Nixpacks

## Проблема
Nix окружение не позволяет использовать `ensurepip` из-за externally-managed-environment. Nixpacks вызывает постоянные проблемы с pip.

## Решение
Создан собственный `Dockerfile`, который использует стандартный Python образ с pip уже установленным.

### Преимущества Dockerfile:
- ✅ pip уже установлен в Python образе
- ✅ Полный контроль над процессом сборки
- ✅ Проще отлаживать
- ✅ Стандартный подход для Django проектов

## Что создано:

1. **Dockerfile** - использует `python:3.11-slim`
2. **railway.json** - обновлен для использования Dockerfile
3. **nixpacks.toml** - удален (больше не нужен)
4. **Procfile** - упрощен (работает из корня после копирования)

## Что нужно сделать:

### 1. Закоммитьте и запушьте изменения:

```bash
git add Dockerfile railway.json Procfile
git rm nixpacks.toml  # если он еще есть
git commit -m "Switch to Dockerfile instead of Nixpacks"
git push
```

### 2. Railway автоматически перезапустит деплой

Railway обнаружит `Dockerfile` и использует его для сборки вместо Nixpacks.

### 3. Настройте переменные окружения:

В Railway → **Settings** → **Variables** добавьте:
- `DEBUG=False`
- `SECRET_KEY` (сгенерируйте новый)
- `ALLOWED_HOSTS=*.railway.app`

### 4. Добавьте PostgreSQL базу данных

## Как работает Dockerfile:

1. Использует `python:3.11-slim` (легкий образ с Python и pip)
2. Устанавливает системные зависимости (gcc для компиляции некоторых пакетов)
3. Копирует `requirements.txt` и устанавливает зависимости
4. Копирует весь проект из `shop_project/`
5. Собирает статические файлы
6. Запускает через gunicorn

## После успешного деплоя:

Выполните миграции через Railway Shell:

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

## Если возникнут проблемы:

### Проверьте логи сборки:
- В Railway откройте последний деплой
- Нажмите "View logs"
- Проверьте, на каком этапе происходит ошибка

### Возможные проблемы:

1. **Ошибка с gcc**: Если какой-то пакет требует компиляции, gcc уже установлен в Dockerfile
2. **Ошибка с путями**: Все пути в Dockerfile указывают на `shop_project/`
3. **Ошибка с PORT**: Переменная `$PORT` автоматически подставляется Railway

Этот подход должен работать надежнее, чем Nixpacks!

