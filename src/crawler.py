# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 23 Nov 2024 Sat 00:45
# Name: crawler
# Author: CHAU SHING SHING HAMISH

import json
import math
from datetime import datetime
from urllib import request, parse
from bs4 import BeautifulSoup

class Spider:
    def __init__(self):
        self.page_url_root = 'https://flk.npc.gov.cn/'
        self.api_url_root = 'https://flk.npc.gov.cn/api/?'
        self.params = {
            'type': '',
            'xlwj': '',
            'zdjg': '',
            'fgxlwj': '',
            'fgbt': '', # 搜索关键字，
            'searchType': 'title;vague',
            # 分类树：关键字;排序方法 有些时候失效，暂不处理
            #   关键字：
            #   - f_tgjgmc_s：制定机关 f_xldj_s：法律性质 f_dqzt_s：时效性 f_bbrq_s：公布日期
            #   排序方法：
            #   - asc：升序 desc：降序
            # 保留为后期可能的扩展
            'sortTr' : 'f_bbrq_s;desc',
            'gbrqStart': '', # 公布日期开始，格式：yyyy-MM-dd
            'gbrqEnd': '', # 公布日期结束，格式：yyyy-MM-dd
            'sxrqStart': '', # 施行日期开始，格式：yyyy-MM-dd
            'sxrqEnd': '', # 施行日期结束，格式：yyyy-MM-dd
            'sort': '', # 是否排序。type存在时，必须存在
            'page': 1, # 页码
            'size': 10, # 每页条数，固定值
            '_': '' # 时间戳
        }
        self.data = []
        self.seq = 0
        self.pages = 1

    def set_param(self, key, value):
        if key in self.params:
            self.params[key] = value
        else:
            raise KeyError(f'Invalid key: {key}')

    def build_url(self):
        # & to url form
        self.params['zdjg'] = parse.quote(self.params['zdjg']) if self.params['zdjg'] and '&' in self.params['zdjg'] \
            else self.params['zdjg']
        # ; to url form
        self.params['searchType'] = parse.quote(self.params['searchType']) if ';' in self.params['searchType'] \
            else self.params['searchType']
        self.params['sortTr'] = parse.quote(self.params['sortTr']) if ';' in self.params['sortTr'] \
            else self.params['sortTr']
        # build url for request
        url = self.api_url_root + '&'.join([f'{k}={v}' for k, v in self.params.items()])

        # every xlwj, fgxlwj, and zdjg in request should be a single key-value pair
        # and if not set, remove them from url
        if len(self.params['xlwj'].split(',')) > 1:
            new_xlwj = ''
            for i in range(len(self.params['xlwj'].split(','))):
                new_xlwj += '&xlwj=' + self.params['xlwj'].split(',')[i]
            url = url.replace(f'&xlwj={self.params["xlwj"]}', new_xlwj)
        elif not self.params['xlwj']:
            url = url.replace('&xlwj=', '')

        if len(self.params['fgxlwj'].split(',')) > 1:
            new_fgxlwj = ''
            for i in range(len(self.params['fgxlwj'].split(','))):
                new_fgxlwj += '&fgxlwj=' + self.params['fgxlwj'].split(',')[i]
            url = url.replace(f'&fgxlwj={self.params["fgxlwj"]}', new_fgxlwj)
        elif not self.params['fgxlwj']:
            url = url.replace('&fgxlwj=', '')

        if len(self.params['zdjg'].split(',')) > 1:
            new_zdjg = ''
            for i in range(len(self.params['zdjg'].split(','))):
                new_zdjg += '&zdjg=' + self.params['zdjg'].split(',')[i]
            url = url.replace(f'&zdjg={self.params["zdjg"]}', new_zdjg)
        elif not self.params['zdjg']:
            url = url.replace('&zdjg=', '')

        if not self.params['type']:
            url = url.replace('&sort=', '')
        else:
            # type must be followed by sort, as users can't and not necessary to set sort manually, set them to true
            url = url.replace('&sort=', '&sort=true')

        if not self.params['fgbt']:
            url = url.replace('&fgbt=', '')

        url += str(int(datetime.now().timestamp() * 1000))
        return url

    def fetch(self):
        url = self.build_url()
        print(f'获取法律列表：{url}')
        r = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64'})
        fetch_retry_time = 0
        try:
            with request.urlopen(r, timeout=10) as page:
                url_soup = BeautifulSoup(page, 'lxml')
        except TimeoutError:
            print('获取法律列表超时，重试')
            if fetch_retry_time < 3:
                fetch_retry_time += 1
                self.fetch()
            else:
                return False
        # locate the data of laws on each page
        law_info = json.loads(url_soup.find('p').contents[0].text)
        self.data = law_info['result']['data']
        # get total pages
        self.pages = math.ceil(law_info['result']['totalSizes'] / 10)
        self.seq = 0
        print(f'共{self.pages}页法律，正下载第{self.params["page"]}页')
        return True

    def next(self):
        # a json response include 10 laws in a page, use this to iterate through all laws
        # when no further law is available, return None, and search.search() will stop
        try:
            law = self.data[self.seq]
            self.seq += 1
            return law
        except IndexError:
            # if there are more pages, fetch the next page
            if self.params['page'] < self.pages:
                # next page is a new json, reset seq to 0 and increment page number
                self.params['page'] += 1
                self.seq = 0
                self.fetch()
                return self.next()
            # when fetching the last page, reset page number and seq for next search
            self.params['page'] = 1
            self.seq = 0
            self.pages = 0
            return None
