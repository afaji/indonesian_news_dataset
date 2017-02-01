import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://bisniskeuangan.kompas.com/search/bisniskeuangan/2014-7-31',
    ]

    def parse(self, response):
        content_urls = []
        content_titles = []
        for news in response.css('div.list-latest'):
            content_urls.append(   news.xpath('a/@href').extract_first() )
            content_titles.append(  news.xpath('a/text()').extract_first()  )
        f = open('url.csv', 'w')
        for url, title in zip(content_urls, content_titles):
            f.write('%s;%s\n'% (url, title) )
        f.close()
        for url in content_urls:
            yield scrapy.Request(url, callback=self.parse_content)

            
    def parse_content(self, response):
        content = response.css('div.kcm-read-text').xpath('text()').extract()
        print(content)