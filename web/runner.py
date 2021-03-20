from web.steam_scaper import SteamScraper

url = 'https://store.steampowered.com/'

scraper = SteamScraper()
scraper.scrape()
for data in scraper.get():
    print(data)
