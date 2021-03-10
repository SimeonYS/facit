import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FacitItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FacitSpider(scrapy.Spider):
	name = 'facit'
	start_urls = ['https://www.facitbank.dk/nyheder/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="w-full h-full flex flex-col"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="text-blue-200 text-lg"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="news-text"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FacitItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
