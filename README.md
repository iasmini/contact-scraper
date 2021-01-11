[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)]() [![Contributions](https://img.shields.io/badge/Contributions-Welcome-blue)]() [![Release](https://img.shields.io/badge/Release-Stable-green)]() [![Maintained](https://img.shields.io/badge/Maintenance-Inactive-lightgrey)]() 
# contact-scraper 

contact-scraper gathers all available logos, phone numbers and emails from a given domain by recursively travesing and scraping the entire site-map. It also validates the emails and phone numbers. Built upon Scrapy.

## **Disclaimer**
This tool is for educational and/or legal scraping purposes only, usage of contact-scraper for scraping targets without prior mutual consent is illegal. Developers of contact-scraper and its dependencies assume no liability and are not responsible for any misuse or damage caused by this program.

## **Installation**
1. To install Scrapy on Ubuntu (or Ubuntu-based) systems, you need to install these dependencies:   
    `sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`
2. Clone the project:  
    `git clone https://github.com/iasmini/contact-scraper.git`
3. Install [Docker](https://docs.docker.com/engine/install/)


## **Usage**
You must set the urls in contactscraper/controller/websites.txt:  
`starting_urls` is a list of URLs you\'d like to start scraping from. A spider will be deployed on each URL, it won\'t deviate to any links that don\'t contain the root url. For example, passing in `https://www.python.org/privacy/` will allow any URL with the root domain of `python.org` to be scraped.

You must set the configurations in contactscraper/controller/config.ini:  
`scrape_logos`, `scrape_emails` & `scrape_numbers` are booleans depicting if you want to gather logos, emails or numbers, respectively.

`region` is the [region](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/shortdata) you wish to validate numbers against, most of NA uses "US" region validation.

`max_results` is the maximum number of unique URLs that contain either emails or phone numbers you\'d like to receive. Must be an integer greater than 0.

Run the command below on the command line at the project root folder:
```shell
docker run -d --mount type=bind,source="$(pwd)"/,target=/code contact-scraper:latest
```

Results get written as a list of JSON objects in *output.json* saved at the project root.

Json objects are stored in the following format
```python
[
  {
    "url": "https://www.python.org/",
    "emails": [ ],
    "numbers": [ ],
    "logos": [
      "https://www.python.org/static/img/python-logo.png"
    ]
  },
  {
    "url": "https://www.python.org/psf/sponsorship/sponsors/",
    "emails": [ ],
    "numbers": [ ],
    "logos": [
      "https://www.python.org/static/img/psf-logo.png"
    ]
  },
  {
    "url": "https://www.python.org/privacy/",
    "emails": [
      "psf@python.org"
    ],
    "numbers": [ ],
    "logos": [
      "https://www.python.org/static/img/python-logo.png"
    ]
  },
  {
    "url": "https://www.python.org/about/legal/",
    "emails": [ ],
    "numbers": [ ],
    "logos": [
      "https://www.python.org/static/img/psf-logo.png"
    ]
  },
  {
    "url": "https://status.python.org/",
    "emails": [ ],
    "numbers": [
      "+16505551234"
    ],
    "logos": [ ]
  }
]
```
## **Validation**
- Emails are validated against modern specs with the [email_validator library](https://github.com/JoshData/python-email-validator "email_validator library")
- Phone numbers are validated by [region](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/shortdata "region") using the [Python implementation](https://github.com/daviddrysdale/python-phonenumbers "Python implementation") of [Google\'s libphonenumber library](https://github.com/google/libphonenumber "Google\'s libphonenumber library")
