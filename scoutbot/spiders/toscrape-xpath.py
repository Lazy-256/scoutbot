# -*- coding: utf-8 -*-
import scrapy
import logging


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'https://www.autoscout24.ru/lst/suzuki/swift?sort=age&desc=1&doorfrom=2&doorto=3&ustate=N%2CU&size=20&page=1&cy=NL&priceto=100000&pricefrom=2000&version0=sport&atype=C&',
    ]

    def __init__(self, *args, **kwargs):
        # see: https://doc.scrapy.org/en/latest/topics/logging.html#logging-settings
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        for car in response.xpath('//div[@class="cl-list-element cl-list-element-gap"]'):
            yield {
                # 'title':             car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary-headline"]/div[@class="cldt-summary-titles"]/a/div[@class="cldt-summary-title"]/div[@class="cldt-summary-makemodelversion sc-ellipsis"]//h2/text()').extract_first(),
                'title':             ' '.join(filter(None, car.xpath('.//h2[contains(@class ,"sc-ellipsis")]/text()').extract())),
                'url':               response.urljoin(car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary-headline"]/div[@class="cldt-summary-titles"]/a/@href').extract_first()),
                # 'price':             car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-pricing"]//text()').extract(),
                'price':             car.xpath('.//span[@data-item-name="price"]/text()').extract_first(),
                'milage':            car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-vehicle-data"]/ul[1]/li[1]/text()').extract_first(),
                'relize-date':       car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-vehicle-data"]/ul[1]/li[2]/text()').extract_first(),
                'power':             car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-vehicle-data"]/ul[1]/li[3]/text()').extract_first(),
                'data-place-holder':      car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-vehicle-data"]/ul[1]/li[@data-placeholder=""]/text()').extract_first(),
                'transmission-type': car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-full-item-main"]/div[@class="cldt-summary"]/div[@class="cldt-summary-vehicle-data"]/ul[1]/li[@data-type="transmission-type"]/text()').extract_first(),
                # 'seller':            car.xpath('./div[@class="cldt-summary-full-item"]/div[@class="cldt-summary-seller"]/div[@class="cldt-summary-seller-data"]/div[@class="cldt-summary-seller-company"]//div/text()').extract(),
                'seller':            ' '.join(filter(None, car.xpath('.//div[@class="cldf-summary-seller-data"]//text()').extract())),
            }

        next_page_url = response.xpath(
            '//li[@class="next-page"]/a/@href').extract_first()
        logging.info(next_page_url)
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
