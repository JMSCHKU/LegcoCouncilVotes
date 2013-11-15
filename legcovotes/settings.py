# Scrapy settings for legcovotes project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'legcovotes'

SPIDER_MODULES = ['legcovotes.spiders']
NEWSPIDER_MODULE = 'legcovotes.spiders'

ITEM_PIPELINES = {
    'legcovotes.pipelines.MultiCSVItemPipeline': 300,
}

#FEED_URI = 'legcovote_unicode.csv'
#FEED_FORMAT = 'csv'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'legcovotes (+http://www.yourdomain.com)'
