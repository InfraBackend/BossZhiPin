# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from BossZhiPin.items import BossZhiPinItem
from BossZhiPin.spiders.getCookie import GetCookie
import time

class BossZhipinSpider(scrapy.Spider):
    get_cookie = GetCookie()
    name = 'zhipin'   # 运行时爬虫的名称
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1']

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': f'__zp_stoken__={get_cookie.get_cookie()}',
            'Host': 'www.zhipin.com',
            'Origin': 'https://www.zhipin.com',
            'Referer': 'https://www.zhipin.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
    }


    def parse(self, response):
        item =BossZhiPinItem()
        # 获取页面数据的条数
        nodeList = response.xpath('//div[@class="job-primary"]')
        for node in nodeList:
            item["job_title"]=node.xpath('.//div[@class="job-title"]//text()').extract()[0]
            item["compensation"]=node.xpath('.//span[@class="red"]/text()').extract()[0]
            item["company"]=node.xpath('.//div[@class="info-company"]//h3//a/text()').extract()[0]
            company_info=node.xpath('.//div[@class="info-company"]//p/text()').extract()
            temp=node.xpath('.//div[@class="info-primary"]//p/text()').extract()
            item["address"] = ""
            item["seniority"] = temp[0]
            item["education"] = temp[1]
            if len(company_info) < 3:
                item["company_type"] = company_info[0]
                item["company_finance"] = ""
                item["company_quorum"] = company_info[-1]
            else:
                item["company_type"] = company_info[0]
                item["company_finance"] = company_info[1]
                item["company_quorum"] = company_info[2]
            yield item
        next_page=response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()[-1]
        if next_page != "javascript:;":
            base_url="https://www.zhipin.com"
            url=base_url+next_page
            time.sleep(10)  # 设置爬取延迟
            yield Request(url=url,callback=self.parse)
