# coding=utf-8
__author__ = 'zyx'
import requests


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        # html = requests.get(url)
        rsp = requests.get(url)
        rsp.encoding = "gb18030"
        # html = html.text.encode(html.encoding).decode("gbk").encode("utf8")
        # html = html.text.encode(html.encoding).decode("gbk").encode("gb2312")
        # rsp.encoding = 'utf8'

        return rsp.text
        # if rsp.encoding == 'ISO-8859-1':
        #     encodings = requests.utils.get_encodings_from_content(rsp.text)
        #     if encodings:
        #         encoding = encodings[0]
        #     else:
        #         encoding = rsp.apparent_encoding
        #
        #     # encode_content = rsp.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        # encode_content = rsp.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        # return encode_content
