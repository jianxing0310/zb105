# coding: utf-8
# # 每日爬蟲直接寫入資料庫

import time
import requests
from bs4 import BeautifulSoup as bs
import datetime
import re
import time
import json
import ast  #轉換成json需要套件
import string
import pymongo
from pymongo import MongoClient

client = MongoClient()
database = client["test1"] 
collection = database["ltn05"] 


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday1 = yesterday.strftime("%Y%m%d")  
#print yesterday1

with open('C:/Users/BIG DATA/Desktop/python/essay/{}.txt'.format(yesterday1), 'w') as f:
    url = 'http://news.ltn.com.tw/newspaper/focus/{}'.format(yesterday1)
    res = requests.get(url)
    soup = bs(res.text)

    Times = 'http://news.ltn.com.tw'
    sort = soup.select('.newspaper a')

    for a in xrange(0, len(sort)):
        url2 = Times + sort[a]['href'] #分類網址
        res2 = requests.get(url2)
        soup2 = bs(res2.text)
        #print len(soup2.select('.p_num'))
        if len(soup2.select('.p_num')) == 1 : #判斷此類別新聞是否一頁
            title = soup2.select('.picword')
            title_num = len(soup2.select('.picword')) #計算有幾篇文章(每天新聞數量不同)
            for i in xrange(0 , title_num):   
                url1=Times+title[i]['href']   #文章網址
                f.write(url1  + '\n')  #寫入text
        else:
            for page1 in xrange (1,len(soup2.select('.p_num'))+1): #此類別新聞超過一頁時執行
                url3= url2+'?page={}'.format(page1)
                #print url3
                res3 = requests.get(url3)
                soup3 = bs(res3.text)
                title = soup3.select('.picword')
                title_num1 = len(soup3.select('.picword')) #計算有幾篇文章(每天新聞數量不同)
                for i in xrange(0 , title_num1):   
                    url1=Times+title[i]['href']   #文章網址
                    f.write(url1  + '\n')  #寫入text


# 標題,類別,內文,關鍵詞,新聞連結網址,日期(格式yyyyMMdd)
# 爬回

def wr_all(url):  #方法 大部分的網頁版型
    res = requests.get(url)
    res.encoding = "UTF-8"
    soup = bs(res.text)
    essay = soup.select('#newstext p , h4')
    tital = soup.select('h1 ')[0].text.encode('utf-8')
    date1 =  soup.select('#newstext span ')[0].text.encode('utf-8')
    category = soup.select('.guide  a ')[1].text.encode('utf-8')
    comp = " LibertyTimes"
    date = string.replace(date1, '-', '')[0:8]
    page=""                          #給一個字串,存放內文用           
    for div3 in essay[0:(len(essay))]:
        page += div3.text.encode('utf-8')       #加入內文

    return tital,date,category, page,comp
        
def wr_sport(url):  #方法 運動類的網頁版型
    res = requests.get(url)
    res.encoding = "UTF-8"
    soup = bs(res.text)    
    essay = soup.select('h4 , p')
    tital = soup.select('.Btitle ')[0].text.encode('utf-8')
    date1 =  soup.select('.news_content .date ')[0].text.encode('utf-8')
    category = "體育"
    comp = " LibertyTimes"
    date = string.replace(date1, '/', '')[0:8]

    page=""                          #給一個字串,存放內文用           
    for div3 in essay[0:(len(essay))]:
        page += div3.text.encode('utf-8')       #加入內文  
        
    return tital,date,category, page,comp

def wr_ent(url):  #方法 娛樂類的網頁版型
    res = requests.get(url)
    res.encoding = "UTF-8"
    soup = bs(res.text)
    essay = soup.select('p')
    tital = soup.select('.news_content h1 ')[0].text.encode('utf-8')
    date1 =  soup.select('.news_content .date')[0].text.encode('utf-8')
    date = string.replace(date1, '/', '')[0:8]
    category = "娛樂"
    comp = " LibertyTimes"
    page=""                          #給一個字串,存放內文用           
    for div3 in essay[0:(len(essay))]:
        page += div3.text.encode('utf-8')       #加入內文   
    return tital,date,category, page,comp

def wr_local(url): #方法 地方類的網頁版型
    res = requests.get(url)
    res.encoding = "UTF-8"
    soup = bs(res.text)
    essay = soup.select('#newstext p , h4')
    tital = soup.select('h1 ')[0].text.encode('utf-8')
    date1 =  soup.select('#newstext span ')[0].text.encode('utf-8')
    category = "地方"
    comp = " LibertyTimes"
    date = string.replace(date1, '-', '')[0:8]
    page=""                          #給一個字串,存放內文用           
    for div3 in essay[0:(len(essay))]:
        page += div3.text.encode('utf-8')       #加入內文
    return tital,date,category, page,comp
    
def wr_talk(url): # 方法 言論類的網頁版型
    res = requests.get(url)
    res.encoding = "UTF-8"
    soup = bs(res.text)
    essay = soup.select('.cont p')
    tital = soup.select('h2 ')[0].text.encode('utf-8')
    date1 =  soup.select('.writer span')[0].text.encode('utf-8')
    date = string.replace(date1, '-', '')[0:8]
    category = "言論"
    comp = " LibertyTimes"
    page=""                          #給一個字串,存放內文用           
    for div3 in essay[0:(len(essay))]:
        page += div3.text.encode('utf-8')       #加入內文    
    return tital,date,category, page,comp


with open('C:/Users/BIG DATA/Desktop/python/essay/{}.txt'.format(yesterday1), 'r') as f:
    for line in f.readlines():
        url = line.strip()
        m = re.match('.*news/(\w+)/paper/(\w+)' ,url)  #正規表達法 切出m.group(1)類別 與 m.group(2)網頁最後的數字(用來當檔名)
        print m.group(1)
        if m.group(1) == 'sports': #判斷是否為體育類
            x=  wr_sport(url) #使用方法
            data ={'title' :x[0],'category' : x[2],'content' : x[3],'url':url,'date':x[1],'comp':x[4],'keyw':'','hitcount':0,'date2':yesterday1[0:6]}
            collection.insert_one(data)
            time.sleep(1.5)

        elif m.group(1) == 'entertainment':#判斷是否為娛樂類
            x= wr_ent(url) #使用方法
            data ={'title' :x[0],'category' : x[2],'content' : x[3],'url':url,'date':x[1],'comp':x[4],'keyw':'','hitcount':0,'date2':yesterday1[0:6]}
            collection.insert_one(data)
            time.sleep(1.5)


        elif m.group(1) =='local': #判斷是否為地方類
            x= wr_local(url) #使用方法
            data ={'title' :x[0],'category' : x[2],'content' : x[3],'url':url,'date':x[1],'comp':x[4],'keyw':'','hitcount':0,'date2':yesterday1[0:6]}
            collection.insert_one(data)
            time.sleep(1.5)

        elif m.group(1) =='opinion': #判斷是否為言論類
            x= wr_talk(url) #使用方法
            data ={'title' :x[0],'category' : x[2],'content' : x[3],'url':url,'date':x[1],'comp':x[4],'keyw':'','hitcount':0,'date2':yesterday1[0:6]}
            collection.insert_one(data)
            time.sleep(1.5)

        else:
            x= wr_all(url) #使用方法
            data ={'title' :x[0],'category' : x[2],'content' : x[3],'url':url,'date':x[1],'comp':x[4],'keyw':'','hitcount':0,'date2':yesterday1[0:6]}
            collection.insert_one(data)
            time.sleep(1.5)



data.clear()




