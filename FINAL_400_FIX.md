# Финальное исправление ошибки 400

## Проблема
Ошибка 400 Bad Request на `up11-production.up.railway.app`

## Решение:

### 1. Добавьте CSRF_TRUSTED_ORIGINS в Railway:

1. Откройте сервис up11 → **Variables**
2. Нажмите **"+ New Variable"**
3. Добавьте:
   - **Name:** `CSRF_TRUSTED_ORIGINS`
   - **Value:** `https://up11-production.up.railway.app`
4. Сохраните

### 2. Убедитесь, что ALLOWED_HOSTS настроен:

В Variables проверьте:
- **Name:** `ALLOWED_HOSTS`
- **Value:** `*` или `up11-production.up.railway.app,*.railway.app`

### 3. Закоммитьте изменения:

```bash
git add shop_project/shop_project/settings.py
git commit -m "Fix CSRF_TRUSTED_ORIGINS configuration"
git push
```

### 4. Перезапустите сервис:

1. В Railway нажмите на три точки (⋮) рядом с активным деплоем
2. Выберите **"Restart"**

### 5. Временное включение DEBUG (для диагностики):

Если ошибка сохраняется:

1. В Railway Variables измените:
   - **DEBUG** = `True`
2. Перезапустите сервис
3. Обновите страницу - увидите детальную ошибку Django
4. После выяснения причины верните `DEBUG=False`

## Возможные причины ошибки 400:

1. **ALLOWED_HOSTS** - не включает ваш домен
2. **CSRF_TRUSTED_ORIGINS** - не настроен для HTTPS
3. **Главная страница требует авторизации** - попробуйте открыть `/login/` или `/register/`

## Альтернатива: Попробуйте другие URL:

Вместо главной страницы попробуйте:
- `https://up11-production.up.railway.app/login/`
- `https://up11-production.up.railway.app/register/`
- `https://up11-production.up.railway.app/cars/`

Если эти URL работают, проблема в главной странице (требует авторизации).

