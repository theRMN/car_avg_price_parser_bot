import requests
from bs4 import BeautifulSoup


def parse(pages, url):
    total_price = 0
    count = 0

    for page_num in range(1, int(pages) + 1):
        next_url = url + f'&page={page_num}'
        full_page = requests.get(next_url)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        price_list = soup.findAll('div', class_='price')
        count += len(price_list)

        for price in price_list:
            price = int(price.next_element.replace(' ', ''))
            total_price += price

    return total_price // count


def get_avg_price(car, model, year):
    url = f'https://aster.kz/cars/{car}/{model}?yearFrom={year}&yearTo={year}'
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    button_text = soup.find('a', class_='btn btn_primary').text.strip()
    items = soup.findAll('span', itemprop='name')

    if len(items) != 4:
        return None

    if button_text == 'Показать 0 авто':
        return None

    try:
        pages = soup.find('li', class_='page-item end').a.text
        avg_price = parse(pages, url)
    except AttributeError:
        pages = 2
        avg_price = parse(pages, url)

    return avg_price
