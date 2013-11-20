# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class VoteItem(Item):
    vote_number = Field()
    date = Field()
    time = Field()
    motion_ch = Field()
    motion_en = Field()
    mover_ch = Field()
    mover_en = Field()
    type = Field()
    separate_mechanism = Field()
    result = Field()
    functional_present = Field()
    functional_vote = Field()
    functional_yes = Field()
    functional_no = Field()
    functional_abstain = Field()
    functional_result = Field()
    geographical_present = Field()
    geographical_vote = Field()
    geographical_yes = Field()
    geographical_no = Field()
    geographical_abstain = Field()
    geographical_result = Field()



class IndividualVoteItem(Item):
    vote_number = Field()
    date = Field()
    name_ch = Field()
    name_en = Field()
    constituency = Field()
    vote = Field()


class VoteXMLFileItem(Item):
    url = Field()