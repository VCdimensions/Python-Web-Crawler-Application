 # -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:04:56 2016

@author: SUNG ANN LEE
"""
'''
[爬蟲實戰] 如何抓取心食譜的食譜資訊?

今天要示範如何使用CSS Selector 的nth-of-type 抓取特定位置的食譜資訊。示範網頁於下
列URL: http://www.xinshipu.com/zuofa/49391
'''
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
os.getcwd()
os.chdir('C:\\Users\\SUNG ANN LEE\\Desktop')

#使用selenium裡面的webdriver啟動 chromedriver，因為 requests.get("http://www.xinshipu.com/zuofa/49391")只能抓到經過javascript變換後的html，跟最後我們看到的網頁的html不一樣
#啟動chrome瀏覽器
driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
url = 'http://www.xinshipu.com/zuofa/49391'
#獲取url的html(我們看到的page source)
driver.get(url)
#將html轉為DOM Tree格式
soup = BeautifulSoup(driver.page_source)
#將資料從list中取出
reup = soup.select('.re-up')[0]
#獲取商品名稱 我們看到商品名稱在font18 no-overflow的class，輸入時空格要用.代替
print(reup.select('.font18.no-overflow')[0].text) #.text代表只取出html非tag(文字)的部分
#獲取商品評分與評價 兩個都在font16 ml10 col的class
print(reup.select('.font16.ml10.col')[0].text)
print(reup.select('.font16.ml10.col')[1].text)
#獲取食譜號、閱讀次數與收藏次數
print(reup.select('.cg2.mt12'))
#由於食譜號在第二個span閱讀次數在第四個span收藏次數在第六個span，我們可以用span:nth-of-type指定或取第幾個span的內容
print(reup.select('.cg2.mt12 span:nth-of-type(2)')[0].text)
print(reup.select('.cg2.mt12 span:nth-of-type(4)')[0].text)
print(reup.select('.cg2.mt12 span:nth-of-type(6)')[0].text)
#整合所有商品所有資訊
print(reup.select('.font18.no-overflow')[0].text) #.text代表只取出html非tag(文字)的部分
print(reup.select('.font16.ml10.col')[0].text)
print(reup.select('.font16.ml10.col')[1].text)
print(reup.select('.cg2.mt12 span:nth-of-type(2)')[0].text)
print(reup.select('.cg2.mt12 span:nth-of-type(4)')[0].text)
print(reup.select('.cg2.mt12 span:nth-of-type(6)')[0].text)



'''
[爬蟲實戰 ]如何模擬用戶代理 (User Agent) 成功存取目標網頁內容 (以永慶房屋為例)?

有的網頁伺服器，會透過檢查用戶代理(User Agent)，以限制爬蟲存取頁面內容，此時我們只
要在標頭上增加自身瀏覽器所使用的用戶代理(User Agent) 就可成功騙過對方伺服器，存取網
頁內容！我們便能使用這技術成功抓取永慶房屋的房價資訊瞜！
範例網址:https://buy.yungching.com.tw/region
'''
import requests
from bs4 import BeautifulSoup
#找出我們GET資料的request headers(我們送出GET請求的表頭)裡面的User-Agent這樣就能偽裝為我們正在使用的瀏覽器進行爬蟲
head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
res = requests.get('https://buy.yungching.com.tw/region',headers = head)
#單純用requests.get無法得到網頁資訊，現在加入User-Agent就可以了
print(res.text)
#可以抓到報價資訊
soup = BeautifulSoup(res.text)
print(soup.select('.price-num')[0].text)


'''
[爬蟲實戰] 如何爬取PTT的網頁?

本次實戰將教您如何從PTT 的Food版(https://www.ptt.cc/bbs/Food/index.html)v抓取鄉
民寶貴的言論，以利之後做美食的文字探勘分析！
範例網址:https://www.ptt.cc/bbs/Food/index5904.html
'''
import requests
#將verify設定為False，Request就能忽略對SSL證書的驗證
res = requests.get('https://www.ptt.cc/bbs/Food/index5904.html',verify=False)
#如此就能存取使用https的頁面內容
print(res.text)


'''
[爬蟲實戰] 如何剖析PTT的網頁?

繼之前教學過該如何透過requests 的 get 取得PTT 網頁內容後，還必須將有意義的結構化資
訊從回傳的原始碼之中抽取出來，本範例將介紹該如何使用 BeautifulSoup4 將發文者的文章
標題、作者及發文時間剖析出來!
'''
import requests
from bs4 import BeautifulSoup

res = requests.get('https://www.ptt.cc/bbs/Food/index5904.html',verify=False)
soup = BeautifulSoup(res.text)
#擷取標題、日期與作者
for entry in soup.select('.r-ent'):
    print(entry.select('.title')[0].text,entry.select('.date')[0].text,entry.select('.author')[0].text)

'''
[爬蟲實戰] 如何告訴PTT我已滿18並順利抓取八卦版的文章 ?

雖然已滿18歲多年，但是不知道你實際年齡的PTT，還是要禮貌性的問你是否滿18後­，才能讓
你閱讀八卦版裡面的內容，但人可以做點選，爬蟲呢？於是我們便可以先透過Ch­rome開發人員
工具快速找到如何使用POST方法通過18歲驗證後，再接續之前的S­ession，就能順利存取八卦版
的內容！
示範網址:https://www.ptt.cc/bbs/Gossiping/index.html
'''
import requests
res = requests.get('https://www.ptt.cc/bbs/Gossiping/index.html',verify=False)
#因為有年齡驗證無法取得資訊
print(res.text)

#再點選滿18後我們看到我們要的GET資訊(index.html)的上個資料為一個POST，其實我們點選滿18的時候就是送出一個POST
#這個POST(over18)要輸入的參數(Form Data)有兩個，第一個為from代表要去的地方，第二個為yes代表是否滿18
payload = {
           'from':'/bbs/Gossiping/index.html',
           'yes':'yes'
           }
#由於必須同時用到POST與GET我們必須新增一個session
#session可以用來Provides cookie persistence, connection-pooling, and configuration.
#簡單說就是session是一種跨網頁的變數，如果有變數需要跨網頁使用，你就可以把它存進session變數，然後在其它頁中叫用
#request是接form表單傳過來的值，變數範圍只在單一網頁
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',verify=False,data=payload)
res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html',verify=False)
print(res.text)

#用BeautifulSoup來擷取文章標題、日期與作者
from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text)

for entry in soup.select('.r-ent'):
    print(entry.select('.title')[0].text,entry.select('.date')[0].text,entry.select('.author')[0].text)


'''
[爬蟲實戰] 如何抓取圖表內的價格資訊?

今天我們將示範如何使用Python 的正規表達法(re.search)抓取匯率網站圖表內的價格資訊！
示範網址：https://www.oanda.com/lang/cns/currency/historical-rates/
'''
#網頁生成圖表有兩種方法，第一為Javascript，第二為flash，對圖表按右鍵如果沒有出現flash相關字眼就是用javascript寫的
#我們發現畫圖的javascrip放在histotical-rates/這個GET裡面，從javascript的繪圖語法我們發現在data裡面有繪圖的資料
#因此我們能從這裏面將資料抓出使用
import requests
import re #正則表達式的套件

res = requests.get('https://www.oanda.com/lang/cns/currency/historical-rates/')
#觀察html的page source後我們發現圖表data藏在"data":[[到]]之間的所有資料
m = re.search('("data":\[\[.*\]\])',res.text) #特殊字元前要加\，另外.表示任意字元，*表示0或多個前面的字元，此處表示抓出在"data":[[到]]之間所有資料，正則表達式用()包住，表示匹配括號內的表達式，也表示一個組
m.group(1) #顯示正則表達式第一組(小括號內)的資料
#轉為json格式方便操作，類似python字典
import json
data = json.loads('{'+m.group(1)+'}') #左右用大括號框住就變為典型的json格式
print(data)
data['data'][0][0]
data['data'][0][1]


'''
[爬蟲實戰] 如何簡簡單單突破驗證碼 (Captcha) 限制?

不一定要用OpenCV 做文字辨識才能抓取(Crawl) 網頁資料，有時只要巧妙延續之前做HTTP 請
求的Session，並搭配Ipython Notebook 的圖片顯示功能，半自動化的辨識方式也能讓你輕輕
鬆鬆抓取有驗證碼 (Captcha) 限制的網頁內容。
示範網址:https://fbfh.trade.gov.tw/rich/text/indexfbOL.asp
'''
#首先取得驗證碼圖形 
import requests
#stream=True因為默認情況下，當你進行網絡請求後，響應體會立即被下載。你可以通過 stream 參數覆蓋這個行為，推遲下載響應體直到訪問 Response.content 屬性
res = requests.get('https://fbfh.trade.gov.tw/rich/text/common/code_98/CheckImageCode.aspx',stream=True,verify=False)
#將取得的圖形存入f儲存器的檔名為check.png的檔案中
import shutil
f = open('check.png','wb') #wb表示指定寫入二進位檔案模式
shutil.copyfileobj(res.raw,f)
f.close()
#利用Image印出圖形檔案
from IPython.display import Image
Image('check.png')
#############################################需手動輸入驗證碼
#將圖片的驗證碼輸入textCheckCode中
payload = {
           'queryType':'C',
           'basic_select':'2',
           'chinese_name':'台北',
           'ccc_select':'1',
           'pname_select':'1',
           'textCheckCode':'2pfxf7'        #此為驗證碼
           }
#post也放入session中        
res = requests.post('https://fbfh.trade.gov.tw/rich/text/fbj/asp/fbje140L.asp',data=payload,verify=False)
#結果為亂碼，修改一下encoding
res.encoding = 'utf-8'
print(res.text)

'''
[爬蟲實戰] 如何抓取591租屋網的資訊?

今天要為各位講解當網頁是透過AJAX 換頁時該如何觀察及爬取換頁資訊，同場加映該如何透
過Python 的json 套件讀取json 內容後，將資訊轉換為字典！
示範網址: https://rent.591.com.tw/house-rentSale-1-0-0-0-0.html#list
'''
#網頁換頁請求一般分兩種，一種是在server處理完後吐回來，這種可以在document找到，另一種為
#透過AJAX來換頁可以在XHR找到
#本例我們用Network偵測時換頁可以發現在XHR有東西跑出來，所以此例是用AJAX來換頁
import requests
#我們發現換頁的請求URL裡的firstRow參數決定頁數，目前等於20在第二頁
res = requests.get('https://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=1&orderType=desc&listview=img&shType=list&firstRow=20&totalRows=13353')
print(res.text)
#發現結果為Json格式，所以將結果用Json載入
import json
data = json.loads(res.text)
data.keys() #查看字典的key
data['main']
#擷取商品名稱
from bs4 import BeautifulSoup
soup = BeautifulSoup(data['main'])
for i in range(0,len(soup.select('.house_url'))):
    print(soup.select('.house_url')[i].text)

'''
[爬蟲實戰] 如何透過網路爬蟲將網路圖片存放至SQLite之中?

除了能抓取網路上的文章內容，網路爬蟲也能將美美的圖片放置到資料庫之中歐！本次教學先
將教各位透過設定stream =TRUE，以將網路圖片抓取下來，之後透過shutil 的copyfileobj 
將圖片存放置檔案，接者於建立一個可以存放blob 資料的資料表之中，我們就可以將圖片存放
置資料庫之中了！
'''
import requests
#攫取圖片stream要設為True
response = requests.get('https://blogwww.s3.amazonaws.com/uploads/fgblogphoto/3936/750740.png',stream=True)
print(response) #Response[200] 表示擷取是成功的
#用binary形式存到image.png
import shutil
f = open('image.png','wb')
shutil.copyfileobj(response.raw,f)
f.close()
#讀取image.png這個檔案，存為變數ablob
f = open('image.png','rb')
ablob = f.read()
f.close()
#放入MySQL
import pymysql
import os
#連接數據庫mysql  
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='malex3444',
    db='image',         #指定image資料庫
    charset='utf8',
    local_infile=True
);

cursor = connection.cursor()
#建立資料表  名稱為Photo
sql = '''CREATE TABLE IF NOT EXISTS Photo (
                            id INT NOT NULL AUTO_INCREMENT,
                            img BLOB,
                            PRIMARY KEY(id)
                            )
'''                             
cursor.execute(sql)                             
#存入資料到資料表practice的img欄位
sql = '''INSERT INTO Photo(img) VALUES(%s)'''
cursor.execute(sql,pymysql.Binary(ablob)) #存入的資料轉為SQL的BINARY
#送出執行
connection.commit()
#關閉資料庫
connection.close()



connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='malex3444',
    db='image',
    charset='utf8',
    local_infile=True
);

cursor = connection.cursor()
sql = '''INSERT INTO practice (img) VALUES (%s)'''
cursor.execute(sql,pymysql.Binary(ablob))

sql1='select * from practice'
cursor.execute(sql1)
data=cursor.fetchall()

with open("Output.png", "wb") as output_file:
    cursor.execute(sql1)
    abl = cursor.fetchall()
    output_file.write(abl[1][1])


connection.commit()
connection.close()


'''
[爬蟲實戰] 如何抓取某知名財報網站的資訊 ?

即使針對網站做層層保護，但只要爬取資料的觀念對了，破解任何網站只是時間的問題。如­同
這知名財報網站(https://goo.gl/7Q2v8p)，雖有檢查使用者是否是透過爬蟲爬取資料或有使
用iframe 做頁面內嵌，都還是難逃被爬取的命運！
示範網址:https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid=1101+%E5%8F%B0%E6%B3%A5
'''
import requests
res = requests.get('https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid=1101+%E5%8F%B0%E6%B3%A5')
print(res.text)
#無法存取 因為被redirects，因為可能發現為機器人在讀取資料，因此我們必須偽裝為人
#放入User-Agent
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
res = requests.get('https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid=1101+%E5%8F%B0%E6%B3%A5',headers = headers)
#這邊我們發現網頁有使用iframe 做頁面內嵌，我們透過觀察主要頁面的page source發現了關鍵的自innerHTML 表
#式有用網頁內嵌，我們找到iframe src=字串後面的字加上網頁的domain即可找到資料的來源
import re
m = re.findall('document.getElementById\(\'g\d+\'\).innerHTML=\'<iframe src=\"(.*?)\"' ,res.text) #.*?表示重複任意次，但盡可能少重複
#加入domain
for url in m:
    print('https://www.stockdog.com.tw/stockdog/' + url)
#對其中一個抓取資料
#由於使用到網頁內嵌 可能會依附到主要頁面，所以要用session
rs = requests.session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
res = rs.get('https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid=1101+%E5%8F%B0%E6%B3%A5',headers = headers)
res2 = rs.get('https://www.stockdog.com.tw/stockdog/' + m[0],headers=headers)
print(res2.text)
import re
data = re.findall('data=(.*)\r',res2.text)


'''
[爬蟲實戰] 如何抓取淘寶網的商品名稱與價格 (2016年版)?

為了迎接即將到來的雙十一節，更新一下以前淘寶的爬蟲，造福所有想要在當天掌握價格變化
，殺進殺出的買賣家。舊的爬蟲只要爬取Document 下的連結，便可很容易獲取商品價格資訊。
但淘寶網也在這些時日更新了，變成使用AJAX 的方式填入頁面內容。因此我們便可以從XHR 以
及JS 下手，找尋進入點，再使用正規表達法(re)，便可以快速的剖析出重要資訊，讓你爬取淘
寶網，無往不利！
示範網址:https://world.taobao.com/search/search.htm?_ksTS=1479760032234_41&spm=a21bp.7806943.20151106.1&_input_charset=utf-8&navigator=all&json=on&q=iphone6%E6%89%8B%E6%9C%BA%E5%A3%B3&callback=__jsonp_cb&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895
'''
#現在新式網頁很多會利用AJAX先載入模板再用javascript將資料寫入模板，這樣的網頁資料會落在XHR下，
#但此例XHR下找不到有關掏寶的連結，此時有可能放在JS下，
import requests
res = requests.get('https://world.taobao.com/search/json.htm?navigator=all&q=iphone6%E6%89%8B%E6%A9%9F%E6%AE%BC&spm=a21bp.7806943.20151106.1&_input_charset=utf-8&json=on&nid=&type=&uniqpid=&_ksTS=1479760032234_41&callback=__jsonp_cb')
print(res.text)
#要將資料從js函數中解析出來，
import re
#將js函數去除，發現為json格式
m = re.search('\{__jsonp_cb\((.*)\)\}',res.text)
#將json解析出來
import json
jd = json.loads(m.group(1))
#由於此json十分複雜，因此我們可以將資料先另存成檔案，用chrome開啟，使用preview來看chrome幫我們解析的json格式
with open('a.json','w') as f:
    f.write(json.dumps(jd)) #由於抓格視為python的dic，因此無法直接存成檔案，要先轉為字串(json格式)
    
for item in jd['itemList']:
    print(item['nick'],item['priceWap'])
    
#我們可以將json格式的字串直接讀如DataFrame，自動將商品資料整理成表格
import pandas
df = pandas.DataFrame(jd['itemList'])
df
    
    
'''
[爬蟲實戰] 如何抓取MoneyDJ 文章中的人氣指數?

本教學將教會各位如何使用Python 抓取 MoneyDJ 文章中http://www.moneydj.com/KMDJ/Ne
ws/NewsViewer.aspx?a=a180a15b-9e4f-4575-b28f-927fcb5c63a3 的人氣指數。 如果想要安
裝POSTMAN 的，請到以下網站下載 https://chrome.google.com/webstore/detail/postman-rest-client-packa/fhbjgbiflinjbdggehcddcbncdddomop   
'''
#我們發現人氣指數，一開始為一個數字，之後突然跳成另一個數字，因為這裡也用到AJAX，一開始先隨便
#丟一個數字，再用JS來更新，因此我們知道檔案可能在XHR中
import requests
from bs4 import BeautifulSoup
url = 'http://www.moneydj.com/InfoSvc/apis/vc'
payload = '{"counts":[{"svc":"NV","guid":"a180a15b-9e4f-4575-b28f-927fcb5c63a3"}]}' #用source方式輸入要用字串形式
head = {'Content-Type':'application/json'}
res = requests.post(url,data = payload,headers=head)
print(res.text)



'''
[爬蟲實戰] 如何使用Selenium IDE 記錄抓取包含Iframe 頁面資訊的步驟 - 以司法院法學檢
索系統為例

如果要抓取司法院法學檢索系統的檢索內容，通常會碰到因為該查詢結果是鑲嵌在Iframe 中，
以致爬蟲無法順利抓取內容。這時就可以使用Selenium 解決抓取的問題。但是該如何寫一個
Selenium程式呢? 這時候可以靠Selenium IDE 的幫忙，自動記錄抓取步驟後，並將步驟轉換成
Python Script，讓一切爬取動作變得不可能再簡單！
'''
##############################to be continued............










'''
[爬蟲實戰] 如何使用 PANDAS 快速爬取財報表格?

表格是網路上常見擺放數據的格式，除了可以使用BeautifulSoup4做數據的剖析外，最佳能將該
資料格式爬取下來的工具可能莫過於PANDAS 莫屬，只要透過簡單的read_html，就可以把網路上
看來複雜的表格資訊，快速轉變成DataFrame，納為股票分析的數據源之一！
網站下載: http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_1101.djhtm
'''

import pandas

url = 'http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_1101.djhtm'
df = pandas.read_html(url)
##############################to be continued............





'''
[爬蟲實戰] 如何使用 Selenium 以及 Python 輕鬆抓取 Agoda 的旅館資訊?

抓取以Ajax 生成的頁面需要許多時間耐心觀察，才能找到抓取的切入點。但是使用Selenium 
可以省去這個麻煩，他的自動點擊跟載入Ajax生成的頁面結果，讓人只消知道元素所在便可抓
取資訊，再搭配BeautifulSoup4 強大的解析功能，用Python 抓取網頁，再簡單不過！

'''
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time 
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

browser = webdriver.Firefox(executable_path=r'D:\程式\python\PythonCrawler\WebDriver\FireFoxWebDriver\geckodriver.exe')


browser.get('http://news.baidu.com/')
browser.find_element_by_xpath(u"(//a[contains(text(),'财经')])[3]").click()
browser.close()

##############################to be continued............

 

'''
[爬蟲實戰] 如何抓取心食譜的食譜資訊?

今天要示範如何使用CSS Selector 的nth-of-type 抓取特定位置的食譜資訊。示範網頁於下列URL: http://goo.gl/TgEr3l

'''
import requests
from bs4 import BeautifulSoup
res = requests.get('https://www.xinshipu.com/zuofa/49391')
soup = BeautifulSoup(res.text,"html.parser")
reup = soup.select('.re-up')

##############################to be continued............



'''
[爬蟲實戰 ]如何模擬用戶代理 (User Agent) 成功存取目標網頁內容 (以永慶房屋為例)?
有的網頁伺服器，會透過檢查用戶代理(User Agent)，以限制爬蟲存取頁面內容，此時我們只要在
標頭上增加自身瀏覽器所使用的用戶代理(User Agent) 就可成功騙過對方伺服器，存取網頁內容！
我們便能使用這技術成功抓取永慶房屋的房價資訊瞜！    
'''
import requests 
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
res = requests.get('https://buy.yungching.com.tw/region', headers = head)
print(res.text)

#f = open('res.text','w', encoding='utf-8')
#f.write(res.text)
#f.close()


'''
[爬蟲實戰] 如何爬取PTT的網頁?
本次實戰將教您如何從PTT 的Food版(https://www.ptt.cc/bbs/Food/index.html)v抓取鄉民寶貴的言論，
以利之後做美食的文字探勘分析！
'''
import requests 
from bs4 import BeautifulSoup
res = requests.get('https://www.ptt.cc/bbs/Food/index.html', verify = False)
soup = BeautifulSoup(res.text)

for entry in soup.select('.r-ent'):
    print( entry.select('.title')[0].text, entry.select('.author')[0].text, entry.select('.date')[0].text )
    

'''
[爬蟲實戰] 如何告訴PTT我已滿18並順利抓取八卦版的文章 ?
雖然已滿18歲多年，但是不知道你實際年齡的PTT，還是要禮貌性的問你是否滿18後­，
才能讓你閱讀八卦版裡面的內容，但人可以做點選，爬蟲呢？於是我們便可以先透過Ch­rome開發人員工具
快速找到如何使用POST方法通過18歲驗證後，再接續之前的S­ession，就能順利存取八卦版的內容！
'''
import requests 
from bs4 import BeautifulSoup

payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'}

rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18', verify = False, data = payload)
res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html', verify = False)
soup = BeautifulSoup(res.text)

for entry in soup.select('.r-ent'):
    print( entry.select('.title')[0].text, entry.select('.author')[0].text, entry.select('.date')[0].text)


'''
[爬蟲實戰] 如何抓取圖表內的價格資訊?
今天我們將示範如何使用Python 的正規表達法(re.search)抓取匯率網站圖表內的價格資訊！
示範網址如下：http://goo.gl/rrq67Z
'''
import requests
import re
import json
res = requests.get('https://www.oanda.com/fx-for-business/historical-rates/api/initialize?source=OANDA&adjustment=0&base_currency=USD&start_date=2018-9-28&end_date=2018-10-28&period=daily&price=bid&view=graph&quote_currency_0=EUR&quote_currency_1=&quote_currency_2=&quote_currency_3=&quote_currency_4=&quote_currency_5=&quote_currency_6=&quote_currency_7=&quote_currency_8=&quote_currency_9=&_=1540719772737')
m = re.search('("data": \[\[.*\]\])',res.text)
data = json.loads('{'+ m.group(0) +'}')
print(data)

'''
[爬蟲實戰] 如何簡簡單單突破驗證碼 (Captcha) 限制?
不一定要用OpenCV 做文字辨識才能抓取(Crawl) 網頁資料，
有時只要巧妙延續之前做HTTP 請求的Session，並搭配Ipython Notebook
 的圖片顯示功能，半自動化的辨識方式也能讓你輕輕鬆鬆抓取有驗證碼 (Captcha) 限制的網頁內容。
'''
###法一
import requests 
import shutil

rs = requests.session()

###法一 Stream = True 
res = rs.get('https://fbfh.trade.gov.tw/rich/text/common/code_98/CheckImageCode.aspx', stream = True, verify = False)
f = open('check.png', 'wb')
shutil.copyfileobj(res.raw, f)
f.close()

from IPython.display import Image
Image('check.png')

###法二 Stream = False
#res = rs.get('https://fbfh.trade.gov.tw/rich/text/common/code_98/CheckImageCode.aspx', stream = False, verify = False)
#f = open('check.png', 'wb')
#f.write(res.content)
#f.close()
#
#from IPython.display import Image
#Image('check.png')


payload = {'queryType': 'C',
            'basic_select':' 2',
            'chinese_name': '台中',
            'ccc_select': '1',
            'ccc_num': '8',
            'pname_select': '1',
            'txtCheckCode': 'beprte'
            }
            
res = rs.post('https://fbfh.trade.gov.tw/rich/text/fbj/asp/fbje140L.asp', data = payload, verify = False )
res.encoding = 'utf-8'
print(res.text)

###法二  藉由打完驗證碼進入後，選取第二頁資料，發現不需要驗證碼，所以有另一個伺服器位置可以直接利用URL來Get資料
res = requests.get('https://fbfh.trade.gov.tw/rich/text/fbj/asp/fbje140L.asp?ScrollAction=Page1&basic_select=2&uni_number=&chinese_name=%E5%8F%B0%E4%B8%AD&english_name=&owner=&ccc_select=1&ccc_num=8&product=&pname_select=1&product_name=&newPage=Y')
res.encoding = 'utf-8'
print(res.text)


'''
[爬蟲實戰] 如何抓取591租屋網的資訊?
今天要為各位講解當網頁是透過AJAX 換頁時該如何觀察及爬取換頁資訊，
同場加映該如何透過Python 的json 套件讀取json 內容後，將資訊轉換為字典！
'''
import requests 
import json
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
res = requests.get('https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=1&firstRow=90&totalRows=10594', headers = head)
data = json.loads(res.text)
print(data.keys()) #列出Json裡面的所有Keys
data['data']
print(data['data'].keys())
data['data']['data']
data['data']['data'][0]
data['data']['data'][0]['price']

for i in range(1,20,1):
   print(data['data']['data'][i]['price'])


'''
[爬蟲實戰] 如何透過網路爬蟲將網路圖片存放至SQLite之中?
除了能抓取網路上的文章內容，網路爬蟲也能將美美的圖片放置到資料庫之中歐！
本次教學先將教各位透過設定stream =TRUE，以將網路圖片抓取下來，之後透過shutil 的copyfileobj 將圖片存放置檔案
，接者於建立一個可以存放blob 資料的資料表之中，我們就可以將圖片存放置資料庫之中了！
'''
import requests
import shutil
import os
from sqlalchemy import create_engine

res = requests.get('https://blogwww.s3.amazonaws.com/uploads/fgblogphoto/3936/750740.png', stream = True)

f = open('Image.png', 'wb')
shutil.copyfileobj(res.raw,f)
f.close()

f = open('Image.png', 'rb')
ablob = f.read()
f.close()

PicEngine = create_engine("mysql+mysqldb://{}:{}@{}/{}?charset=utf8mb4".format('root', 'malex3444', '127.0.0.1', 'test'))
PicConnection = PicEngine.connect()

PicConnection.execute("CREATE TABLE justatest(name TEXT, ablob BLOB)")
sql = "INSERT INTO justatest VALUES(%s, %s)"    
PicConnection.execute(sql,('Pic_1',ablob))

PicConnection.close()



'''
[爬蟲實戰] 如何抓取淘寶網雙十一購物狂歡節活動網頁中的商品列表?
又來到購物血拼的雙十一購物狂歡節了，雖然淘寶 (Taobao) 前一次的網頁改版，讓抓取資料開始變的棘手
，但檔不了我們或取購物資訊的熱情！這次，就是要敎你如何用Python 網路爬蟲 (Python Crawler)將雙十一購物
狂歡節活動網頁中的商品列表抓取下來。
'''

##############################to be continued............


'''
[爬蟲實戰] 如何抓取淘寶網的商品名稱與價格 (2016年版)?
為了迎接即將到來的雙十一節，更新一下以前淘寶的爬蟲，造福所有想要在當天掌握價格變化，殺進殺出的買賣家。
舊的爬蟲只要爬取Document 下的連結，便可很容易獲取商品價格資訊。但淘寶網也在這些時日更新了，變成使用AJAX
 的方式填入頁面內容。因此我們便可以從XHR 以及JS 下手，找尋進入點，再使用正規表達法(re)，便可以快速的剖析出重
 要資訊，讓你爬取淘寶網，無往不利！
'''

##############################to be continued............


'''
[爬蟲實戰] 如何抓取某知名財報網站的資訊 ?
即使針對網站做層層保護，但只要爬取資料的觀念對了，破解任何網站只是時間的問題。
如­同這知名財報網站(https://goo.gl/7Q2v8p)，雖有檢查使用者是否是透過爬蟲爬取資料或有使用iframe 
做頁面內嵌，都還是難逃被爬取的命運！
'''
import requests 
import re
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

rs = requests.session()
res = rs.get('https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid=1101+%E5%8F%B0%E6%B3%A5', headers = headers)
m = re.findall('document.getElementById\(\'g\d+\'\).innerHTML=\'<iframe src=\"(.*?)\"',res.text)

res2 = rs.get('https://www.stockdog.com.tw/stockdog/'+m[1], headers = headers)
print(res2.text)


'''
[爬蟲實戰] 如何抓取MoneyDJ 文章中的人氣指數?
本教學將教會各位如何使用Python 抓取 MoneyDJ 文章中http://www.moneydj.com/KMDJ/News/NewsViewer.aspx?a=a180a15b-9e4f-4575-b28f-927fcb5c63a3 
的人氣指數。 如果想要安裝POSTMAN 的，請到以下網站下載 https://chrome.google.com/webstore/detail/postman-rest-client-packa/fhbjgbiflinjbdggehcddcbncdddomop
'''
import requests 
from bs4 import BeautifulSoup
url = 'https://www.moneydj.com/InfoSvc/apis/vc'
payload = '{"counts":[{"svc":"NV","guid":"a180a15b-9e4f-4575-b28f-927fcb5c63a3"}]}'
head = {'Content-Type':'application/json'}
res = requests.post(url, data = payload, headers = head)
res.text

import json
data = json.loads(res.text)
data['counts'][0]['count']


'''
[爬蟲實戰] 如何使用Selenium IDE 記錄抓取包含Iframe 頁面資訊的步驟 - 以司法院法學檢索系統為例
如果要抓取司法院法學檢索系統的檢索內容，通常會碰到因為該查詢結果是鑲嵌在
Iframe 中，以致爬蟲無法順利抓取內容。這時就可以使用Selenium 解決抓取
的問題。但是該如何寫一個Selenium程式呢? 這時候可以靠Selenium IDE 的幫忙，自動記錄抓取步驟後，
並將步驟轉換成Python Script，讓一切爬取動作變得不可能再簡單！
'''
##############################to be continued............




'''
[爬蟲實戰] 如何透過Selenium 自動將頁面捲動至最下方抓取資料?
當碰到瀑布流網站(例如: EZTABLE)，抓取資訊就會變得比較困難。但所幸可
以使用Selenium 執行Javascript 來解決頁面捲動的問題，在本範例中，
我們利用execute_script 執行 window.scrollTo(0, document.body.scrollHeight);
，便可順利抓取瀑布流式網頁。
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#options = webdriver.ChromeOptions()
#options.add_argument('user-agent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
#driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')# 第一個參數為webdriver位置，第二個參數可以設定headers
driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
driver.implicitly_wait(3) 
driver.get('https://tw.eztable.com/search?country=tw&date=2018-11-11&people=2')

for i in range(1,10):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1) # Let the user actually see something!
    
soup = BeautifulSoup(driver.page_source)

for block in soup.select('.sc-kLIISr.hkDUyW'):
    print(block.text)

driver.quit()


'''
[爬蟲實戰] 如何抓取集保戶股權分散表?
雖然我們可以使用requests.post 取得需要POST請求的網頁內容，但我們也可巧妙的使用GET
 模擬整個的POST 動作，只需要簡單的將POST 內容編碼後，串接在原網址的問號(?)後面，
 便可以順利取得裡面的內容。
'''
import requests
from bs4 import BeautifulSoup

#Method1
res = requests.get('https://www.tdcc.com.tw/smWeb/QryStockAjax.do?scaDates=20181109&scaDate=20181109&SqlMethod=StockNo&StockNo=2330&radioStockNo=2330&StockName=&REQ_OPR=SELECT&clkStockNo=2330&clkStockName=')
soup = BeautifulSoup(res.text)
##############################失效............

#Method2
payload = {
        'scaDates': '20181109',
        'scaDate': '20181109',
        'SqlMethod':' StockNo',
        'StockNo': '2330',
        'radioStockNo': '2330',
        'REQ_OPR': 'SELECT',
        'clkStockNo': '2330'
        }

res = requests.post('https://www.tdcc.com.tw/smWeb/QryStockAjax.do', data = payload)
soup = BeautifulSoup(res.text, 'lxml')
tb = soup.select('.mt')[1]

for tr in tb.select('tr'):
    print(tr.select('td')[0].text, tr.select('td')[1].text, tr.select('td')[2].text,
          tr.select('td')[3].text, tr.select('td')[4].text)


'''
[爬蟲實戰] 如何抓取廉價航空的機票價格 – 以酷航為例?
要能搶的到便宜的廉價航空機票最佳妙方，便是無時無刻關注最新的票價。但上班很忙、上課很累，
所以我們還是讓我們的爬蟲代勞吧。因此我們就教大家如何使用爬蟲 (Python Crawler) 抓取酷
航(http://www.flyscoot.com/)的最新票價資訊，讓你不再錯失便宜的機票。
'''

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time 

payload = {
        'revAvailabilitySearch.SearchInfo.AdultCount':' 1',
'revAvailabilitySearch.SearchInfo.ChildrenCount':' 0',
'revAvailabilitySearch.SearchInfo.InfantCount':' 0',
'revAvailabilitySearch.SearchInfo.Direction':' Return',
'revAvailabilitySearch.SearchInfo.PromoCode':' ',
'revAvailabilitySearch.SearchInfo.SalesCode':' ',
'revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureStationCode':' TPE',
'revAvailabilitySearch.SearchInfo.SearchStations[0].ArrivalStationCode':' CTS',
'revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureDate':' 11/17/2018',
'revAvailabilitySearch.SearchInfo.SearchStations[1].DepartureStationCode':' CTS',
'revAvailabilitySearch.SearchInfo.SearchStations[1].ArrivalStationCode':' TPE',
'revAvailabilitySearch.SearchInfo.SearchStations[1].DepartureDate':' 12/13/2018',
'revAvailabilitySearch.DeepLink.OrganisationCode':' ',
'revAvailabilitySearch.DeepLink.Locale':' '
        }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

rs = requests.session()

res = rs.post('https://makeabooking.flyscoot.com/Book/?culture=zh-tw', data = payload)
res2 = rs.get('https://makeabooking.flyscoot.com/Book/Flight', headers = headers)

print(res2.text)

##############################失效............


'''
[爬蟲實戰] 如何撰寫Python爬蟲
抓取台灣銀行的牌告匯率?
想知道何時能買進最低價位的日圓嗎? 使用爬蟲通知你就對了！今天我們會使用Python Pandas，
極快速的將台灣銀行的牌告匯率抓取下來，並使用Pandas 的語法將匯率資料整理成漂亮的表格。
最後，我們便能將整理過的資料存成Excel。讓你出國血拼，硬是划算！
'''
import os
import pandas 
os.chdir('C:\\Users\\SUNG ANN LEE\\Desktop')

dfs = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')
len(dfs)
currency = dfs[0]
currency = currency.iloc[:,0:5]
currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'即期匯率-本行買入',u'即期匯率-本還賣出']  #設定中文字元在python最好前面加u表示以unicode編碼儲存，匯出資料較不會出現亂碼
currency[u'幣別']
currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')

currency.to_excel('currency.xlsx')


'''
[爬蟲實戰] 如何使用 Selenium 以及 Python 輕鬆抓取 Agoda 的旅館資訊?
抓取以Ajax 生成的頁面需要許多時間耐心觀察，才能找到抓取的切入點。但是使用Selenium 
可以省去這個麻煩，他的自動點擊跟載入Ajax生成的頁面結果，讓人只消知道元素所在便可抓取
資訊，再搭配BeautifulSoup4 強大的解析功能，用Python 抓取網頁，再簡單不過！
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
driver.implicitly_wait(3) 
driver.get("https://www.agoda.com/zh-tw/pages/agoda/default/DestinationSearchResult.aspx?asq=5YR5PTQcb%2BN%2FePzblV4MBFsWbJBVegk7h53XMJQU8Ug3%2BCniEAZEfNAKflO8X37BgB1k7is3d6aCoAzASPwcvmik1sC%2B%2Bkx3SmVVT0JMgCvEN%2B3HN55QPiV4QqZ9Hr9V%2FhCfGh1fe8fw7emVE5OPejlypi9OrtU69rexWvGwtn6KStI%2FdzHjvXk0Bhe3Qwyp8uPa9VTdgPhaGCgz6iRjMg%3D%3D&city=14690&cid=-347&tick=636775526440&languageId=20&userId=8fecae28-01b0-47b9-afde-661d312ed3c5&sessionId=1bqk0c14skx1lmti0ucjjp2q&pageTypeId=1&origin=TW&locale=zh-TW&aid=130589&currencyCode=KRW&htmlLanguage=zh-tw&cultureInfoName=zh-TW&ckuid=8fecae28-01b0-47b9-afde-661d312ed3c5&prid=0&checkIn=2018-11-20&checkOut=2018-12-05&rooms=1&adults=2&children=0&priceCur=KRW&los=15&textToSearch=%E9%A6%96%E7%88%BE&sort=agodaRecommended")
for i in range(18):
    driver.execute_script('window.scrollBy(0,1000)')
    time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')

while len(soup.select('.btn.pagination2__next')) > 0:
    for ele in soup.select('.hotel-name'):
        print(ele.text)
    driver.refresh()
    driver.find_element_by_id("paginationNext").click()
    for i in range(20):
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
driver.close()


'''
[爬蟲實戰] 如何使用 PANDAS 快速爬取財報表格?
表格是網路上常見擺放數據的格式，除了可以使用BeautifulSoup4做數據的剖析外，最佳能將
該資料格式爬取下來的工具可能莫過於PANDAS 莫屬，只要透過簡單的read_html，就可以把網
路上看來複雜的表格資訊，快速轉變成DataFrame，納為股票分析的數據源之一！
'''
import pandas as pd
#營收盈餘
df = pd.read_html('http://jsjustweb.jihsun.com.tw/z/zc/zch/zch_1101.djhtm')
df = df[2]
df = df.iloc[5:,:]
df.columns = df.iloc[0,:]
df.index = df.iloc[:,0]
data = df.iloc[1:,1:]

#綜合損益表
df = pd.read_html('http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_1101.djhtm')
df = df[2]
df.columns = df.iloc[1,:]
df.index = df.iloc[:,0]
data = df.iloc[3:,1:]

#財務比率季表
df = pd.read_html('http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr_2330.djhtm')
df = df[2]
df.columns = df.iloc[2,:]
df.index = df.iloc[:,0]
data = df.iloc[4:,1:]

cond = ['指標','種類','期別','其他單位']
data = data[[any(word in index for word in cond) == False for index  in data.index]]


'''
[爬蟲實戰] 如何使用Selenium 抓取驗證碼?
用Python Requests 擷取驗證碼圖片不是件難事，但用selenium呢? 最簡單的做法就是先
存下頁面快照(screenshot)，再找尋圖片位置後，根據位置還有圖片大小，我們就可以從頁
面中順利擷取出驗證碼，之後只要把驗證碼丟到我們的機器學習引擎辨認，以後就可以讓電
腦自動幫我們訂票啦！ 
程式碼: https://github.com/ywchiu/largitdata/blob/master/code/Course_95.ipynb
'''
from selenium import webdriver
import os 
import numpy as np
os.chdir('C:\\Users\\SUNG ANN LEE\\Desktop')

Width = np.int(1519.2) 
Hight = np.int(1118.47) 

#driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
driver = webdriver.Firefox(executable_path=r'D:\程式\python\PythonCrawler\WebDriver\FireFoxWebDriver\geckodriver.exe')
driver.get('https://irs.thsrc.com.tw/IMINT/') #如果要躲避SSL驗證，可以將https改為http
driver.set_window_size(Width,Hight)
driver.save_screenshot('code.png')

element = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')
element.location
element.size
left = element.location['x']
right = element.location['x'] + element.size['width']*1.2
top = element.location['y']
bottom = element.location['y'] + element.size['height']*1.2

from PIL import Image
img = Image.open('code.png',)
img = img.resize((Width,Hight), Image.ANTIALIAS)
img = img.crop((int(left),int(top),int(right),int(bottom)))
img.show()
img.save('captcha.png')


driver.close()
##############################擷取圖片位置與網頁位置不同............


'''
[爬蟲實戰] 如何破解高鐵驗證碼 (1) - 去除圖片噪音點?
進到高鐵驗證碼破解系列！今天先從去除驗證碼上的噪音點開始。首先我們要安裝opencv，接者便
可以使用opencv 中的 fastNlMeansDenoisingColored (https://docs.opencv.org/3.0-beta/modules/photo/doc/denoising.html) 
去除圖片中的的噪音點，讓驗證碼圖變得更加乾淨！ 
程式碼: https://github.com/ywchiu/largitdata/blob/master/code/Course_96.ipynb
'''
'''
OpenCV提供了这种技术的四种变体。

cv2.fastNlMeansDenoising（） - 使用单个灰度图像
cv2.fastNlMeansDenoisingColored（） - 使用彩色图像。
cv2.fastNlMeansDenoisingMulti（） - 用于在短时间内捕获的图像序列（灰度图像）
cv2.fastNlMeansDenoisingColoredMulti（） - 与上面相同，但用于彩色图像。
Common arguments:

h：参数决定滤波器强度。较高的h值可以更好地消除噪声，但也会删除图像的细节 (10 is ok)
hForColorComponents：与h相同，但仅适用于彩色图像。 （通常与h相同）
templateWindowSize：应该是奇数。 （recommended 7）
searchWindowSize：应该是奇数。 （recommended 21）
'''

from PIL import Image
import cv2
import os 
os.chdir('D:\\程式\\python\\Python Crawler\\Practice\\Data')
Image.open('captcha.png')

img = cv2.imread('captcha.png')

dst = cv2.fastNlMeansDenoisingColored(img, None, 20, 20, 7, 21) 

import matplotlib.pyplot as plt
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(dst)

plt.show()

'''
[爬蟲實戰] 如何破解高鐵驗證碼 (2) - 使用迴歸方法去除多餘弧線?
在去除掉腦人的噪音點後，如何該去除掉跟字一樣粗的弧線便是大問題。所幸，所有高鐵驗證碼的弧
線都可以簡單的用一個二項式迴歸公式表示，因此我們便可以用sklearn 的linear model去適配出
迴歸線後，便可以擦去這條煩人的弧線，提高圖片的可辨識率！ 
程式碼: https://github.com/ywchiu/largitdata/blob/master/code/Course_97.ipynb
'''
import os 
os.chdir('D:\\程式\\python\\Python Crawler\\Practice\\Data')

from PIL import Image
Image.open('captcha.png')
import cv2 
img = cv2.imread('captcha.png')
dst = cv2.fastNlMeansDenoisingColored(img, None, 20, 20, 7 ,21)

import matplotlib.pyplot as plt
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(dst)
plt.show()

ret, thresh = cv2.threshold(dst,127,255,cv2.THRESH_BINARY_INV) #黑色0  白色255  灰色 127
plt.imshow (thresh)

imgarr = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
imgarr.shape

imgarr[:,25:138] = 0   #挖空中間的部分
plt.imshow(imgarr)
imgarr = imgarr[:,15:]  
plt.imshow(imgarr)

import numpy as np
imagedata = np.where(imgarr == 255) #找出我們要的線段位置

#imagedata[1]為Y軸   imagedata[1]為X軸
plt.scatter(imagedata[1], imagedata[0], s = 100, c = 'red', label = 'Cluster 1')
#改為左下到右上
imgarr.shape
plt.scatter(imagedata[1], imgarr.shape[0] - imagedata[0], s = 100, c = 'red', label = 'Cluster 1')
plt.ylim(ymin = 0)
plt.ylim(ymax = imgarr.shape[0])
plt.show()

X = np.array([imagedata[1]])
Y = imgarr.shape[0] - imagedata[0]

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

poly_reg = PolynomialFeatures(degree = 2)
X_ = poly_reg.fit_transform(X.T)
regr = LinearRegression()
regr.fit(X_, Y) #找到這條回歸線

X2 = np.array([[i for i in range(0,imgarr.shape[1])]])
X2_ = poly_reg.fit_transform(X2.T)

plt.scatter(X, Y, color = 'black')
plt.ylim(ymin = 0)
plt.ylim(ymax = imgarr.shape[0])
plt.plot(X2.T, regr.predict(X2_), color = 'blue', linewidth = 20)

newing = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
for ele in np.column_stack([regr.predict(X2_).round(0),X2[0]]):
    pos = imgarr.shape[0] - int(ele[0])
    newing[pos:pos+6, int(ele[1])] = 255 - newing[pos:pos+6, int(ele[1])] 

import matplotlib.pyplot as plt 
plt.subplot(121)
plt.imshow(thresh)
plt.subplot(122)
plt.imshow(newing)


newing = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
for ele in np.column_stack([regr.predict(X2_).round(0),X2[0]]):
    pos = imgarr.shape[0] - int(ele[0])
    newing[pos:pos+8, int(ele[1])] = 0

import matplotlib.pyplot as plt 
plt.subplot(121)
plt.imshow(thresh)
plt.subplot(122)
plt.imshow(newing)



'''
[爬蟲實戰] 如何極速擷取1111購物狂歡節的特價商品資訊?
又來到1111 購物狂歡的季節，除了要瘋狂的Shopping 以外，千萬別忘了用Pyhton 網路爬蟲關
注重要的特價訊息! 這次我們將用簡單的爬蟲，抓取天貓主會場的特價商品資料！先用python
 requests 抓取商品頁面，接者用BeautifulSoup4 抓取位在　.J_dynamic_data　的資料區塊
 ，最後用簡簡單單的json.loads，便可以將資料讀成字典結構，讓妳敗家當下，同時顧好荷包！
 程式碼：https://github.com/ywchiu/largitdata/blob/master/code/Course_80.ipynb
'''
import requests 
from bs4 import BeautifulSoup
import json
 
res = requests.get('https://pages.tmall.com/wow/tmall-3c/20991/sjsm?wh_biz=tm&pos=1&acm=201709142.1003.2.4616129&scm=1003.2.201709142.OTHER_1541294992340_4616129')
soup = BeautifulSoup(res.text, 'html.parser')
type(soup.select('.J_dynamic_data'))

jd = json.loads(soup.select('.J_dynamic_data')[0].text)
for item in jd['list']:
    print( item['itemActPrice'], item['itemTitle'], item['itemDesc'], '\n')

 
'''
[爬蟲實戰] 如何使用Pandas 函式將台灣銀行的牌告匯率存進資料庫中?
將抓取到的牌告匯率存進Excel之中是個保存資料的好方法，但使用者卻很難使用Excel管理新增
的匯率資料。因此，比較好的做法是我們可以將資料庫當成儲存媒介，增加資料的可維護性。而
使用Pandas，只需要在建立與資料庫(SQLite)的連線後，利用 to_sql 函式，即可瞬間將資料
儲存進資料庫中。之後，只要再使用read_sql_query，便可將資料庫中的資料讀回變成 DataFrame。
'''
import os
import pandas 
os.chdir('C:\\Users\\SUNG ANN LEE\\Desktop')

dfs = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')
len(dfs)
currency = dfs[0]
currency = currency.iloc[:,0:5]
currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'即期匯率-本行買入',u'即期匯率-本還賣出']  #設定中文字元在python最好前面加u表示以unicode編碼儲存，匯出資料較不會出現亂碼
currency[u'幣別']
currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')

from datetime import datetime
currency['Date'] = datetime.now().strftime('%Y-%m-%d')
currency.info()
currency['Date'] = pandas.to_datetime(currency['Date'])
currency.info()

from sqlalchemy import create_engine
Engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format('root', 'malex3444', '127.0.0.1', 'test'))
Connection = Engine.connect()

currency.to_sql('currency', con = Connection, if_exists = 'append')
df = pandas.read_sql_query('select * from currency', con = Connection )

Connection.close()


'''
[爬蟲實戰] 如何設定工作排程自動將牌告匯率存進資料庫之中?
讓爬蟲每天定期執行爬取工作才能達成真正的工作自動化！而Windows 使用者可以善用工作排
程器功能，我們便可以每天更新資料庫的匯率資料，以利之後進一步提醒我們現在是否是進場的
好時機！ 如果是MAC 或 Linux 使用者，可以參考Crontab 的用法歐 
(http://linux.vbird.org/linux_basic/0430cron.php) 
'''
##############################使用windows工作排程器操作............






'''
[爬蟲實戰] 如何突破蝦皮拍賣的重重限制以順利抓取拍賣商品資訊?
又回到爬蟲實戰的課題了，這次要抓時下最夯的蝦皮拍賣(https://shopee.tw/)。蝦皮的抓取
\方法必須先找到放在XHR 的請求連結，接下來必須連同json 格式的參數一同透過POST做傳輸
，方能送出正確的請求出去。但是如果今天發出請求後，如何都拿不到正確回應時，便要思考是
不是有少帶哪些標頭(Headers)資訊，此時只要一一嘗試，總會找到一個正確的組合取得商品資
訊。當然，有些標頭資訊是很難以取得的，此時再搭配Selenium 取得正確Cookie，任何難解的
網站都可以迎刃而解!
'''

import requests
from selenium import webdriver
driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
driver.get('https://shopee.tw')

driver.get_cookies()
cookies = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()])

headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'cookie':cookies
         }
res = requests.get('https://shopee.tw/api/v2/search_items/?by=pop&limit=50&match_id=63&newest=0&order=desc&page_type=search', headers = headers)
res.text

import pandas as pd 
df = pd.DataFrame(res.json()['items'])
df



'''
[爬蟲實戰] 如何使用Python Pandas 分析比特幣最佳買點?
比特幣(Bitcoin)與以太幣(Ethereum)大漲的故事，似乎在投資界升起一股虛擬貨幣投資浪潮，
但看著日益上漲的的比特幣，你是不是會擔心高點到了，始終買不下手，遲遲無法進場? 這時我
們可以利用Python 網路爬蟲加上Python Pandas 的數據分析功能，協助你找出比特幣的趨勢線
與移動平均線，讓你可以用傳統的均線理論，趨吉避凶，找出最適當的買點！當然，老話一句，
投資有賺有賠，投資前請詳閱公開說明書 XD 
程式碼: https://github.com/ywchiu/largitdata/blob/master/code/Course_90.ipynb 
想了解更多該如何使用Python 做資料分析?
 可以參考我跟天善智能合作的線上課程: https://edu.hellobi.com/course/159
'''
import requests
res = requests.get('https://www.coingecko.com/price_charts/1/usd/max.json?locale=zh-tw')
res.text

import re
m = re.search('{"stats":(.*?),"total_volumes":', res.text)
import json
jd = json.loads(m.group(1))

import pandas as pd 
df = pd.DataFrame(jd)
df.columns = ['datetime','twd']
df.head()
df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms')
df.head()
df.tail()
df.index = df['datetime']
df.head()

df.plot(x='datetime', y='twd', kind='line', figsize=[10,5])
df['ma7'] = df['twd'].rolling(window=7).mean()
df.head(10)

df[['twd','ma7']].plot(kind='line', figsize=[20,5])

df2 = df[df['datetime'] >= '2018-01-01']
df2.head()
df2[['twd','ma7']].plot(kind='line', figsize=[20,5])


'''
[爬蟲實戰] 如何透過EMAIL即時獲取最新匯率資訊?
當已經能夠設定自動排程，每天定期抓取匯率資訊後，我們便想知道如果今天匯率觸擊我們心目
中的價格，是否可以讓爬蟲透過EMAIL自動通知我們? 因此我們可以使用Python 的smtplib 結
合 GMAIL，再將Data Frame 的資料以HTML 的方式寄出，我們便可以將整個匯率擷取過程全部
用Python 爬蟲自動化，讓你不再錯失任何最佳買點！
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PASWORD = 'malex3444'  #'fininfoscitech@gmail.com'的密碼

fromaddr = 'fininfoscitech@gmail.com'
toaddr = 'a77689466@hotmail.com'

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = '[匯率觸價通知]'

#讀入SQL資料
import pandas
from sqlalchemy import create_engine
Engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format('root', 'malex3444', '127.0.0.1', 'test'))
Connection = Engine.connect()

sql = r'select * from currency'
df = pandas.read_sql_query(sql, con = Connection )
Connection.close()

df = df.sort_values('Date')
df = df[df['幣別'] == 'JPY']


body = df.to_html()
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587) #寄出郵件帳號的server
server.starttls() #傳輸層安全性協定（英語：Transport Layer Security，縮寫作TLS）
server.login(fromaddr, PASWORD)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()


'''
[爬蟲實戰] 如何使用Pandas 快速繪製日幣近期的匯率走勢?
談到資料分析，圖表一定是其中不可或缺的一環，而透過Pandas 的處理，你會發現原來畫圖不過就
是兩三行指令的事。在這邊我們先善用pandas 的 read_csv 讀取 csv 資料，再用%pylab inline
讓圖表成現在Jupyter Notebook 之中，最後使用 plot函式繪製折線圖。畫圖，就是這麼簡單！
'''
import pandas as pd
df = pd.read_csv('https://rate.bot.com.tw/xrt/flcsv/0/l6m/JPY')
df.info()
#轉換index成datetime
df.index = pd.to_datetime(df.index, format='%Y%m%d')
df.info()

df.plot(kind='line', y=['匯率','現金'], figsize=[10,5])


'''
[爬蟲實戰] 如何爬取圖片以建立慾望之牆?
除了可以使用網路爬蟲(Web Crawler)抓取文字資料外，我們當然也可以利用爬蟲抓取圖片檔。因此
想要把最喜­愛的雪芙女神照片蒐集成美女牆(慾望之牆?)，我們只須找到圖片的位置後，結合使用
s­treaming 的資料抓取, binary 寫檔跟shutil套件。我們便可以把
Gamebase(http://goo.gl/oOwFme)上雪芙女神相關的照片變成我們的收藏品。Hi 雪芙，妳好嗎!
'''

import requests
from bs4 import BeautifulSoup
import shutil
import os
os.chdir('C:\\Users\\SUNG ANN LEE\\desktop')

res = requests.get('http://www.gamebase.com.tw/forum/64172/topic/96278769/1')
soup = BeautifulSoup(res.text)
for img in soup.select('.img'):
    fname = img['src'].split('/')[-1]
    res2 = requests.get(img['src'], stream=True)
    f = open(fname, 'wb')
    shutil.copyfileobj(res2.raw, f)   
    f.close()
    del res2



'''
[爬蟲實戰] 如何使用Selenium 自動將slides.com 的網頁投影片輸出成圖檔?
爬蟲不一定是用來抓資料! 你也可以應用網路爬蟲把身邊一些瑣事自動化！這邊我們就教學該如何使
用Selenium 撰寫一個爬蟲，自動將我用slides.com 所製作的HTML 網頁投影片轉換成圖檔，之後
再將圖檔結合起來後匯出成pdf 檔，這樣就不用花錢升級會員，也可以將投影片匯出成pdf 了!
'''
import requests
from selenium import webdriver
import time 
driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')

pageurl = 'http://slides.com/davidchiu/deck-1-2/live#/{}'
for page in range(1,26):
    driver.get(pageurl.format(page))
    time.sleep(2)
    driver.save_screenshot('page{}.png'.format(page))


'''
[爬蟲實戰] 如何突破證交所的限制，穩穩抓取最新成交資訊?
最近證交所的頁面更新，除了讓人有耳目一新的感覺，也帶給爬蟲(Python Crawler)全新的挑戰！
尤其很多人發現，只要頻繁抓取該網站頁面資訊，最終都會面臨無法繼續連上證交所的窘境；這其實
一切都是網頁伺服器的rate limiting 在作祟。因此，我們只要讓抓取之間能夠讓爬蟲小睡(Sleep)
個幾秒，便能擺脫IP被封鎖的命運，讓爬蟲重振雄風，順利抓取您想抓取的資料！ 
程式碼: https://github.com/ywchiu/largitdata/blob/master/code/Course_100.ipynb
'''
import requests 
import time 
for i in range(1,100):
    res = requests.get('http://www.twse.com.tw/exchangeReport/MI_5MINS?response=json&date=&_=1543397783781')
    time.sleep(3)
    print(res)

res.json().keys()
res.json()['data']


'''
[爬蟲實戰] 如何使用機器學習方法破解驗證碼 (1) ? – 安裝opencv3
為了能夠使用更聰明的方法自動破解驗證碼，我們將運用機器學習方法中的類神經網路方法破
解驗證碼。但在建立模型之前，我們先須將opencv3安裝於Anaconda Python 3.6 上，之後便
可以利用Opencv3 切割出各驗證碼數字，方能建立分類模型，讓機器自動辨識驗證碼！
'''
import cv2
import requests 
import os 
os.chdir('C:\\Users\\SUNG ANN LEE\\desktop')

with open('kaptcha.jpg', 'wb') as f:
    res = requests.get('https://serv.gcis.nat.gov.tw/pub/kaptcha.jpg')
    f.write(res.content)

from PIL import Image
image = Image.open('kaptcha.jpg')


import PIL
import numpy 
pil_image = PIL.Image.open('kaptcha.jpg').convert('RGB')
open_cv_image = numpy.array(pil_image)

from matplotlib import pyplot as plt 
plt.imshow(open_cv_image)


'''
[爬蟲實戰] 如何使用機器學習方法破解驗證碼 (2) ? – 切割出驗證碼中的各個數字
繼我們可以於Python 3.5.2 安裝 OpenCV3 以後，我們便可以先透過　Python 爬蟲抓取經濟
部─公司及分公司基本資料查詢(http://gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do)
的驗證碼，之後便可以使用OpenCV 的 findContours 協助我們切割並儲存驗證碼中的各個數字!
'''
#BGR to Gray： Y=0.299R + 0.587G + 0.114*B人眼對綠色的敏感感較大，而對藍色最小，因此綠色權重較大，藍色較小，上述公式為彩色轉灰階的標準。
imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
#THRESH_BINARY超過閾值的像素設為最大值(maxval)，小於閾值的設為0。
ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
#第一個參數是尋找輪廓的圖像，第二個參數表示輪廓的檢索模式，第三個參數method為輪廓的近似辦法
#cv2.RETR_TREE建立一個等級樹結構的輪廓，cv2.CHAIN_APPROX_SIMPLE壓縮水平方向，垂直方向，對角線方向的元素，只保留該方向的終點坐標，例如一個矩形輪廓只需4個點來保存輪廓信息
#cv2.findContours()函數返回兩個值，一個是輪廓本身，還有一個是每條輪廓對應的屬性。
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#找出最小輪廓矩陣
ary = []
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)  #cv2.boundingRect用一個最小的矩形，把找到的形狀包起來
    print((x, y, w, h))    
    if w >= 15 and h ==24:
        ary.append((x, y, w, h))

ary = sorted(ary, key=lambda x:x[0]) #依照x的順序排序輪廓，劃出的輪廓才會按照原始圖片由左至右顯示

#老師上課教的方法
##依照x的順序排序輪廓，劃出的輪廓才會按照原始圖片由左至右顯示
#cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
#
#ary = []
#for (c,_) in cnts:
#    (x, y, w, h) = cv2.boundingRect(c)    
#    print((x, y, w, h))
#    if w >= 15 and h ==24:
#        ary.append((x, y, w, h))
#
#ary

#切出每個數字的圖片，並存檔
import os
os.chdir('C:\\Users\\SUNG ANN LEE\\desktop')
from matplotlib import pyplot as plt

#切出每一個數字輪廓
fig = plt.figure()
for id, (x, y, w, h) in enumerate(ary):
    roi = open_cv_image[y:y+h, x:x+w]
    thresh = roi.copy()
    a = fig.add_subplot(1, len(ary), id+1)
    plt.imshow(thresh)

#將每個數字存檔，用來訓練機器學習
for id, (x, y, w, h) in enumerate(ary):
    fig = plt.figure()
    roi = open_cv_image[y:y+h, x:x+w]
    thresh = roi.copy()
    plt.imshow(thresh)
    plt.savefig('{}.jpg'.format(id+1), dpi=300)
    


'''
[爬蟲實戰] 如何使用機器學習方法破解驗證碼 (3) ? – 使用類神經網路自動辨認驗證碼
將驗證碼切成一個個數字以後，我們接者就可以使用Python scikit-learn 提供的類神經網路
(MLPClassfier)，便可以讓電腦透過機器學習方法自動辨認圖片中的數字。如此一來，驗證碼
再也沒有辦法阻擋我們的爬蟲大軍！
程式碼：https://github.com/ywchiu/largitdata/blob/master/code/Course_93.ipynb 
如要學習更多有關Python 與機器學習相關課程，
可參考： https://edu.hellobi.com/course/159
'''
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
import numpy as np 

#改變原本圖形大小，使機器學習數度加快
import os
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic')
from PIL import Image
basewidth = 50
pil_image = Image.open('0\\15.jpg').convert('1') #convert('1')將圖片轉為黑白
wpercent = (basewidth/float(pil_image.size[0]))
hsize = int((float(pil_image.size[1])*float(wpercent)))
#ANTIALIAS：平滑濾波對所有可以影響輸出像素的輸入像素進行高質量的重採樣濾波，以計算輸出像素值。
img = pil_image.resize((basewidth, hsize), Image.ANTIALIAS)



#產生模型訓練數據
digits = []
labels = []
basewidth = 50
fig = plt.figure(figsize=(20, 20))
cnt = 0
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=.1, wspace=.1)
for i in range(0,10):
    for img in os.listdir('{}/'.format(i)):
        pil_image = Image.open('{}/{}'.format(i, img)).convert('1')    
        
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), Image.ANTIALIAS)
        
        ax = fig.add_subplot(40, 12, cnt+1, xticks=[], yticks=[])
        ax.imshow(img, cmap=plt.cm.binary, interpolation='nearest')
        ax.text(0, 7, str(i), color='red', fontsize=10)
        cnt = cnt +1
        
        digits.append([pixel for pixel in iter(img.getdata())])
        labels.append(i)
        
import numpy
digit_ary = numpy.array(digits)
digit_ary.shape

#標準化訓練資料
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(digit_ary)
X_scaled = scaler.transform(digit_ary)

#訓練類神經網路
mlp = MLPClassifier(hidden_layer_sizes=(30, 30, 30), activation='logistic', max_iter= 1000)
mlp.fit(X_scaled, labels)

predicted = mlp.predict(X_scaled)
predicted

target = numpy.array(labels)

predicted == target

##預測測試資料
import os 
import PIL
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\')
#視覺化要預測的資料
fig = plt.figure(figsize=(20, 20))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=.05, wspace=.05)

for idx, img in enumerate(os.listdir('prediction\\')):
    pil_image = PIL.Image.open('prediction\\{}'.format(img)).convert('1')
    ax = fig.add_subplot(10, 12, idx+1, xticks=[], yticks=[])
    ax.imshow(pil_image, cmap=plt.cm.binary, interpolation='nearest')

#將資料轉為結構資料放入模型中預測
data = []
basewidth = 50
fig = plt.figure(figsize=(20, 20))
cnt = 0
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=.05, wspace=.05)
for idx, img in enumerate(os.listdir('prediction\\')):
    pil_image = PIL.Image.open('prediction\\{}'.format(img)).convert('1')
    
    wpercent = (basewidth/float(pil_image.size[0]))
    hsize = int((float(pil_image.size[1])*float(wpercent)))
    img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
    data.append([pixel for pixel in iter(img.getdata())])
#資料標準化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(data)
data_scaled = scaler.transform(data)
#預測結果
mlp.predict(data_scaled)


'''
[爬蟲實戰] 如何使用機器學習方法破解驗證碼 (4) ?  將所有流程串接起來
– 如何存取訓練模型
當建立完訓練模型後，勢必要將模型保存成pickle 檔，系統後續便可以再讀取pickle 檔，便
可持續利用該模型破解驗證碼，完成爬蟲以順利抓取公司及分公司基本資料! 
程式碼：https://github.com/ywchiu/largitdata/blob/master/code/Course_94.ipynb 
如要學習更多有關Python 與機器學習相關課程，
可參考： https://edu.hellobi.com/course/159
'''

'''資料前處理'''
import matplotlib.pyplot as plt
import os, PIL
import numpy as np
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\')

digits = []
labels = []
basewidth = 50

for i in range(0,10):
    for img in os.listdir('{}/'.format(i)):
        pil_image = Image.open('{}/{}'.format(i, img)).convert('1')    
        
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), Image.ANTIALIAS)
        
        digits.append([pixel for pixel in iter(img.getdata())])
        labels.append(i)

'''標準化資料'''
from sklearn.preprocessing import StandardScaler
import numpy 
digit_ary = numpy.array(digits)

scaler = StandardScaler()
scaler.fit(digit_ary)
X_scaled = scaler.transform(digit_ary)


'''建立模型'''
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(30, 30, 30), activation='logistic', max_iter=1000)
mlp.fit(X_scaled, labels)


'''將模型存成pickle檔'''
#以後如果要辨識此網頁驗證碼，就不用再重新訓練模型，可以載入訓練好的模型pickle檔
#存成pickle檔
from sklearn.externals import joblib
joblib.dump(mlp, 'captcha.pkl')
#載入pickle檔
clf = joblib.load('captcha.pkl')

'''儲存驗證碼'''
import requests
rs = requests.session()
res = rs.get('https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do')
with open('kaptcha.jpg', 'wb') as f:
    res2 = rs.get('https://serv.gcis.nat.gov.tw/pub/kaptcha.jpg')
    f.write(res2.content)

from PIL import Image
Image.open('kaptcha.jpg')


'''建立驗證碼儲存與切割函式'''
import requests
import numpy
from matplotlib import pyplot as plt
from datetime import datetime
import time 
import cv2
from sklearn.preprocessing import StandardScaler
basewidth = 50

#將image做灰階化找到輪廓並存在dest資料夾中
def saveKaptcha(image, dest):
    pil_image = PIL.Image.open(image).convert('RGB')
    open_cv_image = numpy.array(pil_image)
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    ary = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)  #cv2.boundingRect用一個最小的矩形，把找到的形狀包起來
        print((x, y, w, h))    
        if w >= 15 and h ==24:
            ary.append((x, y, w, h))
    ary = sorted(ary, key=lambda x:x[0]) #依照x的順序排序輪廓，劃出的輪廓才會按照原始圖片由左至右顯示

    for idx, (x, y, w, h) in enumerate(ary):
        roi = open_cv_image[y:y+h, x:x+w]
        thresh = roi.copy()
        plt.imshow(thresh)
        plt.savefig(os.path.join(dest, '{}.jpg'.format(idx)), dpi=300)


'''辨識驗證碼函數'''
#載入pickle檔
from sklearn.externals import joblib
clf = joblib.load('captcha.pkl')

def predictKaptcha(dest):
    data = []
    for idx, img in enumerate(os.listdir(dest)):
        pil_image = PIL.Image.open(os.path.join(dest, '{}'.format(img))).convert('1')
    
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
        data.append([pixel for pixel in iter(img.getdata())])

    scaler.fit(data)
    data_scaled = scaler.transform(data)    
    return clf.predict(data_scaled)



'''撰寫網路爬蟲'''
import requests
rs = requests.session()
res = rs.get('https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do', verify=False)
with open('kaptcha.jpg', 'wb') as f:
    res2 = rs.get('https://serv.gcis.nat.gov.tw/pub/kaptcha.jpg', verify=False)
    f.write(res2.content)

saveKaptcha('kaptcha.jpg', 'imagedata')
kaptcha = predictKaptcha('imagedata')

print(kaptcha)
Image.open('kaptcha.jpg')

payload = {
    'method':'query',
    'otherEnterFlag':'false',
    'useEUC':'N',
    'isShowEUC':'N',
    'queryKey':'',
    'selCmpyType':'1',
    'selQueryType':'2',
    'queryStr':'24567645',
    'brBanNo':'',
    'imageCode':'928125'
    }   

headers = {
        'Referer':'https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
            }
payload['imageCode'] = ''.join([str(ele) for ele in kaptcha.tolist()])
res3 = rs.post('https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do', data=payload, headers=headers, verify=False)
#res3.encoding = 'cp950'

print(res3.text)


################################################################################
'''Use Tensorflow to train model'''
###############################################################################
import os, PIL
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
    
def saveKaptcha(image, dest):
    pil_image = PIL.Image.open(image).convert('RGB')
    open_cv_image = numpy.array(pil_image)
    imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    ary = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)  #cv2.boundingRect用一個最小的矩形，把找到的形狀包起來
        print((x, y, w, h))    
        if w >= 15 and h ==24:
            ary.append((x, y, w, h))
    ary = sorted(ary, key=lambda x:x[0]) #依照x的順序排序輪廓，劃出的輪廓才會按照原始圖片由左至右顯示
    
    for idx, (x, y, w, h) in enumerate(ary):
        roi = open_cv_image[y:y+h, x:x+w]
        thresh = roi.copy()
        plt.imshow(thresh)
        plt.savefig(os.path.join(dest, '{}.jpg'.format(idx)), dpi=300)

def next_batch(num, data, labels):

    '''
    Return a total of `num` random samples and labels. 
    '''
    idx = np.arange(0 , len(data))
    np.random.shuffle(idx)
    idx = idx[:num]
    data_shuffle = data[idx]
    labels_shuffle = labels[idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)


###################產生模型訓練數據#####################
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\')

digits = []
labels = []
basewidth = 50
fig = plt.figure(figsize=(20, 20))
cnt = 0
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=.1, wspace=.1)
for i in range(0,10):
    for img in os.listdir('{}/'.format(i)):
        pil_image = Image.open('{}/{}'.format(i, img)).convert('1')    
        
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), Image.ANTIALIAS)
        
        digits.append([pixel for pixel in iter(img.getdata())])
        labels.append(i)
        
import numpy
digit_ary = numpy.array(digits)
digit_ary.shape

#標準化訓練資料
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(digit_ary)
X_scaled = scaler.transform(digit_ary)

#One-hot transform
import keras
labels = keras.utils.to_categorical(labels,10)


###################訓練類神經網路#######################
import tensorflow as tf 
import cv2
sess = tf.InteractiveSession()

input_images = tf.placeholder(tf.float32, shape=[None, 1650], name='input_images')
target_labels = tf.placeholder(tf.float32, shape=[None, 10], name='target_labels')
hidden_nodes = 512

input_weights = tf.Variable(tf.truncated_normal([1650, hidden_nodes]), name='input_weights')
input_biases = tf.Variable(tf.zeros([hidden_nodes]), name='input_biases')
hidden_weights = tf.Variable(tf.truncated_normal([hidden_nodes, 10]), name='hidden_weights')
hidden_biases = tf.Variable(tf.zeros([10]), name='hidden_biases')

input_layer = tf.matmul(input_images, input_weights)
hidden_layer = tf.nn.relu(input_layer + input_biases)
digit_weights = tf.matmul(hidden_layer, hidden_weights) + hidden_biases

loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=digit_weights, labels=target_labels))
optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss_function) #learning rate is 0.5

tf.global_variables_initializer().run()

for x in range(2000):
    [input_images_batch, target_labels_batch] = next_batch(num=100, data=X_scaled, labels=labels)
    optimizer.run(feed_dict={input_images: input_images_batch, target_labels: target_labels_batch})
#建立分類器
predict = tf.nn.softmax(digit_weights)
#預測第一張圖
classification = sess.run(tf.argmax(predict, 1), feed_dict={input_images: X_scaled[100:150,:]})
classification

######儲存predict，以便在預測時使用(載入模刑法二會用到)#######
tf.add_to_collection('predict', predict)

#儲存模型ckeckpoint 
saver = tf.train.Saver()
save_path = saver.save(sess,"D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\TFcheckpoint\\tfPredict.ckpt")  


sess.close()


#############################################################################
'''載入以訓練好的模型 方法一 存成checkpoint, 載入訓練好的變數，載入模型前，需
                            先定義好變數(容器)，且須從新定義結構圖，比較麻煩 '''
#############################################################################

#載入模型
import tensorflow as tf  
import numpy as np  
#定義變數當作載入資料的容器
hidden_nodes = 512
input_weights = tf.Variable(tf.truncated_normal([1650, hidden_nodes]), name='input_weights')
input_biases = tf.Variable(tf.zeros([hidden_nodes]), name='input_biases')
hidden_weights = tf.Variable(tf.truncated_normal([hidden_nodes, 10]), name='hidden_weights')
hidden_biases = tf.Variable(tf.zeros([10]), name='hidden_biased')

input_images = tf.placeholder(tf.float32, shape=[None, 1650])
target_labels = tf.placeholder(tf.float32, shape=[None, 10])

input_layer = tf.matmul(input_images, input_weights)
hidden_layer = tf.nn.relu(input_layer + input_biases)
digit_weights = tf.matmul(hidden_layer, hidden_weights) + hidden_biases

predict = tf.nn.softmax(digit_weights)


saver = tf.train.Saver({'input_weights':input_weights, 'input_biases':input_biases, 'hidden_weights':hidden_weights, 'hidden_biases':hidden_biases})  
with tf.Session() as sess:  
    saver.restore(sess,"D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\TFcheckpoint\\tfPredict.ckpt")  

    classification = sess.run(tf.argmax(predict, 1), feed_dict={input_images: X_scaled[100:150,:]})
    print(classification)


##################查詢Checkpoint中的變練名稱##################
import os
from tensorflow.python import pywrap_tensorflow
current_path = os.getcwd()
model_dir = os.path.join(current_path, 'TFcheckpoint')
checkpoint_path = os.path.join(model_dir,'tfPredict.ckpt') 
# Read data from checkpoint file
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
# Print tensor name and values
for key in var_to_shape_map:
    print("tensor_name: ", key)




#####################################################################################
'''載入以訓練好的模型 方法二 不需重新定義網路結構的方法 從檔案中將儲存的graph的所有節點載入到當前的default graph中，並返回一個saver。也就是說，我們在儲存的時候，除了將變數的值儲存下來，其實還有將對應graph中的各種節點儲存下來，所以模型的結構也同樣被儲存下來了。

比如我們想要儲存計算最後預測結果的predict，則應該在訓練階段將它新增到collection中 '''
#####################################################################################
import tensorflow as tf  
tf.reset_default_graph() 
#將模型結構圖載入
new_saver = tf.train.import_meta_graph("D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\TFcheckpoint\\tfPredict.ckpt.meta")

with tf.Session() as sess:
    #載入模行中的參數
    new_saver.restore(sess, "D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\TFcheckpoint\\tfPredict.ckpt")
    # tf.get_collection() 返回一個list. 但是這裡只要第一個引數即可
    predict = tf.get_collection('predict')[0]
    graph = tf.get_default_graph()
    # 因為predict中有placeholder，所以sess.run(predict)的時候還需要用實際待預測的樣本以及相應的引數來填充這些placeholder，而這些需要通過graph的get_operation_by_name方法來獲取。
    input_images = graph.get_operation_by_name('input_images').outputs[0]
    target_labels = graph.get_operation_by_name('target_labels').outputs[0]
    # 使用predict進行預測  
    print(sess.run(tf.argmax(predict, 1), feed_dict={input_images: X_scaled[0:100,:]}))
    



#TensorpredictKaptcha函數-辨識單張或多張圖片
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

def TensorpredictKaptcha(dest):
    data = []
    for idx, img in enumerate(os.listdir(dest)):
        pil_image = PIL.Image.open(os.path.join(dest, '{}'.format(img))).convert('1')
    
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
        data.append([pixel for pixel in iter(img.getdata())])

    scaler.fit(data)
    data_scaled = scaler.transform(data)    
    return sess.run(tf.argmax(predict, 1), feed_dict={input_images: data_scaled})


#抓新的驗證碼
import requests
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic')
rs = requests.session()
res = rs.get('https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do', verify=False)
with open('kaptcha.jpg', 'wb') as f:
    res2 = rs.get('https://serv.gcis.nat.gov.tw/pub/kaptcha.jpg', verify=False)
    f.write(res2.content)

#刪除imagedata資料夾裡的資料
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\imagedata')
for img in os.listdir():
    os.remove(img)
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic')
saveKaptcha('kaptcha.jpg', 'imagedata')

#預測結果
Image.open('kaptcha.jpg')
TensorpredictKaptcha('imagedata')

sess.close()



################################################################################
'''Use Keras to train model'''
###############################################################################
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import RMSprop

#Setting up model
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(1650,)))
model.add(Dense(10, activation='softmax')) #自動加入input_shape=(1650,)

model.summary()

#Setting up optimizer and loss function 
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

#Training model
model.fit(X_scaled, labels,
                    batch_size=1000,
                    epochs=10,
                    verbose=1,
                    )

#預測結果
model.predict_classes(X_scaled[0:400,:])

#儲存模型
#將模型儲存至 HDF5 檔案中
import os 
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\KerasModel')

model.save('KerasPredict.h5')  # creates a HDF5 file 'my_model.h5'


###############載入訓練好的模型####################
import tensorflow as tf
import os 
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\KerasModel')
#從 HDF5 檔案中載入模型
model = tf.contrib.keras.models.load_model('KerasPredict.h5')

model.predict_classes(X_scaled[0:400,:])

###驗證網路上的驗證碼
import requests
import cv2
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic')
rs = requests.session()
res = rs.get('https://serv.gcis.nat.gov.tw/pub/cmpy/cmpyInfoListAction.do', verify=False)
with open('kaptcha.jpg', 'wb') as f:
    res2 = rs.get('https://serv.gcis.nat.gov.tw/pub/kaptcha.jpg', verify=False)
    f.write(res2.content)

#刪除imagedata資料夾裡的資料
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\imagedata')
for img in os.listdir():
    os.remove(img)
os.chdir('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic')
saveKaptcha('kaptcha.jpg', 'imagedata')


###將導入的模型用於預測網路上的驗證碼###
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

def KerasKaptcha(dest):
    data = []
    for idx, img in enumerate(os.listdir(dest)):
        pil_image = PIL.Image.open(os.path.join(dest, '{}'.format(img))).convert('1')
    
        wpercent = (basewidth/float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1])*float(wpercent)))
        img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
        data.append([pixel for pixel in iter(img.getdata())])

    scaler.fit(data)
    data_scaled = scaler.transform(data)    
    return model.predict_classes(data_scaled)

#預測結果
Image.open('kaptcha.jpg')
KerasKaptcha('D:\\程式\\python\\PythonCrawler\\Practice\\Data\\NumberPic\\imagedata')



'''
[爬蟲實戰] 如何擷取網頁中的隱藏輸入以順利下載證交所的 csv 檔?
爬蟲除了可以直接擷取網頁上的資訊外，也可以用來下載 csv 檔。但看到證交所將網頁內容
以base64 的編碼放置在post 的參數中時，著實也被這匪夷所思的寫法嚇了一跳。所幸我們可
以直接抓取網頁中的隱藏輸入，再將資料做base64編碼，這時我們便可順利的將csv 抓取下來了!
'''
import requests
import os 
os.chdir('C:\\Users\\SUNG ANN LEE\\Desktop')

res = requests.get('http://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=20181130&selectType=ALL', stream=True)
from shutil import copyfileobj
f = open('data.csv', 'wb')
copyfileobj(res.raw, f)

f.close()
del res



'''
[爬蟲實戰] 如何使用Python 爬蟲 (Python Crawler) 下載Youtube 影片
這次介紹該如何寫一個Python 爬蟲 (Python Crawler) 把Youtube 影片下載下來。雖然是影
片檔案，但抓取的方法其實跟一般的爬蟲並無二異，只要先觀察到實體影片的連結位址後，用正
規表達法還有Query String 剖析函式，就可以把影片連結抓取出來，接者再用寫進binary 的
方式，就可以把Girl's day Expectation 的影音串流(https://youtu.be/5yAU52qfYuU) 
從Youtube下載下來啦！好吧，該來練一下吊帶舞了! Woo~ woo~ woo~
'''
import requests
res = requests.get('https://www.youtube.com/watch?time_continue=38&v=5yAU52qfYuU')
print(res.text) 

import re
m = re.search('"args":{(.*?),"url":""', res.text)

with open('temp.txt', 'w') as f:
    f.write(m.group(1))

import json 
jd = json.loads('{'+m.group(1))
jd.keys()

import urllib.parse
a = urllib.parse.parse_qs(jd['url_encoded_fmt_stream_map'])
a['url'][0]

import shutil 
res2 = requests.get(a['url'][0], stream=True)
f = open('temp.mp4', 'wb')
shutil.copyfileobj(res2.raw, f)
f.close()

##############################網頁寫法改變............



'''
[爬蟲實戰] 如何快速爬取天貓TMALL 雙11 特價商品資訊?
又到了雙11 購物狂歡的日子！話不多說，我們就從天貓TMALL 網路爬蟲當做瘋狂購物的前奏吧
！我們首先就用了Python Requests 套件抓取天貓商城的商品資訊，接著搭配BeautifulSoup4 
及 Pandas，讓資料爬取、資料整理到資料儲存能夠三位一體，一次完成！ 
程式碼：https://github.com/ywchiu/largitdata/blob/master/code/Course_98.ipynb
'''
import requests
res = requests.get('https://list.tmall.com/search_product.htm?acm=lb-zebra-24139-328516.1003.4.456266&vmarket=72&q=%CA%D6%BB%FA&spm=141.3067357.a2227oh.d100&from=3c..pc_1_searchbutton&type=p&scm=1003.4.lb-zebra-24139-328516.OTHER_1_456266')
res.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text, 'html.parser')
soup.select('.product-iWrap')
len(soup.select('.product-iWrap'))

soup.select('.product-iWrap')[3].text.strip() #.strip()可以刪掉左右空白
data = soup.select('.product-iWrap')

df = []
for item in data:
    soup2 = BeautifulSoup(item.text)
    a = soup2.select('p')[0].text.split(' ')
    df.append(a)

import pandas as pd
df2 = pd.DataFrame(df)



'''
[爬蟲實戰] 如何使用Python 模擬登入淘寶並成功抓取淘寶指數?
要了解一個市場前，獲取市場相關數據勢必是第一優先！在中國已外可以參照Google Trend，但
在中國就只能用淘寶指數。但困難點在於淘寶指數必須先登入後，才能抓取相關資訊。但天下沒
有無法抓取的資料，一切都在於耐心觀察，藉由觀察登入的樣式與資料的位置後，再透過強大的
Python抓取。依然，我們這次依然可以取得我們要的資料！
'''

import requests
from bs4 import BeautifulSoup as bs
headers = {
        'cookie':'hng=TW%7Czh-TW%7CTWD%7C158; t=502b400ce5ce12d6a596a01a4477be70; _uab_collina=154113413798023327774075; cookie2=1af35876675c7f0225fc8619d7c8fd44; _tb_token_=333ebbf7e7337; XSRF-TOKEN=f1d5fd71-7b19-48f0-aa2d-82209b0eaa55; lid=a77689466; lc=VymaZKQzkd8Fe7bYQSo%3D; _cc_=WqG3DMC9EA%3D%3D; tg=0; l=Anx8jvgeWoO2gAAxBYbk0a5mzBEu6yCf; isg=AuDgX2HmqCVCyhP80qmTZwdXse4IGsSzAi8b3FrxMvuOVYV_C_mUQ7Yli0up; thw=tw; _m_h5_tk=9afbfbd21145f909ddb8faf5fa54fa85_1543927715575; _m_h5_tk_enc=c16b241d4cdd1acf425c2710b6cef12d; enc=oArBqQH94JP16PMZNGEYxmeqUMzO9w3XDXurmW4xTC04%2FX3Wqax456GcgemkeO7%2Bu6Qi0WWeGB6CHT79LyLr7A%3D%3D; v=0; uc1=cookie14=UoTYNcK3oechvA%3D%3D; mt=ci=-1_0; cookieCheck=28111',
        'origin':'https://login.taobao.com',
        'referer':'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fshu.taobao.com%2F',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

rs = requests.session()
res = rs.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fshu.taobao.com%2F&TPL_username=a77689466&TPL_password=&ncoSig=&ncoSessionid=&ncoToken=8254ea90764861f086a89570b044f046a805ce2a&slideCodeShow=false&useMobile=false&lang=zh_CN&loginsite=0&newlogin=0&TPL_redirect_url=http%3A%2F%2Fshu.taobao.com%2F&from=tb&fc=default&style=default&css_style=&keyLogin=false&qrLogin=true&newMini=false&newMini2=false&tid=&loginType=3&minititle=&minipara=&pstrong=&sign=&need_sign=&isIgnore=&full_redirect=&sub_jump=&popid=&callback=&guf=&not_duplite_str=&need_user_id=&poy=&gvfdcname=10&gvfdcre=68747470733A2F2F7777772E676F6F676C652E636F6D2E74772F&from_encoding=&sub=&TPL_password_2=1b8be522ba6f199e54c53fe1960a51105778ff3edb645194ac888e919cfb3e3fbac34f6b9a579946a06ff0d71b343c49610fce2bfd20f2a786a551c7eae991dda32295050b734f2fe1322818e2602e7e83570af30e617c79e918af08cab7e90524f474edb36e18598925cf500d21df99479c2eae68fe1f22c3a3f854a2a8b250&loginASR=1&loginASRSuc=1&allp=&oslanguage=zh-TW&sr=1536*864&osVer=&naviVer=chrome%7C70.0353811&osACN=Mozilla&osAV=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F70.0.3538.110+Safari%2F537.36&osPF=Win32&miserHardInfo=&appkey=00000000&nickLoginLink=&mobileLoginLink=https%3A%2F%2Flogin.taobao.com%2Fmember%2Flogin.jhtml%3FredirectURL%3Dhttp%3A%2F%2Fshu.taobao.com%2F%26useMobile%3Dtrue&showAssistantLink=true&um_token=C1541134137980233277740751543919313576138&ua=114%23MGJNm4OQTTo80TbrSWncva%2F00joJCpczUQoAQf3W%2FX0%2B7H7V%2BK5VugR9PxwIVuNdFX5VTg85QPH3iwJMLijbPN3aeEs89i1JseuAx0tVb8PwAHAB93%2F0fxu40N1Ge%2B05GCbKg2G%2FczwdFxpPIolX2m9n9rZALiQnjs8WwbxFoGDa35TawR18zo8Dn8RD26gm8TssTmJDfMon8TT9e7cGPppKgXjVIXZJ8TTTmJ6UfnoTZ8ntSi89PmmgMwfzpMgRTbtbx4nUgAsT28TT2Q7ofjZwTBzy4xopMdvgeWBp9G1rLWJM%2BGaTQB7sv9bMnT8QYiJbyR8HpCdu0cW1S7nzHI5KBbQRYu2dfVwT%2FiCsdgDyy8yaNcMekV0fmHnN5bhBTVtLbzgyBlA9lpSnqG1ctoPF6lo9RNdfFoaZ2iCvcFDVQkfpZxAapuwVdVbkhRGmQaN%2BqVJPEHBB0T%2FhjzpACTlYwCdKQ2lYm8x6Fo9BwYJttjHdcfndnGhQD9qAcXak6f5UQh4BeROnObaX9q71A%2BI5bFOssqNrF1putmH2vXiY4VgWeU4jykvyYcbInWB%2F4Ayf8LgsGRhemIWFIubp2l9weW2GXvt4lAANN3z3gyZ0PPacN49a4yfCHi%2FdgK9Sis0vDIdRPku6mFov32R2KIlxDLulvzr%2BIBpMpMf27WwOMnXWza39uHCBa3NheSmnX76Z0IaI88EF%2FNBjO%2B4LLmk5VMuO9hA3wcWKQuWjzrbUupYCDXtcQLFm2pWYn5kmaSbI%2BMbEOMfUJynUgQGrtc1frW3NZuoE', headers=headers)

res2 = rs.get('https://shu.taobao.com/api/oneql', headers = headers)
res2.text


##############################網頁寫法改變............


'''
[爬蟲實戰] 如何透過 Python 網路爬蟲 抓取並整理 2018 公投選舉資料?
選舉已經在2018/11/24 號落幕，但是還是有很多人想要了解在這次公投，各地區的人民做了哪些
選擇。為了能夠分析這次公投的資料，我們可以利用Python 的 Selenium 與 Requests 抓取中選
會(http://referendum.2018.nat.gov.tw/pc/zh_TW/index.html)的投票統計資料，讓你能夠
在取得完整資料後，分析各地民眾的意向。 如果想要直接分析的朋友，也可以直接到
https://www.largitdata.com/blog_detail/20181129 下載整理過後的資料 
程式碼： https://github.com/ywchiu/largitdata/blob/master/code/Course_109.ipynb
'''

import requests
res = requests.get('http://referendum.2018.nat.gov.tw/pc/zh_TW/02/63000000000000000.html')
res.text

#發現各區域網頁連結是由java script function 生成，可透過拆解function得到連結，但太過麻煩，
#另一個方法就是利用selenium打開網頁，javascript function 會產生好網頁連結
from selenium import webdriver
driver = webdriver.Chrome('D:\程式\python\PythonCrawler\WebDriver\ChromeWebDriver\chromedriver')
driver.get('http://referendum.2018.nat.gov.tw/pc/zh_TW/02/63000000000000000.html')

from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')
#取出id為item開頭的數據
links = soup.select('div[id^=item] a')

domain = 'http://referendum.2018.nat.gov.tw/pc/zh_TW/'
for ele in links:
    print(domain + ele.get('href').strip('.'))


#整理每個連結資料
import pandas
dfs = pandas.read_html('http://referendum.2018.nat.gov.tw/pc/zh_TW/02/63000000000000000.html')

votes = dfs[2]
votes.columns = votes.loc[1]
votes.drop([0,1,3,4], inplace=True)
votes.reset_index(drop=True, inplace=True)

totalvotes = dfs[3]
totalvotes.columns = totalvotes.loc[0]
totalvotes.drop([0,2,3], inplace=True)
totalvotes.reset_index(drop=True, inplace=True)

m = pandas.concat([votes, totalvotes], axis=1)

#爬取資料所在地區
res = requests.get('http://referendum.2018.nat.gov.tw/pc/zh_TW/02/63000000000000000.html')
soup = BeautifulSoup(res.text, 'lxml') 

soup.select('b')
#有三個b，取第一個，用select_one
area = soup.select_one('b').text
m['投票地區'] = area
m



#寫出抓取每個連結的函數
def getRef(url):
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml') 
    dfs = pandas.read_html(res.text)
    
    votes = dfs[2]
    votes.columns = votes.loc[1]
    votes.drop([0,1,3,4], inplace=True)
    votes.reset_index(drop=True, inplace=True)
    
    totalvotes = dfs[3]
    totalvotes.columns = totalvotes.loc[0]
    totalvotes.drop([0,2,3], inplace=True)
    totalvotes.reset_index(drop=True, inplace=True)
    
    m = pandas.concat([votes, totalvotes], axis=1)
    area = soup.select_one('b').text
    m['投票地區'] = area

    return m

getRef('http://referendum.2018.nat.gov.tw/pc/zh_TW/02/63000000000000000.html')


#爬取所有連結
domain = 'http://referendum.2018.nat.gov.tw/pc/zh_TW/'
results = []
for ele in links[0:3]:
    try:
        results.append(getRef(domain + ele.get('href').strip('.')))
    except:
        print(domain + ele.get('href').strip('.'))

Df = pandas.concat(results)





 
 


