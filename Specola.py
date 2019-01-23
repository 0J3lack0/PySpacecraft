import requests #project:Specola ; Specola gözlem evine ait güneş leke çizimlerinin  indirilmesi.
import xlsxwriter
import os
import urllib
from bs4 import BeautifulSoup as bs


baseURL = 'http://www.specola.ch/drawings/e-cal'
years   = ['1995', '1996', '1997','1998','1999','2000','2001','2002', '2003','2004','2005','2006',
              '2007','2008','2009','2010','2011','2012','2013','2014', '2015', '2016', '2017']

for i in range(0, len(years)):
    currName = years[i]
    currLink = baseURL + years[i] + '.htm'


    print('')
    print('#########################################################################')
    print('Working for: ' + currName)
    print('URL: ' + currLink)
    print('#########################################################################')
    print(baseURL + currName + '.htm')

    r        = requests.get(currLink)
    soup     = bs(r.content, 'html.parser')
    v        = soup.find('h1').find_all('a')

    for i in range(0, len(v)):
        v[i] = v[i].attrs['href']

    base2Url = 'http://www.specola.ch/drawings/'
    downlURL = base2Url + v[i]
    t        = v[i].replace("/", "")
    print(t)
    with open(t, 'wb') as handle:
        response = requests.get(downlURL, stream=True)

        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
















 #   image    = urllib.URLopener()

 #  filename = downlURL.split('/')[1]
 #   t        = requests.get(downlURL, allow_redirects=True)

 #  open(filename, 'wb').write(t.content)
