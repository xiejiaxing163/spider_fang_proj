#coding=utf8
__author__ = 'zyx'
# import urlparse
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import re

class HtmlParser(object):

    def cityurlparser(self, html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf8')
        city_urls = set()
        linklist = soup.find('div', class_="city20141104").find_all('a', href=True)
        [city_urls.add(city_url["href"]+"b81-b91/") for city_url in linklist]  # 只搜索武汉
        return city_urls

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf8')
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        city = self._get_city(soup)
        return new_urls, new_data, city

    # 获取分页链接
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # print(soup.find('div', class_="wid1000"))
        # links = soup.find('div', class_="page").find_all('a', href=re.compile(r"/house/s/b81-\w+"))
        # 获取下一页
        links = soup.find('div', class_="wid1000").find_all('a', href=re.compile(r"/house-a0652-b014312/i\w+"))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    # 获取页面内容
    def _get_new_data(self, page_url, soup):
        res_data = []
        # nodes = soup.find_all('div', class_="nlc_details")
        nodes = soup.find_all('dd', class_="info rel floatr")
        for node in nodes:
            house_data = {}
            # house_name = node.find('div', class_="nlcd_name").get_text()
            # house_name = node.find('p', class_="title").get_text()
            try:
                house_name = node.p.a.contents[0]
                # house_data['house_name'] = ''.join(house_name.split())
                house_data['house_name'] = house_name
            except Exception as e:
                print(Exception, e)
                continue
            # house_tag = node.find('div', class_="nlcd_name").find('a', href=True).get("href")

            try:  # 户型 hose_type
                hose_type = node.find('p', class_="mt12").get_text()
                house_data['hose_type'] = ''.join(hose_type.split())
            except Exception as e:
                print(Exception, e)
                house_data['hose_type'] = ""

            try:  # 面积 hose_area
                hose_area = node.find('div', class_="area alignR").p.text
                house_data['hose_area'] = ''.join(hose_area.split())
            except Exception as e:
                print(Exception, e)
                house_data['hose_type'] = ""

            try:  # 价格 总价 house_price1
                house_price1 = node.find('div', class_="moreInfo").find('span','price').text + '万'
                house_data['house_price1'] = ''.join(house_price1.split())
            except Exception as e:
                print(Exception, e)
                house_data['house_price1'] = ""

            try:  # 价格 单价 house_price2
                house_price2 = node.find('p', class_="danjia alignR mt5").text
                house_data['house_price2'] = ''.join(house_price2.split())
            except Exception as e:
                print(Exception, e)
                house_data['house_price2'] = ""

            try:  # 小区地址 house_address
                # house_address = node.find('div', class_="address").get_text()
                house_address = node.find('span', class_="iconAdress ml10 gray9").attrs['title']
                house_data['house_address'] = house_address
            except Exception as e:
                print(Exception, e)
                house_data['house_address'] = ""

            try:  # 详情链接 house_tag
                house_tag = node.find('p', class_="title").find('a', href=True).get("href")
                house_full_url = urllib.parse.urljoin(page_url, house_tag)
                house_data['house_tag'] = house_full_url
            except Exception as e:
                print(Exception, e)
                house_data['house_tag'] = ""
            res_data.append(house_data)
        # print(res_data)
        return res_data

    def _get_city(self, soup):
        house_city = soup.find('div', class_="s4Box").get_text()
        return house_city
