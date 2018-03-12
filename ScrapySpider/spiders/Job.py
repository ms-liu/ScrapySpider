# -*- coding: utf-8 -*-
import pickle

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver

from item_loaders import FirstItemLoader
from items import JobItem
import time


class JobSpider(CrawlSpider):
    name = 'Job'
    allowed_domains = ['www.lagou.com']
    # start_urls = ['http://www.lagou.com/']
    start_urls = ['https://www.lagou.com/']
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    }
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        "JOBDIR": "runtime/record/job",
        'DEFAULT_REQUEST_HEADERS': header
    }

    rules = (
        # https: // www.lagou.com / zhaopin / Java /?labelWords = label
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        # https: // www.lagou.com / gongsi / 236450.html
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        # https: // www.lagou.com / jobs / 3411257. html
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def start_requests(self):
        """
        进行知乎的登录操作并缓存cookies
        :return:
        """
        local_cookies = {}
        try:
            file = open('E:\PythonWorkSpace\JobboleSpider\JobboleSpider\JobboleSpider\cookies\logou_cookies', 'rb')
            local_cookies = pickle.load(file)
            file.close()
        except Exception as e:
            pass

        if not local_cookies:
            chrome = webdriver.Chrome(executable_path='D:/Selenium/driver/chromedriver.exe')
            chrome.get("https://www.lagou.com")
            # print(chrome.get_cookies())
            # print("==========================")
            pwd_btn = chrome.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a')
            # print(xpath)
            pwd_btn.click()
            pwd_btn = chrome.find_element_by_xpath('//*[@id="lg_tbar"]/div/ul/li[1]/a')
            # print(xpath)
            pwd_btn.click()
            user_input = chrome.find_element_by_xpath(
                '//html/body/section/div[1]/div[2]/form/div[1]/input')
            pwd_input = chrome.find_element_by_xpath(
                '//html/body/section/div[1]/div[2]/form/div[2]/input')
            user_input.send_keys('18818227284')
            pwd_input.send_keys('qq275846421')
            #
            login_btn = chrome.find_element_by_xpath('/html/body/section/div[1]/div[2]/form/div[5]/input')
            login_btn.click()
            time.sleep(5)
            cookies = chrome.get_cookies()
            # print(cookies)
            for cookie in cookies:
                file_cookie = open("E:\PythonWorkSpace\JobboleSpider\JobboleSpider\JobboleSpider\cookies\logou_cookies",
                                   'wb')
                local_cookies[cookie['name']] = cookie['value']
                pickle.dump(local_cookies, file_cookie)
                file_cookie.close()
            chrome.close()
        return [scrapy.Request(self.start_urls[0], headers=self.header, dont_filter=True,
                               cookies=local_cookies)]

    def parse_job(self, response):
        item_loader = FirstItemLoader(item=JobItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_id", response.url)
        item_loader.add_xpath("title", "//*[@class='job-name']/span/text()")
        item_loader.add_xpath("salary_min", "//*[@class='job_request']//span[@class='salary']/text()")
        item_loader.add_xpath("salary_max", "//*[@class='job_request']//span[@class='salary']/text()")
        item_loader.add_xpath("exp_min", "//*[@class='job_request']//span[3]/text()")
        item_loader.add_xpath("exp_max", "//*[@class='job_request']//span[3]/text()")
        item_loader.add_xpath("degree", "//*[@class='job_request']//span[4]/text()")
        item_loader.add_xpath("type", "//*[@class='job_request']//span[5]/text()")
        item_loader.add_xpath("date", "//*[@class='publish_time']/text()")
        item_loader.add_xpath("tags", "//*[contains(@class,'position-label')]//li/text()")
        item_loader.add_xpath("advantages", "//*[@class='job-advantage']/p/text()")
        item_loader.add_xpath("desc", "//*[@class='job_bt']//p//text()")
        item_loader.add_xpath("location", "//*[@class='work_addr']//a/text()")
        item_loader.add_xpath("company_url", "//*[@class='job_company']/dd//a/@href")
        item_loader.add_xpath("company_name", "//*[@class='job_company']//h2/text()")
        item_loader.add_value("crawl_time", int(time.time()))
        item = item_loader.load_item()
        return item
