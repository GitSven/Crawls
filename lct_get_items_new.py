# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 07:17:16 2015

@author: sven
"""

import requests
from bs4 import BeautifulSoup
import datetime
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Referer': 'http://www.lecuntao.com/shop/index.php?act=category&op=index'    
    }
TIME_OUT = 5
ERROR_NUM = 111
#抓取页面    
def crawl(url):
    try:    
        rq = requests.get(url, headers = HEADERS, timeout = TIME_OUT)
    except:
        print '---timeout---'
        return ERROR_NUM
    return rq.text

#分析页面
def parse(html):
    if html == ERROR_NUM:
        print 'pass parse'        
        return str(ERROR_NUM)
    day = str(datetime.date.today())
    lct_items = open(day, 'a')
    
    soup = BeautifulSoup(html)
    goods = soup.find_all('div', class_='goods-content')
    for good in goods:
        good_id = good['nctype_goods']
        good_name = good.select('div[class="goods-name"]')[0].a.text.replace(',','_')
        good_price = good.select('em[class="sale-price"]')[0].text
        good_stat = good.select('a[class="status"]')[0].text
        lct_items.write(good_id + ',' + good_name + ',' + good_price + ',' + good_stat + '\n')
        
    lct_items.close()

#取得所有分类的连接列表 
start_url = 'http://www.lecuntao.com/shop/index.php?act=category&op=index'
list_page = crawl(start_url)
soup = BeautifulSoup(list_page)
list_links = soup.find_all('h4')

for list_link in list_links:
    try:    
        current_link = list_link.a['href']
    except:
        print 'error match'
        continue
    while 1:
        print current_link
        current_page = crawl(current_link)
        parse(current_page)
        if len(re.findall(u'</span></a></li><li><span>\u4e0b\u4e00\u9875</span></li></ul>', current_page))>0:#last page
            print 'get next cate'
            break
        else:#next page
            match_links = re.findall(
                r'</li><li><a class="demo" href="http://www.lecuntao.com/shop/cate-.*?.html', current_page)
            try:
                current_link = match_links[0][31:]
            except:
                print 'can not get link in this page'
                break
