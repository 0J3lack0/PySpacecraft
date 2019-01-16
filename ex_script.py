#deneme dosyası...
import requests
from bs4 import BeautifulSoup as bs
import lxml.html
import urllib3
import pandas as pd

url = 'https://www.cfa.harvard.edu/shocks/ac_master_data/ac_master_1998.html'
url2 ='https://www.cfa.harvard.edu/shocks/ac_master_data/'
r = requests.get(url)

soup = bs(r.content, 'html.parser')
v = soup.find('table', attrs={'class': 'content_table'}).find_all('a')
v.pop()   #array'deki son link çıkarıtılır.


#örneğin   v[1] = <a href="./00000/ac_master_00000.html">link</a> bize ilk elemanda ki  ./00000/ac_master_00000.html  kısım lazım ve bunu tüm array elemanları için uygulamalıyız
#v.attrs['href'] istediğimiz işlemi yapacaktır.

for i in range(0,len(v)):
    v[i] = v[i].attrs['href']

for j in range(0,len(v)):
    v[j] = url2+v[j]

print(v)
i = 0
#for i in range(0,len(v))
g = requests.get(v[1])
#    Sp = bs(g.content, 'html.parser')

t=bs(g.content, "lxml")
table_body=t.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols=row.find_all('td')
    cols=[x.text.strip() for x in cols]
    print (cols)
