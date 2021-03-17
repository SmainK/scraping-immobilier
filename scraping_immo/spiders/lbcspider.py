import scrapy

class LbcSpider(scrapy.Spider):
    name = "lbc"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'}
    start_urls = ['https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france']

    def parse(self, response): 
        print('Spider lbc is active')       
        for ad_card in response.css("div.css-mi8a1d"):
            yield {
            'title': ad_card.css('p.css-1j9uane.e1koqxhm0::text').get(),
            'price': ad_card.css('span.css-66vicj::text').get(),
            'city_and_date' : ad_card.css('p._2k43C._137P-.P4PEa._3j0OU::text').get() 
            }
        pass

        next_page = 'https://www.leboncoin.fr'+ response.css('a._3-yvP:nth-child(3)').attrib['href']
        if next_page is not None: 
            yield response.follow(next_page, callback = self.parse)
