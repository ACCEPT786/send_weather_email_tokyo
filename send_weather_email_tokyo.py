# coding=utf-8
import sys
import time
import json
import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

url = r'https://free-api.heweather.net/s6/weather/forecast?location=tokyo&key=bdb550a6112548289c3d8fe69fde04db'
today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
res = requests.get(url)
res.encoding = 'utf-8'
res = json.loads(res.text)
print(res)
result = res['HeWeather6'][0]['daily_forecast'][0]
date_tomorrow = result['date']
hum_tomorrow = result['hum']
sr_tomorrow = result['sr']
ss_tomorrow = result['ss']
cond_tomorrow = result['cond_txt_d']
max_tomorrow = result['tmp_max']
min_tomorrow = result['tmp_min']
pop_tomorrow = result['pop']
pcpn_tomorrow = result['pcpn']
uv_tomorrow = result['uv_index']
vis_tomorrow = result['vis']
location = res['HeWeather6'][0]['basic']['location']
info = ' 城市: ' + location + "\n" + ' 时间: ' + date_tomorrow + "\n" + ' 天气状况: ' + cond_tomorrow + "\n" + ' 最高气温: ' + max_tomorrow + "\n" + \
       ' 最低气温: ' + min_tomorrow + "\n" + ' 日出: ' + sr_tomorrow + "\n" + ' 日落: ' + ss_tomorrow + "\n" + ' 相对湿度: ' + hum_tomorrow + '\n' + \
       ' 降水概率: ' + pop_tomorrow + '\n' + ' 降水量：' + pcpn_tomorrow + '\n' + ' 紫外线强度：' + uv_tomorrow + '\n' + " 能见度：" + vis_tomorrow + '\n\n'

time.sleep(3)
sess = requests.sessions
sess.keep_alive = False
proxies = {
    'http': 'http://117.95.192.106:9999',
}
user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
               'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
headers = {'User-Agent': random.choice(user_agents)}
url = 'https://www.517japan.com/newsflash-3.html#box'
news = requests.get(url, headers=headers, proxies=proxies)
news.encoding = 'utf8'
soup = BeautifulSoup(news.text, 'lxml')

data1 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(1) > a > div.txt > h2')
brief1 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(1) > a > div.txt > p')
link1 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(1) > a')
for item in data1:
    title1 = item.get_text()
for item in brief1:
    sub_title1 = item.get_text()
for item in link1:
    href1 = item.get('href')

data2 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(2) > a > div.txt > h2')
brief2 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(2) > a > div.txt > p')
link2 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(2) > a')
for item in data2:
    title2 = item.get_text()
for item in brief2:
    sub_title2 = item.get_text()
for item in link2:
    href2 = item.get('href')

data3 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(3) > a > div.txt > h2')
brief3 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(3) > a > div.txt > p')
link3 = soup.select('body > div.newsflashes.clear > div.newsflashes_left > div.news_list > div:nth-child(3) > a')
for item in data3:
    title3 = item.get_text()
for item in brief3:
    sub_title3 = item.get_text()
for item in link3:
    href3 = item.get('href')
news_jp = title1 + "\n" + sub_title1 + "\n" + "https://www.517japan.com" + href1 + "\n\n" + \
          title2 + "\n" + sub_title2 + "\n" + "https://www.517japan.com" + href2 + "\n\n" + \
          title3 + "\n" + sub_title3 + "\n" + "https://www.517japan.com" + href3 + '\n\n'


# 设置邮箱的域名
HOST = 'smtp.qq.com'
# 设置邮件标题
SUBJECT = '%s日份东京地区信息，请查收' % today_time
# 设置发件人邮箱
FROM = '444709834@qq.com'
# 设置收件人邮箱
TO = '444709834@qq.com'  # 可以同时发送到多个邮箱
message = MIMEMultipart('related')
# --------------------------------------发送文本-----------------
# 发送邮件正文到对方的邮箱中
message_html = MIMEText("%s%s" % (info, news_jp), 'plain', 'utf-8')
message.attach(message_html)
# 设置邮件发件人
message['From'] = FROM
# 设置邮件收件人
message['To'] = TO
# 设置邮件标题
message['Subject'] = SUBJECT
# 获取简单邮件传输协议的证书
email_client = smtplib.SMTP_SSL()
# 设置发件人邮箱的域名和端口，端口为465
email_client.connect(HOST, '465')
# ---------------------------邮箱授权码------------------------------
result = email_client.login(FROM, 'zkumuwfdhgzjcaef')  # 授权码填写
print('登录结果', result)
email_client.sendmail(from_addr=FROM, to_addrs=TO.split(','), msg=message.as_string())
# 关闭邮件发送客户端
email_client.close()
