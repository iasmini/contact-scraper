# Scrape for emails, logos and phones

from contactscraper.controller import Controller

instance = Controller(starting_urls=['https://www.silexsistemas.com.br/'],
                      scrape_numbers=True,
                      scrape_emails=True,
                      scrape_logos=True,
                      region="BR")

instance.scrape()
