from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from s_weibo.spiders.weibo import WeiboUserSpider

if __name__ == '__main__':
    query = '1076031004853823'  # 奶粉揭秘的containerid
    settings = get_project_settings()
    settings.update({'JSON_FILE_PATH':
                         '/Users/youyang/PycharmProjects/Weibo_Processing/raw_data/users/results-naifenjiemi.json'})
    process = CrawlerProcess(settings)
    process.crawl(WeiboUserSpider, query=query)
    process.start()
