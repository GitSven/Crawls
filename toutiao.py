# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:23:35 2015

@author: 95
"""
import urllib2
import re
import time
import sys

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
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #待匹配的内容的正则表达式编译
    item_pattern = [re.compile('">.*</a></h2>'), #匹配文章标题
                    re.compile(': \d+</td>')]#匹配阅读量，顶，评论
    #将当前爬取得网页放到temp文件中
    temp = open('temp', 'w')
    temp.write(response.read().decode('utf-8'))
    temp.close()
    #讲temp文件打开为可读模式
    temp = open('temp', 'r')
    #将所需内容准备写入到lct_items文件
    lct_items = open('test1.csv', 'a')
    try:    
        i = 0#格式化内容所需变量
        for line in temp:
            for pattern in item_pattern:
                #将temp中的行依次接收匹配
                result = re.search(pattern, line)
                if result:
                    i += 1#匹配成功一次，累加1
                    if i % 4 == 1 and i % 81 != 0:
                        #文章标题，格式化输出
                        lct_items.write(result.group().replace(',','_')[2:-9] + ',')
                    if i % 4 == 2:
                        #阅读量
                        lct_items.write(result.group()[2:-5] + ',')
                    if i % 4 == 3:
                        #顶
                        lct_items.write(result.group()[2:-5] + ',')
                    if i % 4 == 0:
                        #评论
                        lct_items.write(result.group()[2:-5] + ',' + '\n')
                    
    except Exception, e :
        print e
    finally:
        lct_items.close()
        temp.close()
    #下次抓取延时3s
    time.sleep(3)

def lct_crawl():
    print 'Mission Start'
    page = 1
    #lct_searchresult = 'http://www.lecuntao.com/shop/?act=search&keyword=%2C'
    while page < 3:       
        url_items_list = 'http://toutiao.com/m4103349596/p'+str(page)
        parse(crawl(url_items_list))
        page += 1
    print 'Mission Complete'

lct_crawl()
