from scrapy import Item
from scrapy import Field


class WeiboItem(Item):
    idstr = Field()
    mblog = Field()
