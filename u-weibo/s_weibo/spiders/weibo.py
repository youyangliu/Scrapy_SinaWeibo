import ujson
from scrapy import Spider
from scrapy.http import FormRequest
from ..items import WeiboItem


def gen_mblog(cards):
    for card in cards:
        mblog = card.get('mblog')
        if mblog:
            mblog.pop('user')
            yield mblog


class WeiboUserSpider(Spider):
    name = 'weibouserspider'
    allowed_domains = ['m.weibo.cn']

    def __init__(self, *, query, upper_bound=100):
        super(WeiboUserSpider).__init__()
        self.api = 'https://m.weibo.cn/api/container/getIndex'
        self.containerid = '{}'.format(query)
        self.upper_bound = upper_bound

    def start_requests(self):
        yield from (FormRequest(
            method='GET',
            url=self.api,
            formdata={'containerid': self.containerid, 'page': str(i)},
            meta={'page': i},
            callback=self.parse)
            for i in range(1, self.upper_bound+1))

    def parse(self, response):
        result = ujson.loads(response.text)
        cards = result.get('data', {}).get('cards')
        if cards:
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.api,
                    formdata={'containerid': self.containerid,
                              'page': str(page)},
                    meta={'page': page},
                    callback=self.parse)

            mblogs = gen_mblog(cards)
            yield from (WeiboItem(idstr=mblog.get('idstr'), mblog=mblog)
                        for mblog in mblogs)
