__author__ = 'MiguelFG'
import requests
from bs4 import BeautifulSoup
url = 'http://www.flourish.org/blog'
html = requests.get(url)
soup = BeautifulSoup(html.text)

# ALL HTML
print soup
# print soup.prettify()
# print soup.get_text()

# PRIMEROS FILTROS: LINKS, PARRAFOS
# print soup.a
# print soup.p
# print soup.find_all('p')
# print soup.find_all('a')

# RECORREMOS EL LISTADO DE LINKS E IMPRIMIMOS UNO A UNO
# for link in soup.find_all('a'):
#     print link


# FILTRAMOS POR ETIQUETA Y POR VALOR DEL ATRIBUTO CLASS
# print soup.find_all('div', 'entry-date')

# RECORREMOS EL LISTADO DE ELEMENTOS
# for date in soup.find_all('div', 'entry-date'):
    # print date
    # print date.prettify()
    # print date.get_text()


# RECORREMOS EL LISTADO DE TODOS LOS LINKS EN EL HTML
#  print soup.findAll('a')
# for link in soup.findAll('a'):
    # NOS QUEDAMOS CON EN EL VALOR DEL LINK, http://...
#    print(link.get('href'))
   # if not str(link.get('href')).startswith('javascript'):
   #     print(link.get('href'))