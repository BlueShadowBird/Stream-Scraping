import requests
import csv

from bs4 import BeautifulSoup


class SteamScraper:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
        self.result = []

    def scrape(self):
        url = 'https://store.steampowered.com/'
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        tab_see_more = soup.find_all('div', attrs={'class': 'tab_see_more'})

        top_seller_url = ''
        for tab in tab_see_more:
            if 'Top Sellers' in tab.text:
                top_seller_url = tab.find('a')['href']
                break

        if top_seller_url == '':
            print('Top Seller not found')
        else:
            resp = self.session.get(top_seller_url)
            soup = BeautifulSoup(resp.text, 'html.parser')

            sellers = soup.find('div', attrs={'id': 'search_resultsRows'}).find_all('a', attrs={
                'class': 'search_result_row ds_collapse_flag'})

            for seller in sellers:
                title = seller.find('span', attrs={'class': 'title'}).text
                pic_url = seller.find('div', attrs={'class': 'col search_capsule'}).find('img')['src']
                released = seller.find('div', attrs={'class': 'col search_released responsive_secondrow'}).text
                price_div = seller.find('div', attrs={'class': 'col search_price responsive_secondrow'})
                if None == price_div:
                    price_div = seller.find('div', attrs={'class': 'col search_price_discount_combined responsive_secondrow'})
                    diskon_price = price_div.find('div', attrs={'class': 'col search_price discounted responsive_secondrow'}).contents[3]
                    diskon = price_div.find('div', attrs={'class': 'col search_discount responsive_secondrow'}).text.strip()
                    original_price = price_div.find('div', attrs={'class': 'col search_price discounted responsive_secondrow'})\
                        .find('span').text.strip()
                    price = {'original_price': original_price, 'diskon': diskon, 'diskon_price': diskon_price}
                else:
                    price = price_div.text.strip()

                platform_datas = seller.find('div', attrs={'class': 'col search_name ellipsis'}).find('p').find_all('span')
                platforms = []
                for platform_data in platform_datas:
                    platforms.append(platform_data['class'])
                self.result.append({'title': title, 'pic_url': pic_url, 'released': released, 'price': price, 'platforms': platforms})

    def get(self):
        return self.result

    def generate_cvs(self):
        csv_writer = csv.writer(open('result.csv', 'w+', encoding='utf8', newline=''))
        values = []
        for value in self.result[0].keys:
            values.append(value)

        csv_writer.writerow(['title', 'price', 'desc', 'condition', 'url', 'picture'])
        for detail in self.result:
            values = []
            for value in detail:
                values.append(value)
            csv_writer.writerow(values)
