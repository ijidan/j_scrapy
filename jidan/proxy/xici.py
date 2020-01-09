# -*- coding:utf-8 -*-

import os
import json
import logging
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# 西刺代理
class XiCi(object):

    # 构造函数
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_name = current_dir + os.sep + "proxy.json"
        self.proxy_new = {"http": [], "https": []}

    # 写文件
    def write_proxy(self):
        with open(self.file_name, "w") as fl:
            json.dump(self.proxy_new, fl)

    # 读文件
    def get_proxy(self):
        try:
            with open(self.file_name, "r") as fl:
                proxy = json.load(fl)
                return proxy
        except Exception as e:
            return None

    # 获取代理
    def get_proxies(self):
        proxy = self.get_proxy()
        if proxy is not None:
            https_ips = proxy["https"]
            http_ips = proxy["http"]
            proxies = {"https": str(random.choice(https_ips)), "http": str(random.choice(http_ips))}
            return proxies
        else:
            return None

    # 构造代理
    def build_proxies(self, type=""):
        proxies = self.get_proxies()
        if type in ("http", "https"):
            return proxies[type]
        else:
            return proxies

    # 获取一个有效的代理
    def get_one_valid_proxy(self, count=10, type="http"):
        valid_proxy = None
        for idx in range(1, count):
            proxy = self.build_proxies(type)
            is_valid = self.check_proxy(type, proxy)
            if is_valid is True:
                valid_proxy = proxy
                break
        return valid_proxy

    # 检测代理
    def check_proxy(self, type, proxy):
        # 抓取代理
        headers = self.get_headers()
        url = "http://www.baidu.com"
        proxies = {
            type: proxy,
        }
        try:
            r = requests.get(url, headers=headers, proxies=proxies)
            print "$$$$$$$$$$$$$$$$$$$$$$"+ r.status_code
            return r.status_code != 200
        except Exception as e:
            print e
            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            return False

    # 获取随机header
    def get_headers(self):
        headers = {'user-agent': UserAgent().random}
        return headers

    # 抓取代理
    def get_proxy_new(self, url):
        headers = self.get_headers()
        proxies = self.get_proxies()
        proxies = None
        s = requests.Session()
        try:
            if proxies is None:
                r = s.get(url, headers=headers)
            else:
                r = s.get(url, headers=headers, proxies=proxies)
            if r.status_code != requests.codes.ok:
                logging.error("请求错误：状态码为%s" % r.status_code)
            else:
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                table = soup.table
                all_tr = table.find_all("tr")
                for tr in all_tr:
                    all_td = tr.find_all("td")
                    try:
                        ip = all_td[1].text.strip()
                        port = all_td[2].text.strip()
                        head = all_td[5].text.strip()
                        if head == "HTTP":
                            self.proxy_new["http"].append("http://" + ip + ":" + port)
                        if head == "HTTPS":
                            self.proxy_new["https"].append("https://" + ip + ":" + port)
                    except Exception as e:
                        pass
                return self.proxy_new
        except Exception as e:
            pass

    # 爬取代理
    def get_proxy_list(self):
        url = "https://www.xicidaili.com/nn/"
        for page in range(1, 6):
            link = url + str(page)
            self.get_proxy_new(link)
            self.write_proxy()


if __name__ == "__main__":
    xici = XiCi()
    xici.get_proxy_list()
