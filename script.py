import requests
import xlsxwriter
import os
from bs4 import BeautifulSoup as bs

linkAffix  = ['/ac_master_1998.html','/ac_master_1999.html','/ac_master_2000.html','ac_master_2001.html',
              'ac_master_2002.html','ac_master_2003.html','ac_master_2004.html','ac_master_2005.html',
              'ac_master_2006.html','ac_master_2007.html','ac_master_2008.html','ac_master_2009.html',
              'ac_master_2010.html','ac_master_2011.html','ac_master_2012.html','ac_master_2013.html',
              'ac_master_2014.html']
linksPage  = 'https://www.cfa.harvard.edu/shocks/ac_master_data/ac_master_1998.html'
baseURL    = 'https://www.cfa.harvard.edu/shocks/ac_master_data/'
r          = requests.get(linksPage)

soup = bs(r.content, 'html.parser')
v    = soup.find('table', attrs={'class': 'content_table'}).find_all('a')
v.pop()

for i in range(0, len(v)):
    v[i] = v[i].attrs['href']

for i in range(0, len(v)):
    v[i] = baseURL + v[i]

for i in range(0, len(v)):
    currName              = v[i].split('/')[-1][:-5]
    generalData           = {}
    plasmaData            = {}
    req                   = requests.get(v[i])
    content               = bs(req.content, 'html5lib')
    generalInfo           = content.select('td.content table')[2].find('tbody').find_all('tr')
    plasmaInfo            = content.select('td.content table')[3].find('tbody').find_all('tr')

    for i in range(0, len(generalInfo)):
        currRow = generalInfo[i].find_all('td')

        if currRow:
            cleanDataName              = bs(currRow[0].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
            cleanDataValue             = bs(currRow[1].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
            generalData[cleanDataName] = cleanDataValue
    
    for i in range(0, len(plasmaInfo)):
        currRow = plasmaInfo[i].find_all('td')

        if currRow:
            cleanDataName             = bs(currRow[0].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
            cleanDataValue            = bs(currRow[1].encode_contents().decode('utf-8'), 'lxml').get_text().replace('\n', '')
            plasmaData[cleanDataName] = cleanDataValue

    currFile = 'data/' + currName + '.xlsx'

    if os.path.exists(currFile):
        os.remove(currFile)
    
    workbook  = xlsxwriter.Workbook(currFile)
    worksheet = workbook.add_worksheet()
    row       = 1
    column    = 0
    
    worksheet.set_column(0, 1, 50)
    worksheet.write(0, 0, 'General Information')

    for key in generalData:
        worksheet.write(row, column, key)
        worksheet.write(row, column + 1, generalData[key])
        row += 1
    
    row += 1
    worksheet.write(row, 0, 'Asymptotic plasma parameters')
    row += 1
    
    for key in plasmaData:
        worksheet.write(row, column, key)
        worksheet.write(row, column + 1, plasmaData[key])
        row += 1

    workbook.close()



