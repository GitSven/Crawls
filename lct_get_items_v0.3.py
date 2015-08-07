# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 07:17:16 2015

@author: sven
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Referer':
        'http://www.lecuntao.com/shop/index.php?act=category&op=index'
    }
TIME_OUT = 5
ERROR_NUM = '111'
FILE_NAME = ''


def check_file_name():
    '''
    检查文件是否存在，存在的话则重命名
    '''
    name = time.strftime('%Y-%m-%d', time.localtime()) + '-1'
    while os.path.exists(name):
        name = name[:-1] + str(int(name[-1])+1)
    global FILE_NAME
    FILE_NAME = name


def crawl(url):
    '''
    抓取页面，如果超时，则返回ERROR_NUM；正常则返回html
    '''
    try:
        request = requests.get(url, headers=HEADERS, timeout=TIME_OUT)
    except Exception as e:
        print e
        print 'return ERROR_NUM'
        return ERROR_NUM
    return request.text


def parse(html):
    '''
    页面分析，如果接收到的内容是ERROR_NUM，则说明超时了，则无需在分析；
    如果正常，则分别匹配出商品的id，name，price，stat，并写到以日期命名的文件中
    '''
    if html == ERROR_NUM:
        print 'pass parse'
        return ERROR_NUM

    items = open(FILE_NAME, 'a')
    
    parse_page = BeautifulSoup(html)
    goods = parse_page.find_all('div', class_='goods-content')
    for good in goods:
        good_id = good['nctype_goods']
        good_name = good.select('div[class="goods-name"]')[0].a.text.replace(',', '_')

        good_price = good.select('em[class="sale-price"]')[0].text
        if re.findall(u'\u4e07', good_price):#处理‘1.3万’这种价格
            good_price = str(float(good_price[:-1])*10000)
        else:#取得价格里的人民币符号
            good_price = good_price[1:]

        good_stat = good.select('a[class="status"]')[0].text
        items.write(good_id + ',' + good_name + ','
                        + good_price + ',' + good_stat + '\n')
    items.close()


def main():
    check_file_name()
    #取得所有分类的连接列表
    start_link = 'http://www.lecuntao.com/shop/index.php?act=category&op=index'
    start_page = crawl(start_link)
    soup_start_page = BeautifulSoup(start_page)
    link_lists = soup_start_page.find_all('h4')
    
    for link_list in link_lists:
        try:
            current_link = link_list.a['href']
        except Exception as e:
            print e
            print 'error match, goto next cate'
            continue
        while 1:
            print current_link
            current_page = crawl(current_link)
            parse(current_page)
            if len(re.findall(
                    u'</span></a></li><li><span>\u4e0b\u4e00\u9875</span></li></ul>',
                    current_page)
                ) > 0:#last page
                print 'goto next cate'
                break
            else:#next page
                match_links = re.findall(
                    r'</li><li><a class="demo" href="http://www.lecuntao.com/shop/cate-.*?.html',
                    current_page)
                try:
                    current_link = match_links[0][31:]
                except Exception as e:
                    print e
                    print 'can not get link in this page, goto next cate'
                    break

if __name__ == '__main__':
    main()