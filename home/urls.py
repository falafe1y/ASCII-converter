from django.urls import path
from . import views  # Импортируем функции из views.py

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
]