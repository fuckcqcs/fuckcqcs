# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: f_cccs_scraper.py
 Time: 7/24/18
"""
import logging
import sys
import os
import requests
import time
import lxml
from lxml import html
from cpca import *

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)


def cookies_string_to_dict(cookies_string):
    """
    Transform cookies which is type of string  to the type of dict
    """
    if not cookies_string or cookies_string == '':
        raise ValueError("Invalid blank param of cookies_string !")
    if not isinstance(cookies_string, str):
        raise TypeError("Invalid type of cookies_string !")
    cookies_dict = {}
    for single_mapping_item in cookies_string.split(";"):
        single_mapping_item = single_mapping_item.strip().replace("\t", "").replace("\n", "")
        if '=' not in single_mapping_item:
            continue
        kv_list = single_mapping_item.split('=')
        if len(kv_list) == 0:
            continue
        cookies_dict[kv_list[0]] = kv_list[1]
    return cookies_dict


# 天眼查cookies
global_cookies = """
aliyungf_tc=AQAAAKSZCyj/Pw4Aa9oKcG3TzFVEf18+; csrfToken=D7y9XKBbqKIV_Fa2Di5UKrlh; TYCID=f6de07308ede11e8a54aebc536b5d095; undefined=f6de07308ede11e8a54aebc536b5d095; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1532365213,1532365772,1532394893; _ga=GA1.2.1376886145.1532394894; _gid=GA1.2.1664725936.1532394894; ssuid=8800051336; token=5f8463c57cd64ebfb45fbe56475b6901; _utm=939c54f5cbaf4bd7acc821d1915ded0a; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUxNTEwNTU3MiIsImlhdCI6MTUzMjM5NDk0NCwiZXhwIjoxNTQ3OTQ2OTQ0fQ.efDRyIQPrXyDVRMdrCUAug3lofayBfvZAYjXHLSxdSfNbpqVPX7eOmHT1NI53VOab7-Pn8EsDSIA9fveoC3U3w%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213515105572%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUxNTEwNTU3MiIsImlhdCI6MTUzMjM5NDk0NCwiZXhwIjoxNTQ3OTQ2OTQ0fQ.efDRyIQPrXyDVRMdrCUAug3lofayBfvZAYjXHLSxdSfNbpqVPX7eOmHT1NI53VOab7-Pn8EsDSIA9fveoC3U3w; Hm_lpvt_e92c8d65d92d534b0f
"""
global_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Host": "www.tianyancha.com",
    "DNT": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1"
}


def fetch_remote_html(page: int = 1):
    uri = 'https://www.tianyancha.com/pagination/bid.xhtml?ps=30&pn=%s&id=2322751222' % page
    try:
        r = requests.get(url=uri, headers=global_headers, cookies=cookies_string_to_dict(global_cookies))
        time.sleep(6)
        return {'status_code':r.status_code,'text':''} if r.status_code != 200 or '访问禁止' in r.text else {'status_code':r.status_code,'text':r.text}
    except Exception as ex:
        return {'status_code':500,'text':''}


def fetch_remote_raw_link(uri_from: str)->str:
    try:
        time.sleep(6)
        r = requests.get(url=uri_from, headers=global_headers, cookies=cookies_string_to_dict(global_cookies))
        _h = lxml.html.fromstring(r.text)
        raw_link = ''.join(_h.xpath("//div[@class='f12 common-remark-style pb30 new-border-bottom']/a/@href"))
        return raw_link
    except Exception as ex:
        return ""


def read_html_file(file_path: str) -> str:
    """read cache file from html"""
    with open(file_path, 'r+', encoding='utf-8') as fuck:
        return fuck.read()


def parser_data(html_data: str) -> list:
    """ parser construct data from html"""
    if html_data is None or html_data == '':
        return []

    _f_box = []
    _h = lxml.html.fromstring(html=html_data)
    _x_list = _h.xpath("//tbody/tr/td")
    for i in range(0, len(_x_list), 4):
        publish_time = _x_list[i + 1].text
        title = ''.join(_x_list[i + 2].xpath(".//a/text()"))
        title_link = ''.join(_x_list[i + 2].xpath(".//a/@href"))
        raw_link = fetch_remote_raw_link(title_link)
        location = _x_list[i + 3].text
        # fetch detail location
        df = transform([location]) if '-' not in location else transform([title])
        province = df.ix[[0]].values[0][0]
        city = df.ix[[0]].values[0][1]
        county = df.ix[[0]].values[0][2]
        _f_box.append(
            {'province': province, 'city': city, 'county': county, 'publish_time': publish_time, 'title': title,
             'title_link': title_link, 'raw_link': raw_link, 'location': location})
    return _f_box


def main():
    tmp_counter = 1
    while True:
        code_mapping_text = fetch_remote_html(tmp_counter)
        code = code_mapping_text.get("status_code")
        html_text = code_mapping_text.get('text')
        # 正常返回且返回结果为空，表示已经到达最大页数
        if code == 200 and html_text =='':
            break
        # 实际上一共只有5页
        if tmp_counter >5:
            break
        html_text = read_html_file('bid' + str(tmp_counter) + '.htm') if html_text == '' else html_text
        fuck_box = parser_data(html_text)

        tmp_counter+=1

if __name__ == '__main__':
    main()