import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.cfa.harvard.edu/shocks/ac_master_data/ac_master_1998.html'

r = requests.get(url)

soup = bs(r.content, 'html.parser')
soup.find('table', attrs={'class': 'content_table'}).find_all('a')


