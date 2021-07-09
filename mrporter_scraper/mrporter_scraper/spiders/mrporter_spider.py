import scrapy
import re
import json
from mrporter_scraper.items import MrporterScraperItem


class mrporterSpider(scrapy.Spider):

    name = "mrporter"
    base_url = "https://www.mrporter.com/en-us/mens/azdesigners"
    designer_api_url = "https://www.mrporter.com/api/inseason/search/resources/store/mrp_us/productview/" \
                       "byCategory?attrs=true&category=%2Fdesigner%2F{0}&locale=en_GB&pageNumber=1&pageSize=60"
    counter = 1
    attribute_labels = ["Country Of Origin", "Size", "Chest", "Back Length", "Waist", "Hazardous Materials",
                        "Brand Colour", "Shoulder", "Brand Size", "Sleeve Length", "Shoulder Width"]

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        designers = response.selector.css("a.DesignerList0__designerName::attr(href)").extract()
        print(len(designers))
        for designer_link in designers:
            yield scrapy.Request("https://www.mrporter.com" + designer_link, callback=self.parse_listing)
            # designer_name = re.findall("designer\/(.*)", designer_link)[0]
            # yield scrapy.Request(self.designer_api_url.format(designer_name), callback=self.parse_listing)

    def parse_listing(self, response):
        products = response.selector.css("div.ProductGrid52 > a::attr(href)").extract()
        # yield scrapy.Request("https://www.mrporter.com/en-us/mens/product/mr-p/clothing/winter-coats/checked-brushed-virgin-wool-and-llama-hair-blend-coat/33599693056299663",
        #                      callback=self.parse_product_details)
        for product_link in products:
            yield scrapy.Request("https://www.mrporter.com" + product_link, callback=self.parse_product_details)
        next_page = response.selector.css("a.Pagination7__next::attr(href)").extract_first()
        if next_page:
            if "https://www.mrporter.com" + next_page != response.url:
                yield scrapy.Request("https://www.mrporter.com" + next_page, callback=self.parse_listing)


    def parse_product_details(self, response):
        script = response.selector.css("script::text").extract()
        script = [s for s in script if "window.state" in s][0].replace("window.state=", "")
        data = json.loads(script)
        # try:
        #     text = open("html.txt", "a")
        #     text.write(response.text + "\n")
        #     text.close()
        # except UnicodeError:
        #     pass
        for product in data["pdp"]["detailsState"]["response"]["body"]["products"]:
            for colour in product["productColours"]:
                for sku in colour["sKUs"]:
                    itm = MrporterScraperItem()
                    itm["brand"] = response.selector.css('meta[itemprop="name"]::attr(content)').extract_first()
                    itm["product_id"] = re.findall(".*\/(.*)", response.url)[0]
                    itm["url"] = response.url
                    itm["title"] = response.selector.css("p.ProductInformation83__name::text").extract_first()
                    itm["description"] = response.selector.css("div.EditorialAccordion83__accordionContent--editors_notes").extract_first()
                    images = response.selector.css('img.Image18__image::attr(src)').extract()
                    itm["images"] = ["https:" + i for i in list(set(images)) if i.endswith(".jpg")]
                    videos = response.selector.css("video.HtmlVideoPlayer2__video > source::attr(src)").extract()
                    if videos:
                        itm["videos"] = ["https:" + v for v in videos]
                    else:
                        itm["videos"] = []
                    categories = []

                    for c in response.selector.css("a.ShopMore83__link::text").extract():
                        if c not in categories:
                            categories.append(c)
                    itm["category"] = ">".join(categories)
                    itm["additional_features"] = response.selector.css("div.EditorialAccordion83__a"
                                                                       "ccordionContent--size_and_fit li::text").extract() \
                                                 + response.selector.css("div.EditorialAccordion83__accordionContent--details_and_care li::text").extract()
                    itm["additional_features"] = [i.strip() for i in itm["additional_features"]]
                    itm["age_group"] = None
                    itm["capacity"] = None
                    itm["color"] = colour["label"]
                    itm["SKU"] = sku["partNumber"]
                    itm["UPC"] = None
                    attribute_dict = {}
                    for attribute in sku["attributes"]:
                        if attribute["label"] in self.attribute_labels:
                            attribute_dict[attribute["label"]] = attribute["values"]
                    itm["attributes"] = attribute_dict
                    self.counter += 1
                    yield itm
        # text_itm = TextItem()
        # text_itm["text"] = response.body
        # yield text_itm
