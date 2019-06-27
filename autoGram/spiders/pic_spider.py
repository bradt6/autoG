import scrapy
from ..items import AutogramItem


class PicSpider(scrapy.Spider):
    name = "doit"
    categoery = "beach"
    hashableWord = "".join(categoery.split())
    start_urls = ['https://www.pexels.com/search/{}/?page=1'.format(categoery)]
    page_index = 1
    pic_tags = []

    # def __init__(self):
    #     self.driver = webdriver.Firefox(
    #         executable_path='/anaconda3/bin/geckodriver')

    def start_requests(self):
        request = scrapy.Request(
            url='http://best-hashtags.com/hashtag/{}/'.format(PicSpider.hashableWord), callback=self.parse_2)
        yield request

    def parse(self, response):

        do_not_inclue = ["women", "man", "person", "men", "couple", "lady", "people", "girl", "boy",
                         "girl", "boys", "girls", "baby", "babies", "child", "children", "woman"]

        items = AutogramItem()

        files = response.css(".photo-item__img")
        if files:
            for item in files:
                name = item.xpath("@alt").extract()

                name_to_lower = [word.lower() for word in name]
                comapre = name_to_lower[0]
                compare_split = comapre.split()
                result = any(word_check in compare_split for word_check in do_not_inclue)

                if result:
                    continue
                else:
                    imageURL = item.xpath("@data-big-src").extract()
                    items['name'] = name
                    items['imageURL'] = imageURL
                    items['tags'] = PicSpider.pic_tags
                    print("********************************************")
                    print(items)
                    print("##################################")
                    yield items
        else:
            return

        PicSpider.page_index += 1
        if PicSpider.page_index:
            yield scrapy.Request(url="https://www.pexels.com/search/{}/?page={}".format(PicSpider.categoery, PicSpider.page_index), callback=self.parse)

    def parse_2(self, response):
        tags = response.css(".progression a::text").extract()
        PicSpider.pic_tags = tags
        yield scrapy.Request(url=PicSpider.start_urls[0], callback=self.parse)

    # SELENIUM AUTO SCROLL TO BOTTOM OF PAGE

        # self.driver.get(response.url)

        # SCROLL_PAUSE_TIME = 5.0


# # Get scroll height
#         last_height = self.driver.execute_script("return document.body.scrollHeight")

#         while True:
#             # Scroll down to bottom
#             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#             # Wait to load page
#             time.sleep(SCROLL_PAUSE_TIME)

#             # Calculate new scroll height and compare with last scroll height
#             new_height = self.driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height
