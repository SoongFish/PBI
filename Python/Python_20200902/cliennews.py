import requests
import lxml.html
import time
import telegram

my_token = ''
bot = telegram.Bot(token = my_token)
chat_id = 

response = requests.get("https://www.clien.net/service/board/news")

response.encoding = 'euc-kr'

root = lxml.html.fromstring(response.content.decode('UTF-8'))

root.make_links_absolute(response.url)

for line in root.xpath('//*[@id="div_content"]/div[7]/div'):
    #time.sleep(0.1)
    data_url = line.xpath('div[2]/a[1]')[0]
    url = data_url.get("href")
    
    data_title = line.xpath('div[2]/a[1]/span')[0]
    title = data_title.get("title")
    
    #data_reply = line.xpath('div[2]/a[2]/span')[0]
    #reply = data_reply.get("")
    #print(title, url, sep = "\t", end = "\n")
    
    bot.sendMessage(chat_id = chat_id, text = title + "\n" + url)
    break
    