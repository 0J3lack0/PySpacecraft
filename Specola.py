import requests #project:Specola ; Specola gözlem evine ait güneş leke çizimlerinin  indirilmesi.
from bs4 import BeautifulSoup as bs


baseURL = 'http://www.specola.ch/drawings/e-cal'
years   = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
           '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

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
    t        = {}
    downlURL = {}
    base2Url = 'http://www.specola.ch/drawings/'
    for i in range(0, len(v)):
        v[i]        = v[i].attrs['href']
        t[i]        = v[i].replace("/", "")
        downlURL[i] = base2Url + v[i]






    for i in range(0, len(t)):
        with open(t[i], 'wb') as handle:
            print('Downloading URL' + downlURL[i])
            response = requests.get(downlURL[i], stream=True)

            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)