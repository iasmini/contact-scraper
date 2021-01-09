# Scrape for emails, logos and phones

from contactscraper.controller import Controller

instance = Controller(starting_urls=['https://www.python.org/'],
                      scrape_numbers=True,
                      scrape_emails=True,
                      scrape_logos=True,
                      region="US",
                      max_results=2)

instance.scrape()
