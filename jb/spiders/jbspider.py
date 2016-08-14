# -*- coding:utf-8 -*-
import scrapy
from jb.items import JbItem
from scrapy.http import Request
base_url = "http://www.jb51.net"
parse_list = "http://www.jb51.net/list/list_15_%s.htm"
class JbSpider(scrapy.Spider):
    name = "jb"
    allowed_domains = ["dmoz.org"]
    start_urls = ["http://www.jb51.net/list/list_15_1.htm"]
    allowed_domains = ''

    def parse(self, response):
        _params = response.selector.xpath('//div[@class="dxypage clearfix"]/a[last()]/@href').re('(\d+)')
        count = int(_params[1])  # 总页数
        # 处理
        for page in range(1, count):
            url = (parse_list % page)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        """解析文章列表"""
        article_urls = response.selector.xpath('//div[@class="artlist clearfix"]/dl/dt/a/@href').extract()
        print article_urls
        # for article_url in article_urls:
            # yield Request(base_url + article_url, callback=self.parse_article)
            # print article_url

    def page_article(self, response):
        """解析文章内容"""
        title = response.selector.xpath('//div[@class="title"]/h1/text()').extract()[0]
        content = response.selector.xpath('//div[@id="content"]').extract()[0]
        tags = ','.join(response.selector.xpath('//div[@class="tags mt10"]/a/text()').extract())
        item = JbItem()
        item['title'] = title
        item['content'] = content
        item['tags'] = tags
        self.show(item);

    def show(self, a):
        for title in a['title']:
            print  title