from colored_ascii import colored_ascii
from time import sleep

if __name__ == "__main__":
    num = 0
    while True:
        image_path = f"C:\\Users\\79059\\Downloads\\{num}.jpg"   
        ASCII = colored_ascii(image_path, "ASCII.html", 120)

        ASCII.image_to_ascii_html()
        num += 1
        sleep(3)