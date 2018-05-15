# coding=utf-8

# 抓取武汉二手房房价信息 2018.5.12

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):

        self.urls = url_manager.UrlManager()  # 管理URL
        self.downloader = html_downloader.HtmlDownloader()  # 下载URL内容
        self.parser = html_parser.HtmlParser()  # 解析URL内容
        self.outputer = html_outputer.HtmlOutputer()  # 输出获取到的内容

    # 获取待爬取城市链接
    def CityUrl_Crwa(self, root_url):
        html_cont = self.downloader.download(root_url)
        cityurls_list = self.parser.cityurlparser(html_cont)
        return cityurls_list

    # 爬虫主体程序
    def crwa(self, city_url):
        count = 0
        self.urls.add_new_url(city_url)  # 将根链接首先放入page页urllist
        while self.urls.has_new_url():
            count = count + 1
            try:
                new_url = self.urls.get_new_url()  # 获取新的链接
                html_cont = self.downloader.download(new_url)  # 下载页面内容
                new_urls, new_data, house_city = self.parser.parse(new_url, html_cont)  # 解析页面内容
                self.urls.add_new_urls(new_urls)
                self.outputer.output_excel(new_data, house_city)  # 写入excel
                # self.outputer.output_mysql(new_data,house_city)#写入mysql
                print('第', count, '个网页【', new_url, '】输出成功--------------')
                # if count > 1:  # 测试时只抓取部分数据
                #     break
            except Exception as e:
                print(Exception, e)
                self.urls.add_false_url(new_url)  # 如果解析失败，则将url放入失败列表
                print("第",count,"个网页【",new_url,"】爬取失败，将会被重新爬取,失败次数过多将会被舍弃-------------")
                count = count - 1
                self.urls.release_urllist()  # 解析并输出完一个城市后，释放page页urllist

if __name__=="__main__":
    obj_spider = SpiderMain()
    # root_url = "http://newhouse.wuhan.fang.com/house/s/b81-b91/"
    root_url = "http://esf.wuhan.fang.com/house-a0652-b014312/"  # 武汉藏龙岛二手房

    city_urls = obj_spider.CityUrl_Crwa(root_url)
    print(city_urls)

    # for city_url in city_urls:
    #    obj_spider.crwa(city_url)
    obj_spider.crwa(root_url)  # 只爬武汉藏龙岛二手房信息
