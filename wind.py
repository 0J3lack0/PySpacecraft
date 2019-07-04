import requests
import xlsxwriter
import os
from bs4 import BeautifulSoup as bs

baseURL    = 'https://www.cfa.harvard.edu/shocks/wi_data/'
pathPrefix = 'wi_'
years      = ['1995', '1996', '1997','1998','1999','2000','2001','2002', '2003','2004','2005','2006',
              '2007','2008','2009','2010','2011','2012','2013','2014', '2015', '2016', '2017']

for i in range(0, len(years)):
    currName = years[i]
    currLink = baseURL + pathPrefix + currName + '.html'
    currFile = 'wind_data/' + currName + '.xlsx'

    print('')
    print('#########################################################################')
    print('Working for: ' + currName)
    print('URL: ' + currLink)
    print('#########################################################################')

    if os.path.exists(currFile):
        os.remove(currFile)

    workbook   = xlsxwriter.Workbook(currFile)
    cellFormat = workbook.add_format({'align': 'center'})
    r          = requests.get(currLink)
    soup       = bs(r.content, 'html.parser')
    v          = soup.find('table', attrs={'class': 'content_table'}).find_all('a')
    v.pop()
    print('Fetching tables...')

    for i in range(0, len(v)):
        v[i] = v[i].attrs['href']

    for i in range(0, len(v)):
        v[i] = baseURL + v[i]

    for i in range(0, len(v)):
        counter = str(i)
        print('Processing URL: ' + v[i])
        generalData = {}
        plasmaData = {}
        req = requests.get(v[i])
        content = bs(req.content, 'html5lib')
        generalInfo = content.select('td.content table')[2].find('tbody').find_all('tr')
        plasmaInfo = content.select('td.content table')[3].find('tbody').find_all('tr')

        for i in range(0, len(generalInfo)):
            currRow = generalInfo[i].find_all('td')

            if currRow:
                cleanDataName = bs(currRow[0].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
                cleanDataValue = bs(currRow[1].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
                generalData[cleanDataName] = cleanDataValue

        for i in range(0, len(plasmaInfo)):
            currRow = plasmaInfo[i].find_all('td')

            if currRow:
                cleanDataName             = bs(currRow[0].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
                cleanDataUpstreamValue    = bs(currRow[1].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
                cleanDataDownstreamValue  = bs(currRow[2].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')

                cleanDataUpstreamValue    = cleanDataUpstreamValue.split()[0]
                cleanDataDownstreamValue  = cleanDataDownstreamValue.split()[0]
                plasmaData[cleanDataName] = [cleanDataUpstreamValue, cleanDataDownstreamValue]

        worksheet = workbook.add_worksheet(str(int(counter) + 1))
        row       = 1
        column    = 0

        worksheet.set_column(0, 2, 50)
        worksheet.write(0, 0, 'General Information', cellFormat)

        for key in generalData:
            worksheet.write(row, column, key, cellFormat)
            worksheet.write(row, column + 1, generalData[key], cellFormat)
            row += 1

        row += 1
        worksheet.write(row, 0, 'Asymptotic plasma parameters', cellFormat)
        row += 1

        for key in plasmaData:
            worksheet.write(row, column, key, cellFormat)
            worksheet.write(row, column + 1, plasmaData[key][0], cellFormat)
            worksheet.write(row, column + 2, plasmaData[key][1], cellFormat)
            row += 1

    print('Writing xlsx file...')
    workbook.close()
