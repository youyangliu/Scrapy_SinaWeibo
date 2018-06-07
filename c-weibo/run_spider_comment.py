from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from s_weibo.spiders.weibo import WeiboCommentSpider

if __name__ == '__main__':
    query = '4240245207283641'  # 微博的id
    settings = get_project_settings()
    settings.update({'JSON_FILE_PATH':
                         '/Users/youyang/PycharmProjects/Weibo_Processing/raw_data/comments/comments.json'})
    process = CrawlerProcess(settings)
    process.crawl(WeiboCommentSpider, query=query)
    process.start()
