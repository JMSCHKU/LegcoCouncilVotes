from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


from selenium import webdriver

from scrapy import log
import time

from scrapy.http import Request
import urlparse

from legcovotes.items import LegcoVote


class LegcoVotesSpider(CrawlSpider):
    name = "legcovotes"
    allowed_domains = ["www.legco.gov.hk"]
    start_urls = [
        "http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm"
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []

        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.browser = webdriver.Firefox()
        self.browser.get('http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm')
        
    def __del__(self):
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def spider_closed(self, spider):
        self.browser.close()

    def parse(self, response):
        #hxs = HtmlXPathSelector(response)
        #sites = hxs.select('a/[contains(text(),"XML")]/@href').extract()
        sel = self.browser
        #sel.open(response.url)

        #Wait for javscript to load in Selenium
        time.sleep(2.5)

        links = sel.find_elements_by_link_text('(XML)')
        #print links

        for link in links:
            url=urlparse.urljoin("http://www.legco.gov.hk/", link.get_attribute('href'))
            yield Request(url, callback=self.parse_xml_document)    

    def parse_xml_document(self, response):
        return 

        xxs = XmlXPathSelector(response)
        votes = xxs.select('//meeting/vote')
        items = []

        for vote in votes:
            item = LegcoVote()
            item["number"] = vote.select('@number').extract()
            item["date"] = vote.select('vote-date/text()').extract()
            item["time"] = vote.select('vote-time/text()').extract()
            item["motion_ch"] = vote.select('motion-ch/text()').extract()
            item["motion_en"] = vote.select('motion-en/text()').extract()
            item["mover_ch"] = vote.select('mover-ch/text()').extract()
            item["mover_en"] = vote.select('mover-en/text()').extract()
            item["type"] = vote.select('mover-type/text()').extract()
            item["separate_mechanism"] = vote.select('vote-separate-mechanism/text()').extract()
            items.append(item)

            #item["member_vote"] = xxs.select('//individual-votes/member/vote/text()').extract()[0]

        return items