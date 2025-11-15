# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_add_created_at_to_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото автомобиля'),
        ),
    ]

