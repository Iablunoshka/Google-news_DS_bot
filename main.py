import requests
from bs4 import BeautifulSoup

# URL страницы Google Новостей
url = 'https://news.google.com/u/2/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRGQwTWpFU0FuVnJLQUFQAQ?hl=uk&gl=UA&ceid=UA%3Auk'
response = requests.get(url)

# Создание пустого словаря для тем новостей
url_list = []
count_url = []
big_news_dict = {}
small_news_dict = {}
news_dict = {}


def big_news():
    global big_news_dict
    global url_list
    global count_url

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
    combine(big_news_dict, comb_flag, url_list, small_news_dict, count_url)


def small_news():
    global small_news_dict
    global url_list

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
                    url_list.append(full_url)
                    small_news_dict[theme2] = []

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    comb_flag = False
    combine(big_news_dict, comb_flag, url_list, small_news_dict, count_url)


def get_final_url(news_dict):
    for theme, links in news_dict.items():
        for i in range(len(links)):
            try:
                redirect_url = links[i]
                # Отправка запроса на непрямую ссылку
                response = requests.get(redirect_url)
                final_url = response.url
                links[i] = final_url
            except requests.RequestException as e:
                print(f"Error retrieving URL {redirect_url}: {e}")


def combine(big_news_dict, comb_flag, url_list, small_news_dict, count_url):
    global news_dict

    if comb_flag:
        for idx, key in enumerate(big_news_dict):
            count = count_url[idx]
            for _ in range(count):
                if url_list:
                    big_news_dict[key].append(url_list.pop(0))
        get_final_url(big_news_dict)
    else:
        for key in small_news_dict:
            for _ in range(1):
                if url_list:
                    small_news_dict[key].append(url_list.pop(0))
        get_final_url(small_news_dict)

    news_dict.update(big_news_dict)
    news_dict.update(small_news_dict)


def main():
    big_news()
    small_news()
    count_news = len(news_dict)
    print(count_news)
    print(news_dict)
    return news_dict  # Возвращаем news_dict


# Если файл main.py запускается как основная программа, выполним main()
if __name__ == "__main__":
    main()
