# Как добавить данные в базу данных

## Проблема
Каталог автомобилей пуст - в базе данных нет данных.

## Решение 1: Через админ-панель Django (рекомендуется)

### 1. Создайте суперпользователя:

Я создал скрипт `create_superuser.py`, который автоматически создаст администратора при запуске.

**По умолчанию:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

**Или настройте через переменные окружения в Railway:**
- `DJANGO_SUPERUSER_USERNAME` = ваш логин
- `DJANGO_SUPERUSER_PASSWORD` = ваш пароль
- `DJANGO_SUPERUSER_EMAIL` = ваш email

### 2. Закоммитьте изменения:

```bash
git add Dockerfile create_superuser.py
git commit -m "Add automatic superuser creation"
git push
```

### 3. Войдите в админ-панель:

1. Откройте в браузере: `https://up11-production.up.railway.app/admin/`
2. Введите:
   - Username: `admin`
   - Password: `admin123`
3. Нажмите "Войти"

### 4. Добавьте данные:

В админ-панели Django:

1. **Добавьте марки (Brands):**
   - Нажмите "Марки" → "Добавить марку"
   - Заполните: название, страна, описание, загрузите логотип
   - Сохраните

2. **Добавьте модели (Models):**
   - Нажмите "Модели" → "Добавить модель"
   - Выберите марку, введите название модели
   - Сохраните

3. **Добавьте автомобили (Cars):**
   - Нажмите "Автомобили" → "Добавить автомобиль"
   - Заполните все поля:
     - Модель
     - VIN номер
     - Цвет
     - Цена
     - Пробег
     - Год выпуска
     - Загрузите фото
   - Сохраните

## Решение 2: Через Django Shell (если есть доступ)

Если вы найдете способ открыть Shell в Railway:

```python
python manage.py shell
```

Затем выполните:

```python
from shop.models import Brand, Model, Car

# Создать марку
brand = Brand.objects.create(
    name="Mercedes-Benz",
    country="Германия",
    description="Немецкий производитель автомобилей",
    logo="brands/mercedes.jpg"  # путь к изображению
)

# Создать модель
model = Model.objects.create(
    brand=brand,
    name="GLC"
)

# Создать автомобиль
car = Car.objects.create(
    model=model,
    vin="WDC0G4JBOLF123459",
    color="Черный",
    price=1800000.00,
    mileage=15000,
    year=2022,
    image="cars/mercedes_glc.jpg",
    is_available=True
)
```

## Решение 3: Импорт данных из фикстур

Если у вас есть данные в формате JSON:

1. Создайте файл `fixtures/initial_data.json` с данными
2. Загрузите через админ-панель или команду:
   ```bash
   python manage.py loaddata fixtures/initial_data.json
   ```

## Быстрый способ: Используйте данные из локальной базы

Если у вас есть локальная база данных с данными:

1. Экспортируйте данные:
   ```bash
   python manage.py dumpdata shop > fixtures/data.json
   ```

2. Загрузите в Railway через админ-панель или Shell

## После добавления данных:

1. Обновите страницу каталога
2. Автомобили должны отобразиться
3. Фотографии должны загружаться из папки `media/`

## Важно:

- Убедитесь, что медиа-файлы (фото автомобилей) загружены в папку `media/` в Railway
- Или используйте внешнее хранилище (S3, Cloudinary) для медиа-файлов в production

