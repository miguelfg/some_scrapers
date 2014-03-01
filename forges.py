__author__ = 'MiguelFG'
import requests
# from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
url = 'http://elpais.com/autor/antonio_fraguas_forges/a/'
html = requests.get(url)
soup = BeautifulSoup(html.content)
########################################
# soup.a
# soup.p
# soup.find_all('p')
# soup.find_all('a')
# soup.find(id="link3")
# soup.prettify()
# print soup.get_text()
# print soup.find_all('div', 'zone_info_mep')

#print soup.findAll('div', 'zone_info_mep')
#for link in soup.findAll('a'):
#    if not str(link.get('href')).startswith('javascript'):
#        print(link.get('href'))

########################################
print soup.a
print soup.p
print soup.find_all('p')
print soup.find_all('a')
print soup.find(id="link3")
print soup.prettify()
print soup.find_all('div', 'zone_info_mep')
for link in soup.find_all('a'):
     print(link.get('href'))
# print(soup.get_text())




