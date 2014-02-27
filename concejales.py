__author__ = 'MiguelFG'
import json
import requests
import urllib2
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
# url = 'https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes'
# html = requests.get(url)
# soup = BeautifulSoup(html.content)
# print soup.prettify()
# print soup.get_text()

def request_ssweb_seap_minhap_es():
    response = None

    try:
        req = urllib2.Request("https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes")

        # req.add_header("Connection", "keep-alive")
        # req.add_header("Accept", "*/*")
        # req.add_header("Origin", "https://ssweb.seap.minhap.es")
        # req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36")
        # req.add_header("Content-Type", "application/x-www-form-urlencoded")
        # req.add_header("Referer", "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes")
        # req.add_header("Accept-Encoding", "gzip,deflate,sdch")
        # req.add_header("Accept-Language", "en-US,en;q=0.8,es;q=0.6")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        req.add_header("Cookie", "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; _ga=GA1.3.1489095445.1392115052; BALANCEID=balancer.prophpmodmz01")

        body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D=2&consulta_alcalde%5Bid_entidad%5D=17978"
        body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D=2&consulta_alcalde%5Bid_entidad%5D=49085"

        response = urllib2.urlopen(req, body)


    except urllib2.URLError, e:
        if not hasattr(e, "code"):
            return False
        response = e
    except:
        return False

    return response

def using_requests():
    url = 'https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Cookie': "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; _ga=GA1.3.1489095445.1392115052; BALANCEID=balancer.prophpmodmz01"
    }
    payload = {'body': r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D=2&consulta_alcalde%5Bid_entidad%5D=17978"}
    # response = requests.post(url, headers=headers, data=payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response

response = request_ssweb_seap_minhap_es()
# response = using_requests()
soup = BeautifulSoup(response)
print soup.prettify()
# for td in soup.find_all('td'):
#     print td.get_text()