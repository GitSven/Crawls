# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 09:19:20 2015

@author: sven
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import os
#import sys, os
#reload(sys)
#sys.setdefaultencoding('utf-8')

#add logging
import logging

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Referer':
        'http://www.lecuntao.com/shop/index.php?province_id=140'
    }
TIME_OUT = 5
#ERROR_NUM = '111'
INDEX = 'http://www.lecuntao.com/shop/index.php?act=category&op=index'


def make_file(goods):
    '''
    检查文件是否存在，存在的话则重命名,然后写入信息
    '''
    logger.info('making file start...')
    start_mf = time.time()
    
    name = time.strftime('%Y-%m-%d', time.localtime()) + '-1'
    while os.path.exists(name):
        name = name[:-1] + str(int(name[-1])+1)

    # items_file = open(name, 'a')
    with open(name, 'a') as items_file:
    # try:
        for goods_id in goods.keys():
            items_file.write(
                goods_id + ',' + goods[goods_id].encode('utf-8') + '\n')
    
    end_mf = time.time()
    logger.info('making file end...')
    logger.info('make file time ' + str(end_mf - start_mf))
#            items_file.write(goods_id + ',' + goods[goods_id][0] + ',' +
#                goods[goods_id][1] + ',' + goods[goods_id][2] + '\n', )
    # finally:
    #    items_file.close()


def crawl(url):
    '''
    抓取页面，如果超时，则返回ERROR_NUM；正常则返回html
    '''
    try:
        request = requests.get(url, headers=HEADERS, timeout=TIME_OUT)
    except Exception, e:
        print e
        logger.info('=====crawl field=====',e)        
        return ''

    return request.text


def parse(html):
    '''
    页面分析，如果接收到的内容是ERROR_NUM，则说明超时了，则无需在分析；
    如果正常，则分别匹配出商品的id，name，price，stat，并写到以日期命名的文件中
    '''
    if not html:
        logger.info('======pass parse=====')
        return {}

    items = {}
#    print isinstance(html, str)
    parse_page = BeautifulSoup(html)
    goods = parse_page.find_all('div', class_='goods-content')

    for good in goods:

        good_id = good['nctype_goods'][1:]#在开始有一个空格

        good_name = good.select('div[class="goods-name"]')[0].a.text.replace(',', '_')

        good_price = good.select('em[class="sale-price"]')[0].text
        if re.findall(u'\u4e07', good_price):#处理‘1.3万’这种价格
            good_price = str(float(good_price[:-1])*10000)
        else:#去掉价格里的人民币符号
            good_price = good_price[1:]

        good_stat = good.select('a[class="status"]')[0].text

        items[good_id] = good_name + ',' + good_price + ',' + good_stat

    return items


def get_cate_list():
    '''
    取得所有分类的连接
    '''
    logger.info('parse cate list start...')
    index_page = crawl(INDEX)
    links_div = BeautifulSoup(index_page).find_all('div', class_='class')

#    cate_links = []
    for div in links_div:
#        cate_links.append(div.a['href'])
        cate_links = div.a['href']
        yield cate_links
    
    logger.info('parse cate list end...')
#    return cate_links


def main():
    start_main = time.time()
    logger.info('misson start...')
    items = {}
    logger.info('parse start...')
    cates = get_cate_list()
    last_r = u'</span></a></li><li><span>\u4e0b\u4e00\u9875</span></li></ul>'
    next_r = r'</li><li><a class="demo" href="http://.*?/cate-.*?.html'

    for cate in cates:

        current_link = cate

        while 1:

            logger.info(current_link)
            current_page = crawl(current_link)
            current_page_items = parse(current_page)
            items.update(current_page_items)

            if len(re.findall(last_r, current_page)) > 0:#last page
                logger.info('goto next cate')
                break
            else:#next page
                match_links = re.findall(next_r, current_page)
                if match_links:
                    current_link = match_links[0][31:]
                else:
                    logger.info('can not get link in this page, goto next cate')
                    break
    end_p = time.time()
    logger.info('parse end...')
    logger.info('parse used time'+str(end_p - start_main))
    
    make_file(items)

    end_main = time.time()
    logger.info('misson end...')
    logger.info('misson used time'+str(end_main - start_main))

if __name__ == '__main__':
    main()

