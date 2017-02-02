import scrapy
from datetime import timedelta, date

# helper
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def url_date_generator():
    start_date = date(2016, 1, 2)
    end_date = date(2016, 1, 3)
    date_url = [("http://bisniskeuangan.kompas.com/search/bisniskeuangan/" + single_date.strftime("%Y-%m-%d")) for single_date in daterange(start_date, end_date)]
    
    return date_url


class QuotesSpider(scrapy.Spider):
    name = "kompas"
    start_urls = url_date_generator()
    f_title = open('url.csv', 'w')
    f_content = open('content.txt','w')

    def parse(self, response):
        content_urls = []
        content_titles = []
        for news in response.css('div.list-latest'):
            content_urls.append(   news.xpath('a/@href').extract_first() )
            content_titles.append(  news.xpath('a/text()').extract_first()  )

        for url, title in zip(content_urls, content_titles):
            self.f_title.write('%s;%s\n'% (url, title) )
        
        for url in content_urls:
            yield scrapy.Request(url, callback=self.parse_content)

            
    def parse_content(self, response):
        content = response.css('div.kcm-read-text').xpath('node()//text()').extract()
        
        #join them
        res = ""
        for line in content:
            res += line.encode('ascii', 'ignore')
        self.f_content.write('%s\n'% res)
