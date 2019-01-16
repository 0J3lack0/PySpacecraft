import requests
from bs4 import BeautifulSoup as bs

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

