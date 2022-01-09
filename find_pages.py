import scrapy
import re

MAX_DEPTH = 3

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.economist.com/',
    ]

    hosts = {}

    def is_in_hosts(self, url, origin):
        if re.search('^/', url):
            host = origin
            print("Host: " + host)
        elif re.search('^(http|https)?:?//', url):
            host = re.search('//([^/]+)/?', url).group(1)
        else:
            host = "None"
        if host not in self.hosts:
            return False

        return self.hosts[host] >= MAX_DEPTH

    def parse(self, response):

        if not re.search('text/html', response.headers['Content-Type'].decode('utf-8')):
            return

        for quote in response.xpath('//*[@*[contains(., \'/etc.clientlibs/\')]]'):
            yield {
                'src': quote.get(),
                'page': response.url,
            }
        for resource in response.xpath('//*[@*[starts-with(., \'/content/dam/\')]]'):
            yield {
                'src': resource.get(),
                'page': response.url,
            }

        host = re.search('//([a-zA-Z0-9.]+)/', response.url).group(1)

        if host not in self.hosts:
            self.hosts[host] = 0

        if host in self.hosts and self.hosts[host] < MAX_DEPTH:
            self.hosts[host] = self.hosts[host] + 1

            next_pages = response.xpath('//a/@href').getall()
            if next_pages is not None:
                for next_page in next_pages:
                    if not (re.search('^(tel|mailto):', next_page) or self.is_in_hosts(next_page, host)):
                        yield response.follow(next_page, self.parse)
