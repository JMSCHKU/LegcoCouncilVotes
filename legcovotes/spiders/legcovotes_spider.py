from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


from scrapy import log
import time

from scrapy.http import Request
import urlparse

from legcovotes.items import VoteItem
from legcovotes.items import IndividualVoteItem
from legcovotes.items import VoteXMLFileItem




class LegcoVotesXMLFileSpider(CrawlSpider):
    name = "legcovotes"
    allowed_domains = ["www.legco.gov.hk"]
    start_urls = []
    #    "http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm"
    #]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []

        #dispatcher.connect(self.spider_opened, signals.spider_opened)
        #dispatcher.connect(self.spider_closed, signals.spider_closed)

        xmlfiles = self.get_xml_files()
        
        for xmlfile in xmlfiles:
            self.start_urls.append(xmlfile)

        
    def __del__(self):
        print self.verificationErrors

    #def spider_opened(self, spider):

    #def spider_closed(self, spider):

    def parse(self, response):
        xxs = Selector(response)
        votes = xxs.xpath('/legcohk-vote/meeting/vote')
        items = []

        for vote in votes:
            councilvote = VoteItem()
            councilvote["vote_number"] = vote.xpath('@number').extract()
            councilvote["date"] = vote.xpath('vote-date/text()').extract()
            councilvote["time"] = vote.xpath('vote-time/text()').extract()
            councilvote["motion_ch"] = vote.xpath('motion-ch/text()').extract()
            councilvote["motion_en"] = vote.xpath('motion-en/text()').extract()
            councilvote["mover_ch"] = vote.xpath('mover-ch/text()').extract()
            councilvote["mover_en"] = vote.xpath('mover-en/text()').extract()
            councilvote["type"] = vote.xpath('mover-type/text()').extract()
            councilvote["separate_mechanism"] = vote.xpath('vote-separate-mechanism/text()').extract()

            items.append(councilvote)


            members = vote.xpath('individual-votes/member')
            for member in members:
                individualvote = IndividualVoteItem()
                individualvote['vote_number'] = councilvote["vote_number"]
                individualvote['date'] = councilvote["date"]
                individualvote['name_ch'] = member.xpath('@name-ch').extract()
                individualvote['name_en'] = member.xpath('@name-en').extract()
                individualvote['constituency'] = member.xpath('@constituency').extract()
                individualvote['vote'] = member.xpath('vote/text()').extract()

                items.append(individualvote)

        return items

    """ Build list of XML files - requires selenium """
    def get_xml_files(self):
        import os.path

        xmlfilestxt = 'votexmlfiles.txt'

        if not ( os.path.isfile(xmlfilestxt) ): # & os.path.getsize(xmlfilestxt) == 0 ):
            from selenium import webdriver

            browser = webdriver.Firefox()
            browser.get('http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm')

            #Wait for javscript to load in Selenium
            time.sleep(2.5)

            xmlfiles = browser.find_elements_by_link_text('(XML)')

            f = open(xmlfilestxt, 'w')
            for xmlfile in xmlfiles:
                url=urlparse.urljoin("http://www.legco.gov.hk/", xmlfile.get_attribute('href'))
                f.write(url + "\n")
            f.close()
            browser.close()

            return xmlfiles
        else:
            with open(xmlfilestxt, 'r') as f:
                xmlfiles = [line.strip() for line in f]
            return xmlfiles

