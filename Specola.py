#project:Specola ; Specola gözlem eelemsine ait güneş leke çizimlerinin  indirilmesi.

import requests
import os
from bs4 import BeautifulSoup as bs

baseURL     = 'http://www.specola.ch/drawings/'
years       = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
           '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

for i in range(0, len(years)):
    currName = years[i]
    currPath = 'specola_data/' + currName
    currLink = baseURL + currName + '/'
    os.mkdir(currPath)

    print('')
    print('#########################################################################')
    print('Working for: ' + currName)
    print('URL: ' + currLink)
    print('#########################################################################')

    r          = requests.get(currLink)
    soup       = bs(r.content, 'html.parser')
    elems      = soup.find_all('a')[1:]
    downURLs   = {}

    for i in range(0, len(elems)):
        elems[i]    = elems[i].attrs['href']
        downURLs[i] = currLink + elems[i]

    for i in range(0, len(downURLs)):
        with open(currPath + '/' + elems[i], 'wb') as currFile:
            print('Downloading ' + elems[i] + ' image...')
            resp = requests.get(downURLs[i], stream = True)

            for block in resp.iter_content(1024):
                currFile.write(block)
