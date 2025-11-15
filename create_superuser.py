#!/usr/bin/env python
"""Скрипт для создания суперпользователя Django"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Проверяем, есть ли уже суперпользователь
if not User.objects.filter(is_superuser=True).exists():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Суперпользователь создан: {username}')
else:
    print('Суперпользователь уже существует')

