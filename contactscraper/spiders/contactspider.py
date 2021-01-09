import logging
import phonenumbers as pn
import re

from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from contactscraper.items import ContactInfo


class ContactSpider(CrawlSpider):
    """
    Info:
        This spider recursively crawls a site starting from a root (top-level domain)
        It will not deviate from the root domain but will explore all paths
        in depth-first order

        Each page is scraped for potential emails, logos and or phone numbers.
    """

    def __init__(self, root=None, start_urls=[], allowed_domains=[], region='US', scrape_emails=True,
                 scrape_numbers=True, scrape_logos=True, max_results=False, **kwargs):
        """
        * * * * * * 
        * Initilize the spider with Controller attributes
        *
        * * * * * * 
        * @param <String> root       : the top level domain to start from
        *
        *
        * @return void
        */
        """

        self.root = root
        self.seen_urls = set()

        self.start_urls = start_urls
        self.allowed_domains = allowed_domains
        self.region = region
        self.scrape_emails = scrape_emails
        self.scrape_numbers = scrape_numbers
        self.scrape_logos = scrape_logos
        self.total_results = 0
        self.max_results = max_results
        logging.info(self.max_results)

        super().__init__(**kwargs)

    name = 'contact_spider'

    rules = (
        Rule(LinkExtractor(), callback='parse_item'),
    )

    def parse_item(self, response):
        """
        * * * * * * 
        * Uses regex to broad scrape the entirety of the HTML for numbers and emails
        * on the current web page, if any emails or phone numbers exist
        * they will be passed down the item pipeline for further validation.
        * * * * * * 
        * @param <Response> response     : Scrapy Response object from the newest page
        * @yield ContactInfo             : scrapy Item class with emails, logos, numbers, and url
        */
        """

        contact_info = ContactInfo()

        contact_info['url'] = response.url
        html_text = str(response.text)

        potential_numbers = [pn.format_number(match.number, pn.PhoneNumberFormat.E164) for match in
                             pn.PhoneNumberMatcher(html_text, self.region)]

        potential_emails = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', html_text)

        potential_logos = []
        soup = BeautifulSoup(html_text)
        try:
            potential_logos = [soup.findAll('img')[0]['src']]
        except IndexError:
            pass

        if response.url not in self.seen_urls and \
                (len(potential_numbers) != 0 or len(potential_emails) != 0 or len(potential_logos) != 0):

            if self.scrape_emails:
                contact_info['emails'] = potential_emails
            else:
                contact_info['emails'] = []

            if self.scrape_numbers:
                contact_info['numbers'] = potential_numbers
            else:
                contact_info['numbers'] = []

            if self.scrape_logos:
                contact_info['logos'] = potential_logos
            else:
                contact_info['logos'] = []

            if not self.max_results or self.total_results < self.max_results:
                self.total_results += 1
                self.seen_urls.add(response.url)
                yield contact_info

            logging.info(f"found {self.total_results}/{self.max_results} results")
            if self.total_results >= self.max_results:
                raise CloseSpider('Reached max results')
