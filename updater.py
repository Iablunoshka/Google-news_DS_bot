import time
from main import main

def update_news_file():
    while True:
        news_dict = main()

        # Открываем файл для записи
        with open("news.txt", "w", encoding="utf-8") as f:
            # Записываем словарь в файл
            for key, urls in news_dict.items():
                f.write(f"{key}:\n")
                for url in urls:
                    f.write(f"{url}\n")
                f.write("\n")  # Добавляем пустую строку между категориями новостей

        time.sleep(1800)  # Обновление каждые 30 минут

if __name__ == "__main__":
    update_news_file()
