# scrapy runspider beer_spider.py -o top-beers.json
# creates a top-beers.json file

import scrapy
from beerspider.items import BeerItem


class TopBeersSpider(scrapy.Spider):
    name = 'topbeers'
    start_urls = ['http://www.beeradvocate.com/lists/top/']

    def parse(self, response):
        rows = response.xpath('//*[@id="ba-content"]/table//tr')
        for row in rows:
            # this is empty for first couple rows that aren't beers
            if not row.xpath('.//td[@class="hr_bottom_light"]'):
                continue

            item = BeerItem()
            # SUCKY HACKs: the table markup is not good
            d = row.xpath('.//text()').extract()
            if len(d) < 8:
                # not sure what to do in this case, skip it
                continue
            item['rank'] = d[0]
            item['beer'] = d[1]
            item['brewery'] = d[2]
            item['style'] = d[3]
            if len(d) == 9:  # we have ABV, else assume it's missing
                item['abv'] = self.make_number(d[4])
                item['weighted_rank'] = self.make_number(d[5])
                item['reviews'] = self.make_number(d[6])
                item['hads'] = self.make_number(d[8])
            else:
                item['weighted_rank'] = self.make_number(d[4])
                item['reviews'] = self.make_number(d[5])
                item['hads'] = self.make_number(d[7])

            urls = row.xpath('.//a/@href').extract()
            item['beer_url'] = urls[0]
            item['brewery_url'] = urls[1]
            item['style_url'] = urls[2]
            beer_url = response.urljoin(urls[0])
            request = scrapy.Request(beer_url, callback=self.parse_beer_contents)
            request.meta['item'] = item
            yield request

    def parse_beer_contents(self, response):
        """find the location for the brewery"""
        item = response.meta['item']
        places = response.xpath('//a[contains(@href,"place/directory")]/text()').extract()
        # should be city, country, directory
        # or country, directory
        # I haven't seen any that have more than 3 but it's a big assumption :(
        if len(places) > 2:
            item['state'] = places[0]
            item['country'] = places[1]
        else:
            item['country'] = places[0]
        return item

    @staticmethod
    def make_number(value):
        """Not super sophisticated - just removes some characters from the field"""
        translation_table = dict.fromkeys(map(ord, '/| ,%ABV'), None)
        value = value.translate(translation_table).strip()
        if '.' in value:
            return float(value)
        else:
            return int(value)
