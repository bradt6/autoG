import scrapy
from ..items import AutogramItem
import sys

class PicSpider(scrapy.Spider):
    name = "doit"
    start_urls = ['https://www.pexels.com/search/sea/']


    # def start_requests(self):
    #     start_urls = ['https://www.pexels.com/popular-photos/'] 

        # for url in urls:
        #     yield scrapy.Request(url = url, callback=self.parse)

    # def parse(self, response):
    #     links_to_images = response.css(
    #         ".photo-item__img").xpath("@data-big-src").extract()
    #     yield {
    #         "URL" : links_to_images
    #     }

    def parse(self, response):

        items = AutogramItem()

        # already_been = list()

        content_page = response.css(
            ".photo-item__link").xpath("@href").extract()
        
        try:     
                links = response.css(".js-photo-page-image-img")

                name = links.xpath("@alt").extract()
                finalName = name[0]

                imageURL = links.xpath("@srcset").extract()
                highDefImageURL = [URL.split(",")[-1] for URL in imageURL]
                onlyURL = highDefImageURL[0]

                tagsLink = response.css(".rd__tag::text").extract()
                hashedTags = ["#" + tag for tag in tagsLink]                             

                items['name'] = finalName
                items['imageURL'] = onlyURL
                items['tags'] = hashedTags
                print("********************************************")
                print(items)
                print("##################################")
                yield items
        except:
            print("NO DATA")
    
        for page in content_page:    
            if content_page is not None:
                # already_been.append(page)
                yield response.follow("https://www.pexels.com" + page, callback=self.parse)
