# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.exporter import CsvItemExporter

import json


def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # TeamItem => team


class JsonVotePipeline(object):
    def __init__(self):
        self.votefile = open('data/json/votes.json', 'wb')
        self.individualvotefile = open('data/json/individualvotes.json', 'wb')

    def process_item(self, item, spider):
        if (type(item).__name__ == 'VoteItem'):
            line = json.dumps(dict(item)) + "\n"
            self.votefile.write(line)
            return item

        if (type(item).__name__ == 'IndividualVoteItem'):
            line = json.dumps(dict(item)) + "\n"
            self.individualvotefile.write(line)
            return item

        return item


class MultiCSVItemPipeline(object):
    SaveTypes = ['vote','individualvote']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.files = dict([ (name, open('data/csv/'+name+'.csv','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvItemExporter(self.files[name],delimiter = '\t')) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
    	what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item