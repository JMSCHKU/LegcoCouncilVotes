# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LegcoVote(Item):
    number = Field()
    date = Field()
    time = Field()
    motion_ch = Field()
    motion_en = Field()
    mover_ch = Field()
    mover_en = Field()
    type = Field()
    separate_mechanism = Field()
