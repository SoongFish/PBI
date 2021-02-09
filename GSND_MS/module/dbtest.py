import urllib.request
import bs4
import os

os.system('cls')

result = list()

url = 'https://github.com/SoongFish/GSND_MSDB/blob/master/version'

db = urllib.request.urlopen(url)
db_obj = bs4.BeautifulSoup(db, 'html.parser')

sep = db_obj.findAll('td', {'class' : 'blob-code'})

for index in range(len(sep)):
    result.append(sep[index].text)
    
print(result)

#result = open('result.txt', 'a', encoding = 'utf-8')
#result.write(str(db_obj))

#print(db.decode())

