# Scrape for emails, logos and phones
import os
import sys

from contactscraper.controller import Controller
from contactscraper.controller.config import get_parser

config = get_parser()
try:
    scrape_numbers = config.getboolean('scraper', 'scrape_numbers')
    scrape_emails = config.getboolean('scraper', 'scrape_emails')
    scrape_logos = config.getboolean('scraper', 'scrape_logos')
    region = config['scraper']['region']
    max_results = int(config['scraper']['max_results'])
except KeyError as e:
    print('Invalid settings. Check ini files on contactscraper/controller/config.ini')
    print(e)
    sys.exit(0)

filename = 'output.json'
try:
    os.remove(filename)
except OSError:
    pass

starting_urls = list()
with open('contactscraper/controller/websites.txt') as f:
    for line in f:
        starting_urls.append(line)

instance = Controller(starting_urls=starting_urls,
                      scrape_numbers=scrape_numbers,
                      scrape_emails=scrape_emails,
                      scrape_logos=scrape_logos,
                      region=region,
                      max_results=max_results)

instance.scrape()
