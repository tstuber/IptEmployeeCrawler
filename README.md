# IptEmployeeCrawler

Crawls the employee's from ipt from their public website and stores the results as a json export.

### Installation
Requires python with the [scrapy](https://scrapy.org) package.

### Execution
Invoking ipt-spider:
    scrapy crawl ipt -t json -o  - > iptEmployees.json
