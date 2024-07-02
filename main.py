import requests
from bs4 import BeautifulSoup

# URL страницы Google Новостей
url = 'https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnlkUm9DVWxVb0FBUAE?hl=ru&gl=RU&ceid=RU%3Aru'
response = requests.get(url)

# Создание пустого словаря для тем новостей
url_list = []
count_url = []
small_url_list = []
big_news_dict = {}
small_news_dict = {}
news_dict = {}



def big_news():
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        blocks = soup.find_all('div', class_='W8yrY')

        for block in blocks:
            # Находим элемент <a> в текущем блоке, который содержит текст темы
            link = block.find('a', jsaction="click:kkIcoc;")
            elements = block.find_all('a', class_='WwrzSb')
            if link:
                theme = link.text.strip()
                big_news_dict[theme] = []  # Инициализируем пустым списком для каждой темы

            count = 0
            for element in elements:
                href = element.get('href')
                if href:
                    # Формируем полные ссылки
                    full_url = f'https://news.google.com{href[1:]}' if href.startswith('.') else href
                    url_list.append(full_url)
                    count += 1

            # Добавляем количество ссылок в список count_url
            count_url.append(count)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    comb_flag = True
    combine(big_news_dict, comb_flag, url_list, small_news_dict, small_url_list, count_url)


def small_news():
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        blocks = soup.find_all('div', class_="m5k28")

        for block in blocks:
            # Ищем элемент <a> с классом 'JtKRv' внутри текущего блока
            link = block.find('a', class_='JtKRv')
            href_element = block.find('a', class_='WwrzSb')
            if link and href_element:
                theme2 = link.text.strip()
                href = href_element.get('href')
                if href:
                    # Формируем полные ссылки
                    full_url = f'https://news.google.com{href[1:]}' if href.startswith('.') else href
                    small_url_list.append(full_url)
                    small_news_dict[theme2] = []

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    comb_flag = False
    combine(big_news_dict, comb_flag, url_list, small_news_dict, small_url_list, count_url)



def combine(big_news_dict, comb_flag, url_list, small_news_dict, small_url_list, count_url):
    if comb_flag:
        # Добавляем ссылки к каждой теме в big_news_dict
        for idx, key in enumerate(big_news_dict):
            count = count_url[idx]
            for _ in range(count):
                if url_list:
                    big_news_dict[key].append(url_list.pop(0))
    else:
        # Добавляем до 1 ссылки к каждой теме в small_news_dict
        for key in small_news_dict:
            for _ in range(1):
                if small_url_list:
                    small_news_dict[key].append(small_url_list.pop(0))
                    news_dict.update(big_news_dict)
                    news_dict.update(small_news_dict)

def main():
    big_news()
    small_news()
    count_key = len(news_dict)
    print(news_dict)
    print(count_key)

main()
