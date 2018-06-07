from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from s_weibo.spiders.weibo import WeiboUserSpider

if __name__ == '__main__':
    query = '1076032416080157'  # 美赞臣中国的containerid
    settings = get_project_settings()
    settings.update({'JSON_FILE_PATH':
                         '/Users/youyang/PycharmProjects/Weibo_Processing/raw_data/users/results-Meizanchen.json'})
    process = CrawlerProcess(settings)
    process.crawl(WeiboUserSpider, query=query)
    process.start()
