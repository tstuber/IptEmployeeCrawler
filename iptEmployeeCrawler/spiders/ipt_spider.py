import scrapy
from unidecode import unidecode

# Command Line call to start cralwer (owerwrites export)
# >
# > scrapy crawl ipt -t json -o  - > iptEmployees.json
# >

class QuotesSpider(scrapy.Spider):
    name = "ipt"

    def start_requests(self):
        urls = ['https://ipt.ch/person']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def derive_code(self, name):
        ### Create employee abbreviation ###
        # Remove Umlaute.
        fullname = unidecode(name)

        # Remove Titles from names.
        if "Dr. " in fullname:
            fullname = fullname.replace("Dr. ","")

        # Derive first and last name.
        firstname = fullname.split(' ', 1)[0].strip();
        lastname = fullname.split(' ', 1)[1].strip();

        # Ugly exceptions.
        if 'Schwarb' == lastname:
            code = 'RSW'
        elif 'David Konatschnig' == fullname:
            code = 'DKN'
        else:
            # first char from vorname, first two chars from nachname to build code.
            code = firstname[:1] + lastname [:2]
        return code

    def parse(self, response):
        for employee in response.css('ul.og-grid li'):

            # Get employee element.
            name = employee.css('a').xpath('@data-title').extract_first().strip()
            code = self.derive_code(name)

            yield {
                'code': code.upper(),
                'name': employee.css('a').xpath('@data-title').extract_first().strip(),
                'function': employee.css('a').xpath('@data-funktion').extract_first().strip(),
                'slogan': employee.css('a').xpath('@data-blockquote').extract_first().strip(),
                'picture': employee.css('a').xpath('@data-largesrc').extract_first().strip(),
            }
