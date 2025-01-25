from django.shortcuts import render
from django.http import HttpResponse
from image_to_ascii import colored_ascii
import os
from django.conf import settings

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        if uploaded_file and uploaded_file.name.endswith('.jpg'):

            # Создание пути для сохраненного файла
            save_directory = os.path.join(settings.BASE_DIR, 'uploads')  # Папка рядом с views.py
            os.makedirs(save_directory, exist_ok=True)  # Если папки нет создаем ее
            path_to_file = os.path.join(save_directory, uploaded_file.name)

            # Сохранение изображения на сервер
            with open(path_to_file, 'wb') as file:
                for chunk in uploaded_file.chunks():
                    file.write(chunk)
            
            # Создание ASCII-арта
            ASCII = colored_ascii.colored_ascii(path_to_file, "C:\\Users\\79059\\Documents\\Work\\Django\\home\\templates\\home\\index.html", 50)
            ASCII.image_to_ascii_html()

            return render(request, 'home/index.html')
        else:
            return HttpResponse("Пожалуйста, выберите файл в формате JPG.")
    return render(request, 'home/index.html')