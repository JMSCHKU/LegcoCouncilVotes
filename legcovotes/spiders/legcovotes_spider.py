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

from legcovotes.items import VoteItem
from legcovotes.items import IndividualVoteItem


class LegcoVotesSpider(CrawlSpider):
    name = "legcovotes"
    allowed_domains = ["www.legco.gov.hk"]
    start_urls = [
        "http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm"
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []

        #dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.browser = webdriver.Firefox()
        self.browser.get('http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm')
        
    def __del__(self):
        print self.verificationErrors
        CrawlSpider.__del__(self)

    #def spider_opened(self, spider):

    def spider_closed(self, spider):
        self.browser.close()

    def parse(self, response):
        sel = self.browser

        #Wait for javscript to load in Selenium
        time.sleep(2.5)

        links = sel.find_elements_by_link_text('(XML)')
        
        # restrict to one XML file for developing purposes
        #links = [links[0]]

        for link in links:
            url=urlparse.urljoin("http://www.legco.gov.hk/", link.get_attribute('href'))
            yield Request(url, callback=self.parse_xml_document)    

    def parse_xml_document(self, response):
        xxs = XmlXPathSelector(response)
        votes = xxs.select('//meeting/vote')
        items = []

        for vote in votes:
            councilvote = VoteItem()
            councilvote["number"] = vote.select('@number').extract()
            councilvote["date"] = vote.select('vote-date/text()').extract()
            councilvote["time"] = vote.select('vote-time/text()').extract()
            councilvote["motion_ch"] = vote.select('motion-ch/text()').extract()
            councilvote["motion_en"] = vote.select('motion-en/text()').extract()
            councilvote["mover_ch"] = vote.select('mover-ch/text()').extract()
            councilvote["mover_en"] = vote.select('mover-en/text()').extract()
            councilvote["type"] = vote.select('mover-type/text()').extract()
            councilvote["separate_mechanism"] = vote.select('vote-separate-mechanism/text()').extract()

            items.append(councilvote)


            members = xxs.select('//individual-votes/member')
            for member in members:
                individualvote = IndividualVoteItem()
                individualvote['number'] = councilvote["number"]
                individualvote['date'] = councilvote["date"]
                individualvote['name_ch'] = member.select('@name-ch').extract()
                individualvote['name_en'] = member.select('@name-en').extract()
                individualvote['constituency'] = member.select('@constituency').extract()
                individualvote['vote'] = member.select('vote/text()').extract()

                items.append(individualvote)


        return items