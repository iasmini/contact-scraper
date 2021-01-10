# -*- coding: utf-8 -*-
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import os
import phonenumbers as pn
import re

from email_validator import validate_email, EmailNotValidError
from urllib.parse import urljoin


class ContactscraperPipeline:
    def open_spider(self, spider):
        filename = 'output.json'
        try:
            os.remove(filename)
        except OSError:
            pass

        self.file = open(filename, 'a+')
        self.emails = set()
        self.numbers = set()
        self.logos = set()
        self.url_map = {}

    def close_spider(self, spider):
        output = [{'url': url, 'emails': list(contact['emails']), 'numbers': list(contact['numbers']),
                   'logos': list(contact['logos'])} for url, contact in self.url_map.items()]

        self.file.write(json.dumps(output))

        self.file.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        emails, numbers, logos, url = item['emails'], item['numbers'], item['logos'], item['url']

        if len(emails) == len(numbers) == 0 == len(logos) == 0:
            return False

        # For every URL, a set of phone numbers, logos and emails found
        if url not in self.url_map:
            self.url_map[url] = {'numbers': set(),
                                 'emails': set(),
                                 'logos': set()
                                 }

        for email in emails:
            try:
                valid = validate_email(email)
                ascii_email = valid.ascii_email
                known_emails = self.url_map[url]['emails']
                if ascii_email not in known_emails:
                    known_emails.add(ascii_email)

            except EmailNotValidError as e:
                logging.debug(f"email not valid \n\t{email}")

        for number in numbers:
            try:
                num = pn.parse(number, None)
                known_numbers = self.url_map[url]['numbers']
                if pn.is_valid_number(num) and number not in known_numbers:
                    number = str(number)
                    number = re.sub(r'[^\d()+]+', ' ', number)
                    known_numbers.add(number)
            except Exception as e:
                logging.debug(f'Number not parsed: \n\t{str(e)}')

        for logo in logos:
            known_logos = self.url_map[url]['logos']
            if logo not in known_logos:
                url_logo = urljoin(url, logo)
                known_logos.add(url_logo)

        return item
