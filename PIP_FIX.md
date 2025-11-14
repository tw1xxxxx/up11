# Исправление проблемы с pip

## Проблема
`pip` не найден в Nix окружении, даже через `python3 -m pip`.

## Решение

Я добавил установку pip через `ensurepip` перед установкой зависимостей:

```toml
[phases.install]
cmds = [
    "python3 -m ensurepip --upgrade",  # Устанавливает pip
    "python3 -m pip install --upgrade pip",  # Обновляет pip
    "python3 -m pip install -r shop_project/requirements.txt",
    ...
]
```

## Что нужно сделать:

### 1. Закоммитьте и запушьте изменения:

```bash
git add nixpacks.toml Procfile
git commit -m "Install pip via ensurepip before installing packages"
git push
```

### 2. Railway автоматически перезапустит деплой

`ensurepip` установит pip, если его нет, что должно решить проблему.

## Если все еще не работает:

### Альтернатива: Использовать Dockerfile напрямую

Если Nixpacks продолжает вызывать проблемы, можно создать собственный Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY shop_project/requirements.txt .
RUN pip install -r requirements.txt

COPY shop_project/ .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "shop_project.wsgi:application", "--bind", "0.0.0.0:$PORT"]
```

И указать в `railway.json`:
```json
{
  "build": {
    "builder": "DOCKERFILE"
  }
}
```

### Или использовать Render.com

Render.com лучше работает с подпапками и не требует таких сложных настроек.

