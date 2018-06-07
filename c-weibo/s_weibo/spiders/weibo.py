import ujson
from scrapy import Spider
from scrapy.http import FormRequest
from ..items import WeiboItem


def gen_comments(data):
    for comment in data:
        yield comment


class WeiboCommentSpider(Spider):
    name = 'weibocommentspider'
    allowed_domains = ['m.weibo.cn']

    def __init__(self, *, query, upper_bound=100):
        super(WeiboCommentSpider).__init__()
        self.api = 'https://m.weibo.cn/api/comments/show'
        self.id = '{}'.format(query)
        self.upper_bound = upper_bound

    def start_requests(self):
        yield from (FormRequest(
            method='GET',
            url=self.api,
            formdata={'id': self.id, 'page': str(i)},
            meta={'page': i},
            callback=self.parse)
            for i in range(1, self.upper_bound+1))

    def parse(self, response):
        result = ujson.loads(response.text)
        data = result.get('data', {}).get('data')
        if data:
            current_page = response.meta['page']
            if current_page >= self.upper_bound:
                page = current_page + 1
                yield FormRequest(
                    method='GET',
                    url=self.api,
                    formdata={'id': self.id,
                              'page': str(page)},
                    meta={'page': page},
                    callback=self.parse)

            comments = gen_comments(data)
            yield from (WeiboItem(idstr=comment.get('id'), comment=comment)
                        for comment in comments)
