from flask import Flask, render_template

from web.steam_scraper import SteamScraper

url = 'https://store.steampowered.com/'

scraper = SteamScraper()
scraper.scrape()
top_seller_datas = scraper.get()

app = Flask(__name__)

@app.route('/')
def test():
    return render_template('top_seller.html', datas=top_seller_datas)

if __name__ == '__main__':
    app.run(debug=True)