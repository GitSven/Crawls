# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 09:19:20 2015

@author: sven
"""

import requests
from bs4 import BeautifulSoup
import re
import urllib
import os

HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Referer':
        'http://www.fuliti.com/'
    }
TIME_OUT = 5
INDEX = 'http://www.fuliti.com/category/mizitu/page/'

#抓取页面，如果超时，则返回ERROR_NUM；正常则返回html
def crawl(url):
    try:
        request = requests.get(url, headers=HEADERS, timeout=TIME_OUT)
    except Exception, e:
        print e
        print '===crawl url field==='
        return ''
    return request.text

# 取得所有的pic页面
def get_page_list():
    page_links = []
    for i in xrange(3, 8):
        current_url = INDEX+str(i)
        print 'website_url: ' + current_url
        page = crawl(current_url)
        h2s = BeautifulSoup(page).find_all('h2')
        for href_div in h2s:
            page_links.append(href_div.a['href'])
    return page_links

# 获取页面的所有pic
def get_pic_list(page):
    img_list = []
    print 'pic_page: ' + page
    html = crawl(page)
    parse_page = BeautifulSoup(html)
    imgs_div = parse_page.find_all('div', class_='context')[0]
    imgs = re.findall(r'src=".*\.jpg"', str(imgs_div))
    for img in imgs:
        img_list.append(img[5:-1])
    return img_list


def save(imgsrc, name):
    u = urllib.urlopen(imgsrc)
    data = u.read()
    f = open(name, 'wb')
    f.write(data)
    f.close()


def main():
    j = 0
    for page in get_page_list():
        i = page[22:-5]
        for pic in get_pic_list(page):
            j += 1
            name = str(i) + '_' + str(j) + '.jpg'
            save(pic, name)
            print 'save'+name

if __name__ == '__main__':
    main()

