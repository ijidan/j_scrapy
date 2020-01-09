# -*- coding:utf-8 -*-

import time
import json
import logging
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree


class GetProxyHandler(object):
    def __init__(self, domain, proxy, logging):
        self.s = requests.session()
        # 设置连接活跃状态为False
        self.s.keep_alive = False
        # 模拟浏览器头信息
        self.headers = {"User-Agent": UserAgent().random}
        # 访问地址及登录信息
        self.domain = domain
        self.logging = logging
        self.proxy = proxy
        https_ips = self.proxy["https"]
        http_ips = self.proxy["http"]
        self.proxies = {"https": str(random.choice(https_ips)), "http": str(random.choice(http_ips))}
        # 需要得到的值
        self.proxy_new = {"http": [], "https": []}

    def __del__(self):
        return

    def getlist(self, page):
        try:
            try:
                params = {
                    "cookies": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTliM2MzNTJjMTdhODFjMjM4NDJjYmU2YzMwYjg2MjJlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUFwV01xRGErZUpxeTJQOE9Nd01TZXlJTGJsdHdpY2twUWJZSHljQ2g4aFE9BjsARg%3D%3D--bfd24031a5fcd05799f86bf29f22d127d7ad6d2c; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1576576835,1576577338,1576577347,1577785731; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1577785755"}
                # 请求路径，西刺代理网站
                url = 'http://www.xicidaili.com/'
                # 请求响应头
                headers = {
                    'User-Agent': UserAgent().random}
                # 通过requests的get方法访问目标网站，获得响应对象
                response = self.s.get(url, headers=self.headers, proxy=self.proxies, verify=False, allow_redirects=True,
                                      timeout=5)
                if response.status_code == 200:
                    self.logging.info("请求接口成功 %s (有效IP %s)......" % (str(page), str(self.proxies)))
                    soup = BeautifulSoup(response.text, 'html.parser')
                    table = soup.table
                    all_tr = table.find_all("tr")
                    for tr in all_tr:
                        all_td = tr.find_all("td")
                        try:
                            ip = all_td[1].text.strip()
                            port = all_td[2].text.strip()
                            head = all_td[5].text.strip()
                            if head == "HTTP":
                                self.proxy_new["http"].append(ip + ":" + port)
                            if head == "HTTPS":
                                self.proxy_new["https"].append(ip + ":" + port)
                        except Exception as e:
                            pass
                    with open("proxy.json", "w") as fl:
                        json.dump(self.proxy_new, fl)
                else:
                    self.logging.error("请求接口错误 : %s" % str(response.status_code))
            except Exception as e:
                if len(self.proxy["http"]) == 0 or len(self.proxy["https"]) == 0:
                    return
                self.logging.warn("尝试重新获取代理IP ...")
                self.proxy["http"].remove(self.proxies["http"])
                self.proxy["https"].remove(self.proxies["https"])
                https_ips = self.proxy["https"]
                http_ips = self.proxy["http"]
                self.proxies = {"https": str(random.choice(https_ips)), "http": str(random.choice(http_ips))}
                self.getlist(page)
        except Exception as e:
            self.logging.error("请求失败 : %s" % e)
        return


if __name__ == "__main__":
    # 定义日志
    curdate = time.strftime("%Y%m%d")
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='proxyip-%s.log' % (curdate), level=logging.DEBUG, format=LOG_FORMAT)
    # 实例化对象
    with open("proxy.json", "r") as fl:
        proxy = json.load(fl)
    if proxy:
        obj = GetProxyHandler("https://www.xicidaili.com/nn/", proxy, logging)
        for page in range(1, 6):
            proxy = obj.getlist(page)
