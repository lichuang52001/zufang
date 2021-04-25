# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:33:26 2021
Beijing Zufang
Ref: https://blog.csdn.net/ALBDXV/article/details/109375377
"""

import requests
import urllib.request#urllib.request功能的了解
from bs4 import BeautifulSoup#BeautifulSoup功能了解
import bs4
import random
import re

##通过函数获取网页信息
def gethtml(url):
    #用代理IP访问
    proxy_support = urllib.request.ProxyHandler({'http':'119.6.144.73:81'})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363')]
    urllib.request.install_opener(opener)
    #读取网页信息
    #zf = urllib.request.urlopen('https://sh.lianjia.com/zufang/anting/rt200600000001l0/')
    zf = urllib.request.urlopen(url)
    #'https://ks.lianjia.com/zufang/kunshan/rt200600000001l0/'
    html = zf.read()
    ht = html.decode('utf8')
    zf.close
    Soup = BeautifulSoup(ht,'lxml')
    return Soup

##定义一些循环中会用到的变量
info = []
page = 1
TotalNumber = 0
urlMain = 'https://bj.lianjia.com/zufang/tongzhou/'
urlOption = 'rt200600000001/'
#一共有多少条结果，防止找到限制条件以外的推荐结果
Number = int(gethtml(urlMain+urlOption).find(class_ = 'content__article').find(class_ = 'content__title').find('span').text)
print('已找到{}套租房'.format(Number))

##用while循环去读取每一页的租房信息
while TotalNumber <= Number:
    print('正在读取第%d页'%page)
    if page == 1:
        url = urlMain + urlOption
    else:
        url = urlMain +'pg{}'.format(page) + urlOption
    Soup = gethtml(url)
    ###找到地址，价格，网址在网页中的位置，然后用find筛选出来
    Soup = Soup.find_all(class_ = 'content__list--item')
    numberOfThisPage = len(Soup)
    print('该页有%d条租房信息'%numberOfThisPage)
    print('')
    counter = 0
    for Soup in Soup:
        #print(Soup)
        counter+=1
        #print(counter)
        Address = Soup.find(class_ = 'content__list--item--des').find_all('a')
        if Address == []:
            continue
        else:
            #print(Address)
            Address_DistrictName = Address[2].text
            Address_Location = Address[0].text+'，'+Address[1].text
            Price = Soup.find('em').text
            Website = Soup.find(class_ = 'content__list--item--title').find('a')['href']
            Website = 'https://bj.lianjia.com'+Website
        info.append([Address_DistrictName,Address_Location,Price,Website])
        ###写入表格中
        fo=open("zufang.csv","w")
        for row in info:
            fo.write(",".join(row)+"\n")
        fo.close()
        if counter == numberOfThisPage:
            break
    TotalNumber += counter
    page += 1
    
