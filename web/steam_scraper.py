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
                url = seller['href']
                title = seller.find('span', attrs={'class': 'title'}).text
                pic_url = seller.find('div', attrs={'class': 'col search_capsule'}).find('img')['src']
                released = seller.find('div', attrs={'class': 'col search_released responsive_secondrow'}).text
                price_div = seller.find('div', attrs={'class': 'col search_price responsive_secondrow'})

                discount = ''
                original_price = ''
                if price_div is None:
                    price_div = seller.find('div', attrs={
                        'class': 'col search_price_discount_combined responsive_secondrow'})
                    price = price_div.find('div', attrs={
                        'class': 'col search_price discounted responsive_secondrow'}).contents[3]
                    discount = price_div.find('div', attrs={
                        'class': 'col search_discount responsive_secondrow'}).text.strip()
                    original_price = price_div.find('div', attrs={
                        'class': 'col search_price discounted responsive_secondrow'}).find('span').text.strip()
                else:
                    price = price_div.text.strip()

                platform_datas = seller.find('div', attrs={'class': 'col search_name ellipsis'}).find('p').find_all(
                    'span')
                platforms = []
                for platform_data in platform_datas:
                    platform_class = platform_data['class']
                    if 'win' in platform_class:
                        platforms.append('Windows OS')
                    elif 'linux' in platform_class:
                        platforms.append('Linux OS')
                    elif 'mac' in platform_class:
                        platforms.append('Mac OS')
                    elif 'vr_supported' in platform_class:
                        platforms.append('VR Supported')
                    elif 'vr_required' in platform_class:
                        platforms.append('VR Only')
                    else:
                        platforms.append('Not Supported: {}'.format(platform_class))
                self.result.append(
                    {'title': title, 'url': url, 'pic_url': pic_url, 'released': released, 'price': price,
                     'discount': discount, 'original_price': original_price, 'platforms': platforms})

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
