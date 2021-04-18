import time
from selenium import webdriver
import re
from config import KindDict
from bs4 import BeautifulSoup
import smtplib
import base64
from email.mime.text import MIMEText

kind = KindDict
def Transfer(Rise):
    if Rise[0]=='+' :
        return float(Rise.strip('+'))
    else:
        return -float(Rise.strip('-'))

def Report(Coin,current):
    if current-kind[Coin]>=20:
        SendEmail('\n'+Coin+':'+str(current-kind[Coin]))

def filewrite(KindDict):
    file = open(r'coin.txt','wb')
    for i in KindDict :
        file.write((i+':'+str(KindDict[i])+'\n').encode('utf-8'))

def main():
    start = time.time()
    browser=webdriver.Chrome()
    url = 'https://www.huobi.li/zh-cn/markets/'
    browser.get(url)
    while 1 :
        data = browser.page_source
        while 'part-wrap' not in data:
            data = browser.page_source
        #print(data)
        Analyse = BeautifulSoup(data,'lxml')
        for i in KindDict:
            coindetail = Analyse.find(id=i)
            try :
                coindetail = coindetail.find(class_="rise").text.strip().strip('%')
                Report(i,Transfer(coindetail))
                KindDict[i] = Transfer(coindetail)
            except AttributeError:
                continue
        filewrite(KindDict)
        print(time.asctime())
        time.sleep(300)

def SendEmail(Message):
    Message = time.asctime()+'\n'+Message

    smtpserver = 'smtp.163.com'
    send = 'xxxxxxxxxx@163.com'
    recieve = 'xxxxxxxxxx@163.com'

    msg = MIMEText(Message, 'html', 'utf-8')
    msg['Subject'] = '虚拟货币暴涨提醒！'
    # msg['From'] = email.utils.formataddr(('py发送者', snd_email)) # 发件人：py发送者<xxx@163.com>
    msg['From'] = send
    msg['To'] = recieve

    password = b''#需要用到邮箱服务器的smtp服务，在这里填下授权码
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(send , bytes.decode(password))
    smtp.sendmail(send , recieve , msg= msg.as_string())
    smtp.quit()

if __name__=='__main__':
    main()

