from PIL import Image
from colorama import init

class colored_ascii:
    def __init__(self, image_path:str, output_html:str, width:int):
        # Инициализация colorama
        init(autoreset=True)
        
        self._image_path = image_path
        self._output_html = output_html
        self._width = width

    # Функция для преобразования изображения в ASCII с цветами оффлайн в терминал
    def image_to_colored_ascii(self):
        # Открываем изображение
        img = Image.open(self._image_path)
        
        # Изменяем размер изображения
        aspect_ratio = (img.height / img.width)
        new_height = int(aspect_ratio * 0.8 * self._width)
        img = img.resize((self._width*2, new_height))

        # Конвертируем в градации серого
        img = img.convert("L")

        # Определяем символы для ASCII арта
        chars = "0123456789 "
        pixels = img.getdata()
        
        # Создаем ASCII арт
        ascii_str = ''.join(chars[pixel // 33] for pixel in pixels)
        
        # Форматируем строку в нужный вид
        img_width = img.width
        ascii_art = "\n".join(ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width))
        ascii_art += "\n\n"
        
        return ascii_art

    # Метод для преобразования изображения
    # в ASCII арт на странице HTML
    def image_to_ascii_html(self):
        img = Image.open(self._image_path)
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * 0.8 * self._width)  # При необходимости скорректировать коэффициент
        img = img.resize((self._width, new_height))

        img_gray = img.convert("L")
        img_color = img.convert("RGB")

        chars = "o0123456789"
        char_len = len(chars)
        pixel_to_char = lambda pixel: chars[int(pixel / 255 * (char_len - 1))]

        # Шаблон для кнопок и открытия файлового менеджера
        html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FASCII</title>
    <style>
        body {
            background-color: #121212; /* Черный фон */
            color: #ffffff; /* Белый текст */
            font-family: Arial, sans-serif; /* Шрифт */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            margin-left: -140px; /* Сдвиг тега h1 на 140 пикселей влево */
        }

        form {
            background-color: #1c1c1c; /* Черный фон формы */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 400px;
            margin-left: -100px; /* Сдвиг тега form на 100 пикселей влево */
        }

        input[type="file"] {
            background-color: #333;
            border: 2px solid #444;
            color: #fff;
            padding: 10px;
            width: 100%;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 1em;
        }

        button {
            background-color: #5f5f5f; /* Серый цвет кнопки */
            border: none;
            color: white;
            padding: 12px 20px;
            font-size: 1.2em;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #3e3e3e; /* Цвет кнопки при наведении */
        }

        button:active {
            background-color: #2a2a2a; /* Цвет кнопки при нажатии */
        }

        input[type="file"]:hover,
        button:hover {
            background-color: #4c4c4c; /* Фон светлее при наведении */
        }
    </style>
</head>
<body>
    <div>
        <h1></h1>
        <form method="POST" enctype="multipart/form-data" action=".">
            {% csrf_token %}
            <input type="file" name="image" accept=".jpg" required>
            <button type="submit">Создать арт</button>
        </form>
    </div>
</body>
<head>
<style>
    body {
        background-color: black;
        color: white;
        font-family: monospace;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        overflow: hidden;
    }
    pre {
        line-height: 0.6;
        text-align: left; /* Объект с ASCII-артом слева */
        position: relative;
        left: 100px; /* Сдвиг на 100 пикселей вправо */
        font-size: 20px; /* Размер шрифта */
        width: auto; /* Ширина ASCII-арта */
        height: auto; /* Высота ASCII-арта */
        # overflow: auto; /* Прокрутка, если арт выходит за пределы видимой области */
    }
        """
        html_content += "</style>\n</head>\n<body><pre>\n"
        pixels_gray = img_gray.getdata()
        pixels_color = img_color.getdata()

        for i in range(len(pixels_gray)):
            if i % self._width == 0 and i != 0:
                html_content += "\n"
            gray_pixel = pixels_gray[i]
            color_pixel = pixels_color[i]
            r, g, b = color_pixel
            ascii_char = pixel_to_char(gray_pixel)
            html_content += f"<span style='color: rgb({r},{g},{b});'>{ascii_char}</span>"

        with open(self._output_html, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML-файл с ASCII-артом сохранён: {self._output_html}")