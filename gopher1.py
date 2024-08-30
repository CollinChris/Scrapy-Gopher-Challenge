import scrapy

class Gopher1Spider(scrapy.Spider):
    name = "gopher1"
    allowed_domains = ["gopher1.extrkt.com"]
    start_urls = ["https://gopher1.extrkt.com/"]


    def parse(self, response):
        product_links = response.xpath("//div[@class='shop-kit-poroduct style1']/a/@href").getall()
        for product_url in product_links:
            print("#############product loop##########")
            yield response.follow(product_url, callback = self.parse_product_page)

        next_page = response.xpath("//nav[@class='woocommerce-pagination']//a[@class='next page-numbers']/@href").get()
        if next_page != None:
            yield response.follow(next_page, callback = self.parse)


    def parse_product_page(self, response):  #in product url
        #table = response.xpath("//div[@class = 'woocommerce-tabs wc-tabs-wrapper']").get()
        print("#############parsing product page#############")
        product_name = response.xpath("//div[@class='summary entry-summary']/h1[@class='product_title entry-title']/text()").get()
        product_price = response.xpath("//span[@class='woocommerce-Price-amount amount']/bdi/text()").get()
        product_descript = response.xpath("//div[@class = 'woocommerce-tabs wc-tabs-wrapper']//p/text()").get()
        product_sizes = response.xpath("//div[@class = 'woocommerce-tabs wc-tabs-wrapper']//td[@class = 'woocommerce-product-attributes-item__value']/p/text() ").get()
        product_colours = response.xpath("//th[contains(text(), 'Color')]/following-sibling::td[@class='woocommerce-product-attributes-item__value']/p/text()").getall()

        yield{'product_name'     : product_name,
              'product_price'    : product_price,
              'product_descript' : product_descript,
              'product_sizes'    : product_sizes,
              'product_colours'  : product_colours}
  