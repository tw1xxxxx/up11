"""
Management command для заполнения базы данных тестовыми данными
"""
from django.core.management.base import BaseCommand
from shop.models import Brand, Model, Car
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (марки, модели, автомобили)'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю заполнение базы данных...')
        
        # Очистка существующих данных (опционально)
        # Car.objects.all().delete()
        # Model.objects.all().delete()
        # Brand.objects.all().delete()
        
        # Создание марок
        brands_data = [
            {
                'name': 'Mercedes-Benz',
                'country': 'Германия',
                'description': 'Немецкий производитель автомобилей премиум-класса',
            },
            {
                'name': 'BMW',
                'country': 'Германия',
                'description': 'Баварский производитель автомобилей премиум-класса',
            },
            {
                'name': 'Toyota',
                'country': 'Япония',
                'description': 'Японский производитель надежных автомобилей',
            },
            {
                'name': 'Audi',
                'country': 'Германия',
                'description': 'Немецкий производитель автомобилей премиум-класса',
            },
        ]
        
        brands = {}
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults=brand_data
            )
            brands[brand_data['name']] = brand
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана марка: {brand.name}'))
        
        # Создание моделей
        models_data = [
            {'brand': 'Mercedes-Benz', 'name': 'GLC'},
            {'brand': 'Mercedes-Benz', 'name': 'C-Class'},
            {'brand': 'Mercedes-Benz', 'name': 'E-Class'},
            {'brand': 'BMW', 'name': 'X5'},
            {'brand': 'BMW', 'name': '3 Series'},
            {'brand': 'Toyota', 'name': 'Land Cruiser 200'},
            {'brand': 'Toyota', 'name': 'Land Cruiser 300'},
            {'brand': 'Audi', 'name': 'Q7'},
            {'brand': 'Audi', 'name': 'A6'},
        ]
        
        models = {}
        for model_data in models_data:
            brand = brands[model_data['brand']]
            model, created = Model.objects.get_or_create(
                brand=brand,
                name=model_data['name'],
                defaults={'brand': brand, 'name': model_data['name']}
            )
            models[f"{model_data['brand']} {model_data['name']}"] = model
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана модель: {model}'))
        
        # Создание автомобилей
        cars_data = [
            {
                'model': 'Mercedes-Benz GLC',
                'vin': 'WDC0G4JBOLF123459',
                'color': 'Черный',
                'price': Decimal('1800000.00'),
                'mileage': 15000,
                'year': 2022,
                'is_available': True,
                'features': 'Полный привод, кожаный салон, панорамная крыша'
            },
            {
                'model': 'Mercedes-Benz C-Class',
                'vin': 'WDC0G4JBOLF123460',
                'color': 'Белый',
                'price': Decimal('3500000.00'),
                'mileage': 8000,
                'year': 2023,
                'is_available': True,
                'features': 'AMG пакет, спортивная подвеска'
            },
            {
                'model': 'Mercedes-Benz E-Class',
                'vin': 'WDC0G4JBOLF123461',
                'color': 'Серебристый',
                'price': Decimal('4200000.00'),
                'mileage': 12000,
                'year': 2023,
                'is_available': True,
                'features': 'Бизнес-класс, все опции'
            },
            {
                'model': 'BMW X5',
                'vin': 'WBAFR7C50LC123432',
                'color': 'Синий',
                'price': Decimal('5500000.00'),
                'mileage': 20000,
                'year': 2021,
                'is_available': True,
                'features': 'xDrive, M Sport пакет'
            },
            {
                'model': 'BMW 3 Series',
                'vin': 'WBAFR7C50LC123433',
                'color': 'Красный',
                'price': Decimal('3200000.00'),
                'mileage': 10000,
                'year': 2023,
                'is_available': True,
                'features': 'Спортивная версия'
            },
            {
                'model': 'Toyota Land Cruiser 200',
                'vin': 'WBAFR7C50LC123434',
                'color': 'Белый',
                'price': Decimal('5600000.00'),
                'mileage': 45000,
                'year': 2017,
                'is_available': True,
                'features': 'Внедорожник, полный привод'
            },
            {
                'model': 'Toyota Land Cruiser 300',
                'vin': 'WBAFR7C50LC123435',
                'color': 'Черный',
                'price': Decimal('11200000.00'),
                'mileage': 5000,
                'year': 2022,
                'is_available': True,
                'features': 'Новое поколение, все опции'
            },
            {
                'model': 'Audi Q7',
                'vin': 'WAUZZZ4L7HD123456',
                'color': 'Серый',
                'price': Decimal('4800000.00'),
                'mileage': 18000,
                'year': 2021,
                'is_available': True,
                'features': 'Quattro, 7 мест'
            },
            {
                'model': 'Audi A6',
                'vin': 'WAUZZZ4L7HD123457',
                'color': 'Черный',
                'price': Decimal('3900000.00'),
                'mileage': 15000,
                'year': 2022,
                'is_available': True,
                'features': 'Бизнес-седан, премиум'
            },
        ]
        
        created_count = 0
        for car_data in cars_data:
            model = models[car_data['model']]
            car_data_copy = car_data.copy()
            del car_data_copy['model']
            
            car, created = Car.objects.get_or_create(
                vin=car_data['vin'],
                defaults={
                    'model': model,
                    **car_data_copy
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Создан автомобиль: {car}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nГотово! Создано автомобилей: {created_count}'
        ))
        self.stdout.write('Примечание: Фотографии нужно загрузить вручную через админ-панель Django')

