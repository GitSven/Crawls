# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:23:35 2015

@author: 95
"""
import urllib2
import re
import time

def crawl(url):
    #设置headers    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    headers = {'User-Agent' : user_agent}
    #开始爬取 
    print 'current_url: ' + url
    try:
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)
    except Exception, e:
        print e
        return 0
    return response

def parse(response):
    #待匹配的内容的正则表达式编译
    item_pattern = [re.compile('goods=" \d*"'), #匹配商品的id
                    re.compile('>.*<em>'),#匹配商品名
                    re.compile('&yen;\d+\.\d{2}">'),#匹配市场价和商城价
                    re.compile('>\d+</a><p>')]#匹配销量和评论量
    #将当前爬取得网页放到temp文件中
    temp = open('temp', 'w')
    temp.write(response.read().decode('utf-8'))
    temp.close()
    #讲temp文件打开为可读模式
    temp = open('temp', 'r')
    #将所需内容准备写入到lct_items文件
    lct_items = open('lct_items.csv', 'a')
    try:    
        i = 0#格式化内容所需变量
        for line in temp:
            for pattern in item_pattern:
                #将temp中的行依次接收匹配
                result = re.search(pattern, line)
                if result:
                    i += 1#匹配成功一次，累加1
                    if i % 7 == 1:
                        #匹配到了id，格式化输出
                        lct_items.write(result.group()[8:-1] + ',')
                    if i % 7 == 2:
                        #匹配到了商品名称，格式化输出
                        lct_items.write(result.group().replace(',','_')[1:-4] + ',')
                    if i % 7 == 4:
                        #匹配到了商城价，格式化输出；值为3时为网页注释中的商品名；5时为市场价
                        lct_items.write(result.group()[5:-2] + ',')
                    if i % 7 == 6:
                        #匹配到了销量，格式化输出
                        lct_items.write(result.group()[1:-7] + ',')
                    if i % 7 == 0:
                        lct_items.write('\n')
    except Exception, e :
        print e
    finally:
        lct_items.close()
        temp.close()
    #下次抓取延时3s
    time.sleep(3)

def lct_crawl():
    page = 1
    #lct_searchresult = 'http://www.lecuntao.com/shop/?act=search&keyword=%2C'
    while page < 3:        
        url_items_list = 'http://www.lecuntao.com/shop/cate-0-0-0-0-0-0-0-'+str(page)+'.html'
        parse(crawl(url_items_list))
        page += 1
    print "Mission Complete"

lct_crawl()

