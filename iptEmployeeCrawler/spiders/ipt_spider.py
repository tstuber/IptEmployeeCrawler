import scrapy
from unidecode import unidecode

# Command Line call to start cralwer:
# >
# > scrapy crawl ipt -o iptEmployees.json 
# >

class QuotesSpider(scrapy.Spider):
    name = "ipt"

    def start_requests(self):
        urls = ['https://ipt.ch/person']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for employee in response.css('ul.og-grid li'):
            
            # Remove Doktor.
            code = employee.css('a').xpath('@data-title').extract_first()
            if "Dr. " in code:
                code = code.replace("Dr. ","")

            code = unidecode(code)

            vorname = code.split(' ', 1)[0]
            nachname = code.split(' ', 1)[1]

            # first char from vorname, first two chars from nachname to build code. 
            code = vorname[:1] + nachname [:2]

            yield {
                'code': code.upper(),
                'name': employee.css('a').xpath('@data-title').extract_first(),
                'function': employee.css('a').xpath('@data-funktion').extract_first(),
                'slogan': employee.css('a').xpath('@data-blockquote').extract_first(),
                'picture': employee.css('a').xpath('@data-largesrc').extract_first(),
            }