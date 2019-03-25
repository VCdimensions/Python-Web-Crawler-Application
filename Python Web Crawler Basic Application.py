# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:04:23 2016

@author: SUNG ANN LEE
"""

'''
什麼是網路爬蟲?
爬蟲? 這不是在看動物星球，而是一種利用HTTP Request 抓取網路資料的技術。
想想看如果你要做個比價網站或資料分析，但苦無資料的時候，又來不及跟別人談資料交換或
合作時，就可以利用這種技術將別人的資料庫變成自己的資料庫，聽起來很迷人嗎？趕快來了
解一下。
'''
'''
什麼是網路爬蟲?

爬蟲? 這不是在看動物星球，而是一種利用HTTP Request 抓取網路資料的技術。想想看如果
你要做個比價網站或資料分析，但苦無資料的時候，又來不及跟別人談資料交換或合作時，就
可以利用這種技術將別人的資料庫變成自己的資料庫，聽起來很迷人嗎？趕快來了解一下。
'''
'''
如何安裝 Jupyter (Ipython Notebook)

今天要跟各位介紹個好用的工具"Jupyter"！Jupyter 提供一個網頁介面，讓使用者可以透過
瀏覽器連線進網頁服務，並在上面進行Julia, Python 或 R 程式的開發與維護！功能相當強
大，不可錯過！之後我們會陸續介紹到它有多麼好用！
'''
'''
Jupyter 操作入門 (1)

Jupyter 可以說是開發、維護Python 程式的好幫手，今天介紹該如何在Jupyter 中引入
pylab 進行繪圖、使用類linux 指令觀看當前目錄的檔案、執行python 程式，以及如何使
用MathJax 繪製數學方程式。
'''
%pylab inline #讀入多個繪圖相關的套件

import random 
plot(range(1,10),[random.randint(1,10) for i in range(1,10)])

%ls #加%可以在windos使用linux的ls

'''
如何使用GET 抓取網頁內容?

為大家示範Python如何使用簡單三行程式碼就可以抓取淘寶網的網頁內容 範例網頁:
    http://tw.taobao.com/product/%E5%A4%9A%E6%A8%A3%E5%B1%8B-%E8%91%AB%E8%9
    8%86-%E4%BF%9D%E6%BA%AB%E6%9D%AF.htm
'''
import requests
res = requests.get("http://tw.taobao.com/product/%E5%A4%9A%E6%A8%A3%E5%B1%8B-%E8%91%AB%E8%98%86-%E4%BF%9D%E6%BA%AB%E6%9D%AF.htm")
print( res.text)

'''
如何使用POST 抓取網頁內容?

POST 是另一種HTTP 請求方法，讓你可以將請求資訊包裝起來後，再送至伺服器以取得回應資
訊，在Python 中使用POST 的方法一樣簡單，只需將請求資訊以字典做包裝即可，本單元將敎
您如何使用POST 方法抓取高鐵網頁內容。
示範網址:https://www.thsrc.com.tw/tw/TimeTable/SearchResult
'''
import requests

payload = {
           'StartStation':'2f940836-cedc-41ef-8e28-c2336ac8fe68',
           'EndStation':'e6e26e66-7dc1-458f-b2f3-71ce65fdc95f',
           'SearchDate':'2016/11/17',
           'SearchTime':'15:00',
           'SearchWay':'DepartureInMandarin'
}

res = requests.post("https://www.thsrc.com.tw/tw/TimeTable/SearchResult",data=payload)

print(res.text)


'''
如何使用Python 套件: BeautifulSoup4 剖析網頁內容?

終於進到該如何使用BeautifulSoup4 剖析網頁內容的部分了！簡簡單單幾個Select 動作，可
以快速幫您抓取非結構化資料中有價值的部分，有了資料，想當然爾，分析只是一步之遙！
'''
from bs4 import BeautifulSoup

html_sample = ' \
<heml> \
 <body> \
   <h1 id="title">Hello World</h1> \
   <a herf="#" class="link">This is link1</a> \
   <a herf="# link2" class="link">This is link2</a> \
 </body> \
</html>'

soup = BeautifulSoup(html_sample)

#抽取不含Tag的資訊
print(soup.text) 
#全部的內容抓出抓在list
print(soup.contents) 
#抓出html的內容放入list
print(soup.select('html')[0])
#抓出h1的內容放入list 
print(soup.select('h1'))
#抓出a的內容放入list 
print(soup.select('a')) 
print(soup.select('a')[0]) #第一個a的內容
print(soup.select('a')[1])
#抓取id用#加上id名稱  抓取class用.加上class名稱
print(soup.select('#title'))
print(soup.select('.link'))
print(soup.select('.link')[0])
print(soup.select('.link')[1])

'''
如何使用Python 的requests 及BeautifulSoup4 完成淘寶爬蟲?

既然已經知道如何使用requests 抓取頁面內容，也懂得如何使用BeautifulSoup4 剖析有用
資訊，接下來我們就進入實戰階段，示範如何使用Python 的requests 及BeautifulSoup4 
完成淘寶爬蟲！
示範網址:http://tw.taobao.com/product/%E5%A4%9A%E6%A8%A3%E5%B1%8B-%E8%91%AB%E8%98%86-%E4%BF%9D%E6%BA%AB%E6%9D%AF.htm
'''
import requests
from bs4 import BeautifulSoup
res = requests.get("http://tw.taobao.com/product/%E5%A4%9A%E6%A8%A3%E5%B1%8B-%E8%91%AB%E8%98%86-%E4%BF%9D%E6%BA%AB%E6%9D%AF.htm")
soup = BeautifulSoup(res.text)
#使用info lite確定要抓的資料屬於什麼
#在這個範例中每個商品是屬於.item  價格是在strong
for item in soup.select('.item'):
    print(item.select('strong'))
for item in soup.select('.item'):
    print(item.select('strong')[0].text) #將list中的價格抓出來
#每個商品的名稱為.title
for item in soup.select('.item'):
    print(item.select('.title')[0].text) #將list中的商品名稱抓出來
#裡用strip將空白移除
for item in soup.select('.item'):
    print(item.select('.title')[0].text.strip()) 
#將價格與商品名稱抓出
for item in soup.select('.item'):
    print(item.select('strong')[0].text,item.select('.title')[0].text.strip())
#加入來自哪的資訊
for item in soup.select('.item'):
    print(item.select('strong')[0].text,item.select('.title')[0].text.strip(),item.select('.J_NickPopup')[0].text)

'''
探索Facebook 隱藏的秘密: 使用Graph API

今天來說些好玩的，教學大家該如何使用Facebook Graph API 探索個人的隱私，想測試使用
Graph API，可以連線到 Facebook Developer Page: https://developers.facebook.com/
'''

'''
探索Facebook 隱藏的秘密: 使用Python 存取 Facebook 資訊

緊接著上一段，如何使用Graph API 存取FB 資訊後，我們接者示範只要擷取access token 
後，把access token 資訊填入Graph API 中即可透過Python 的requests取得個人資訊(ID,
 最喜歡的運動員)
'''
import requests
token = 'EAACEdEose0cBANoRx7Rv750spr8JXetVOaBp8g7YhmWcgLSSPdU32eyuPvyEWe0AYObZCqZBqJpmhsj82YuIfo58z1txncxE9vGXuEpsq1FezBuwimZAj98J8tQ9gGycicaM7VhqZAIaNbauxkuBOOZBOOXYd44zDGJJ1DSI7JP8eWe3uNF4R'
res = requests.get("https://graph.facebook.com/v2.8/me?access_token=%s&debug=all&format=json&method=get&pretty=0&suppress_http_code=1"%(token))
print(res.text)

#因為抓回來的資料是Json格式 所以要用Json.loads將Json轉為python中的dictionary物件
import requests
import json
token = 'EAACEdEose0cBANoRx7Rv750spr8JXetVOaBp8g7YhmWcgLSSPdU32eyuPvyEWe0AYObZCqZBqJpmhsj82YuIfo58z1txncxE9vGXuEpsq1FezBuwimZAj98J8tQ9gGycicaM7VhqZAIaNbauxkuBOOZBOOXYd44zDGJJ1DSI7JP8eWe3uNF4R'
res = requests.get("https://graph.facebook.com/v2.8/me?access_token=%s&debug=all&format=json&method=get&pretty=0&suppress_http_code=1"%(token))
jsondata = json.loads(res.text) #為dictionary
print(jsondata['id']) #查我的id
print(jsondata['name'])


#查我的facebook朋友 並列出
import requests
import json
token = 'EAACEdEose0cBANoRx7Rv750spr8JXetVOaBp8g7YhmWcgLSSPdU32eyuPvyEWe0AYObZCqZBqJpmhsj82YuIfo58z1txncxE9vGXuEpsq1FezBuwimZAj98J8tQ9gGycicaM7VhqZAIaNbauxkuBOOZBOOXYd44zDGJJ1DSI7JP8eWe3uNF4R'
#網址改為https://graph.facebook.com/v2.8/me/friends
res = requests.get("https://graph.facebook.com/v2.8/me/friends?access_token=%s&debug=all&format=json&method=get&pretty=0&suppress_http_code=1"%(token))
jsondata = json.loads(res.text) #為dictionary
print(jsondata['data'])
#印出每個朋友名字
for friend in jsondata['data']:
    print(friend['name'])
#印出每個朋友id
for friend in jsondata['data']:
    print(friend['id'])



























