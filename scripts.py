import requests
from bs4 import BeautifulSoup


def get_avg_price(car: str, model: str, year: str):
    url = f'https://aster.kz/cars/{car}/{model}?yearFrom={year}'

    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    price_list = soup.findAll('div', class_='price')
    total_price = 0

    for price in price_list:
        price = int(price.next_element.replace(' ', ''))
        total_price += price

    avg_price = total_price / len(price_list)

    return round(avg_price, 2)


if __name__ == '__main__':
    print(get_avg_price('acura', 'mdx', '2002'))
