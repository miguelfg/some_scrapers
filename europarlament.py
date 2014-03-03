#!/usr/bin/env python
__author__ = 'miguelfg'

import scraperwiki
import requests
from bs4 import BeautifulSoup

base_url = 'http://www.europarl.europa.eu'
url = 'http://www.europarl.europa.eu'
html = requests.get(url)
soup = BeautifulSoup(html.content)

# 1) play a bit with beautiful soup
# soup.a
# soup.p
# soup.find_all('p')
# soup.find_all('a')
# soup.find(id="link3")
# soup.prettify()
#
# for link in soup.find_all('a'):
#     print(link.get('href'))
#
# print(soup.get_text())
# ================================================= #

# 2) scrape main page of euro diputates
# url = "http://www.europarl.europa.eu/meps/es/full-list.html"
# html = requests.get(url)
# soup = BeautifulSoup(html.content)
# ================================================= #

# 3) same as 2 but as a function
def get_one_soup(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content)
    # print soup.prettify()
    return soup
# ================================================= #

# 4) scrape one page of euro diputates
url = "http://www.europarl.europa.eu/meps/es/full-list.html?filter="
page_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

euro_dip = []
euro_dip_name = ""
euro_dip_country = ""
euro_dip_webpage = ""
euro_dip_eu_party = ""
euro_dip_country_party = ""

# unique_keys = ['id']
# unique_keys = ['name', 'eur_party', 'country_party', 'country', 'webpage']
unique_keys = ['']
unique_keys = ['name']
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)

id = 0
for page in page_list[:2]:
    soup = get_one_soup(url + page)
    # YA NAVEGAMOS!!
    # get interesting data
    zone_info_meps = soup.find_all('div', 'zone_info_mep')
    for mep in zone_info_meps:
        print "------->"
        print mep.find('li', 'mep_name').a.contents[0]
        print mep.find('li', 'mep_name').a.get('href')
        print mep.find('li', 'group').contents[0]
        print mep.find('span', 'name_pol_group').contents[0]
        print mep.find('li', 'nationality').contents[0]

        euro_dip_name = mep.find('li', 'mep_name').a.contents[0]
        euro_dip_webpage = mep.find('li', 'mep_name').a.get('href')
        euro_dip_eu_party = mep.find('li', 'group').contents[0]
        euro_dip_country_party = mep.find('span', 'name_pol_group').contents[0]
        euro_dip_country = mep.find('li', 'nationality').contents[0].strip()

        # scraperwiki.sql.save(unique_keys, data)
        scraperwiki.sqlite.save(["id"], {'id': id,
                                        'name':euro_dip_name,
                                        #'eu_party': euro_dip_eu_party.decode('latin-1'),
                                        'country_party': euro_dip_country_party,
                                        'country':euro_dip_country,
                                        'web': euro_dip_webpage})
        id += 1

# ================================================= #

# Saving data:
# data = { 'id':12, 'name':'violet', 'age':7 }
# unique_keys = [ 'id' ]
# scraperwiki.sql.save(unique_keys, data)
