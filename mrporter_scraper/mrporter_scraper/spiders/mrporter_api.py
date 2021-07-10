import scrapy
import re
import json
from mrporter_scraper.items import MrporterScraperItem


class mrporterSpider(scrapy.Spider):

    name = "mrporter_api"
    base_url = "https://www.mrporter.com/en-us/mens/azdesigners"
    designer_api_url = "https://www.mrporter.com/api/inseason/search/resources/store/mrp_us/productview/" \
                       "byCategory?attrs=true&category=%2Fdesigner%2F{0}&locale=en_GB&pageNumber={1}&pageSize=600"
    counter = 1
    attribute_labels = ["Country Of Origin", "Size", "Chest", "Back Length", "Waist", "Hazardous Materials",
                        "Brand Colour", "Shoulder", "Brand Size", "Sleeve Length", "Shoulder Width"]
    headers = {
        'authority': 'www.mrporter.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'application-version': '4.137.0',
        'x-ibm-client-id': '0b1e2c22-581d-435b-9cde-70bc52cba701',
        'label': 'getCategoryBySeoPath',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'application-name': 'Blue lobster',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.mrporter.com/en-pt/mens/designer/{0}?pageNumber={1}',
        'accept-language': 'el-GR,el;q=0.9,en;q=0.8,de;q=0.7,it;q=0.6',
        'cookie': 'LPVID=ViYzc5NzhjZjQ1MDIzMGQ5; geoIP=US; Y-City=US--; country_iso=US; lang_iso=en; AKA_A2=A; bm_sz=D6BEF97E7351C86B349278BDB3F9980F~YAAQjUUVArUfQ3d6AQAArI7njQz+YyMCDFi9e+FP98iFxpGZSuGMSXlk5tMuLMxoKqdXGQ6e+ycv0C1AlU+/XD1w9WavaMqB5VVIf3AUInJ1RTMvw5pwYEHjpn1hA/1vZjob9asOUNYZJdOiyQY2g4r8TqIPXSgeT4AQ1bWVMjDHndoRG33c7qG29Nm/Y61tDN3gJjU1SPt9hUY1k3tn4sndV8hG6XsVB94KmKFgG2JcwyY9biQJpwbjFOKy0LwLMot6eQ+ggetJYzaDFGkEN0HGaclh+/XMeHGMoUkX; LPSID-73583570=yKyMyBXETF6LriXezfeLJA; bm_mi=91922F3826592964BFECEFF9A44E2AEE~pijlnkMBOOikNvdo16+bFZbqG8xQ10VBQiJwbShSpQB5PYdMhqBsgDXAutDXqYUpV+uK3LOVPT0fWHj4sBwSat6ThnS9V5C0F3tBYgkWQ+ll9VmNsRn3jB2epeXHKVW0QZK72rFQEj82i984YXC26oViGTwKpzBfK4+Z5ARxN+JfWoUmAYY/uCAgAjrytdAkeocSSTI0XdfdsCOxNJ1p1C8W+1/H6Bf1YUyZEmZlGTiYSN1lCNMB22/+ITPhTVh0bq1je9HZmy4b4l8t5lZE1+5Sc6FS69YSt38GBadpoT8JjdPxRJJzX23Ztze2jvpRyRmjDlbPCqRvx9ACffPJFRJsaDccJtu6ItDt6J+CoEMawN+GE0ONpxhVgcZ52GiCPmLHKbWYA3bFRf1RsYpmJSOeXSHvxN4JhubShTinoJ8=; bm_sv=ADB72B9C28BFA46C1655128ECE19EE4C~HusdybBa4nZVfiFwg07i9H1KBdX2DY8RZi03DmZsWfzXi8ojaQtorM+dXPOhKVtGPPg6C0OS6rPUweO07dwkbMJ84bTiWP5api46MyDeX0QlbweSgZnPm7fQ1cl5zxnOGWDSxgAeABYKCdqqy7hG1yN544/d/tRGLAB693lAjEY=; ak_bmsc=F864B89EC421E6EFACD20FF619A50E1C~000000000000000000000000000000~YAAQD/fSFygcsRh6AQAAo032jQzNSo9JPr7u2jmAP64Rwz9kcXkdNSLjxd0nYTRict02tEjVw9kg5kmiKkiB34KKzwbiuo51BqJcjCcr+/G29zXINXJ7gynIXZG7j2t+RdLun/ZEPt/pZ1fTgeKcep2jtJTipj+wY2U5S893dAwm30Pdk0M4iXUQrtFB7lLFUX+p2RaOqH8ceQWsW5LeixPJlN5Dpe7DlV5y+vornVdONVdR1xD/Iwm9LKarpt21wMT5LZC2g1T6DW49KeHMrWRn4KZkS51ppOb1iPZEB2giIM9zjQzWNWznIz5DN9UDwN2kYiF1QeS+RCDEwMCE7RTRxCuRMxA53ukuuPcV7ps2tynmfR/tK2yC5Qag5+LHsGJswp5VJteqSl2/j5NBM3kGeSB1OX4uOFdt9f8q5JuRi5WfNumhVaKvz6wWDY1e8T/UAvZUfIudLVNV1Ol1l4jLVdbHVwTu+dEL4Kdtp88F/z73dFTVNQ3ZheREYVdFGg7PFm48P01FD1XhkugKyXOCAJrqvjL06Y8TXzjdbpCxpsOajO55znbKpz1S5ct3K9RBdOzipPBfP3x+r+EwOuZ8NnfZzws9tWYwWIQ=; TS016d9db0=01231dfb7f1b8a7168cedf9125447b0e87d84fdcf349c8fb5fc35c0a0254e7fd44282999df2e15a8cc8ade4f6df74a2407b2afd861; _abck=CDBD9D5EF786EE641D9EB260CFD6B8F0~0~YAAQJI8UAoi+tYN6AQAAP2IXjgbDQM1qgoEPhI3CwOmUmXrp4aZ8kfZ0HFJNassQCWuMc/8Cse0h8GT4FL+8RnBgz4/8Kfl8IB6+1pR3VJw0wGZ9OjdGWNHSQeZM0b+WIpbvBSStSLcLeluJU+qse3llGaQnW9E11vhkgX6UhuyB758gB/H629BAN0KKNOTruUurX4EuZlCl2B65+2zP0YLmswXO/0KGpVhQZPKRXVv4g0WjT+nFWnzfVuG1EAdJm8rXeAlmyGZhkKeoVooxpcJp2VjZLDBVrpSPm1eycD4UhdifpIKQMHTK/M6aMy6X/dy/tC2vHsfbJNvLhD4qP+u+3YrccGS/W5GsNWHuCYKn9fCoqRSX4JS3vgdrRR7md7pfBjinVgFd8/r412J0A6ZEqpnpHsVXw12BnDFJPEIjBOsLxVwz1moLu/aawtHIKI/JANkhPcopAyHyre1U~-1~-1~1625885124',
    }

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        designers = response.selector.css("a.DesignerList0__designerName::attr(href)").extract()
        headers = dict(self.headers)
        headers["referer"] = headers["referer"].format("sale", "4")
        yield scrapy.Request(self.designer_api_url.format("sale", "4"), callback=self.parse_listing,
                             meta={"page": 1, "designer": "sale"}, headers=headers)
        # for designer_link in designers:
        #     # yield scrapy.Request("https://www.mrporter.com" + designer_link, callback=self.parse_listing)
        #     designer_name = re.findall("designer\/(.*)", designer_link)[0]
        #     yield scrapy.Request(self.designer_api_url.format(designer_name, "1"), callback=self.parse_listing,
        #                          meta={"page": 1, "designer": designer_name})

    def parse_listing(self, response):
        print(response.url)
        designer_name = response.meta["designer"]
        page = response.meta["page"]
        data = json.loads(response.text)
        headers = dict(self.headers)
        headers["referer"] = headers["referer"].format(designer_name, str(page))
        print(len(data["products"]))
        for product in data["products"]:
            if "46128359902970429" in product["seo"]["seoURLKeyword"]:
                print(product["seo"]["seoURLKeyword"])
            print(product["seo"]["seoURLKeyword"])
            yield scrapy.Request("https://www.mrporter.com/en-us/mens/product/" + product["seo"]["seoURLKeyword"], callback=self.parse_product_details,
                                 dont_filter=True)

        # total_pages = data["totalPages"]
        # if page < total_pages:
        #     yield scrapy.Request(self.designer_api_url.format(designer_name, str(page + 1)), callback=self.parse_listing,
        #                          meta={"page": page + 1, "designer": designer_name}, headers=headers)


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
                    try:
                        itm["full_price"] = float(sku["price"]["wasPrice"]["amount"]) / float(sku["price"]["wasPrice"]["divisor"])
                    except:
                        itm["full_price"] = None
                    try:
                        itm["price_with_discount"] = float(sku["price"]["sellingPrice"]["amount"]) / float(sku["price"]["sellingPrice"]["divisor"])
                    except:
                        itm["price_with_discount"] = None
                    if (itm["price_with_discount"]) and (itm["full_price"] is None):
                        itm["full_price"] = itm["price_with_discount"]

                    attribute_dict = {}
                    for attribute in sku["attributes"]:
                        if attribute["label"] in self.attribute_labels:
                            attribute_dict[attribute["label"]] = attribute["values"]
                    itm["attributes"] = attribute_dict
                    yield itm

