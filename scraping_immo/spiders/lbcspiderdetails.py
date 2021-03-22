import scrapy
from urllib.parse import urljoin
import colorama
colorama.init()
from termcolor import colored, cprint

class LbcSpiderDetails(scrapy.Spider):
    name = "lbcdetails"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'}
    start_urls = ['https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france']

#fonction permettant de recenser l'ensemble des liens menant vers des annonces immobilières et d'y accéder
    def parse(self, response):
        ads_list = response.css('a.styles_Link__30F66::attr(href)').extract()
        for ad in ads_list:
            url = urljoin(response.url, ad)
            yield scrapy.Request(url, callback=self.parse_ad)

        next_page = 'https://www.leboncoin.fr'+ response.css('a._3-yvP:nth-child(3)').attrib['href']
        #1ère condition à retirer si l'on souhaite scraper toutes les pages 
        if next_page == 'https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/p-3': 
            raise CloseSpider()
        elif next_page is not None:  
            yield response.follow(next_page, callback = self.parse)
            
#fonction permettant d'extraire les informations qui nous intéressent de chaque annonce immobilière 
    def parse_ad(self, response):

        for info in response.css('div.css-709yn1'):
            yield {
                'titre': info.css('h1.-HQxY._3OFYf._2l1lk._38n__._2QVPN._3zIi4._2-a8M._1JYGK._35DXM::text').extract_first(),
                'nbre_pièces': info.css('div.css-iel3r1').css('span._137P-.P4PEa._3j0OU::text').extract_first(),
                'mètre_carré': info.css('div.css-iel3r1').css('span._137P-.P4PEa._3j0OU:nth-child(2)::text').extract_first(), 
                'ville': info.css('div.css-iel3r1').css('span._137P-.P4PEa._3j0OU:nth-child(3)::text').extract_first(),
                'description': info.css('span._1fFkI::text').get(), 
                'type_de_bien': info.css('span._3eNLO._38n__._137P-.P4PEa._35DXM::text').extract_first(),
            }