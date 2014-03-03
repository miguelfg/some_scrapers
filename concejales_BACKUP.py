import requests
import json
import requests
import urllib2
import scraperwiki
from bs4 import BeautifulSoup


def save2database(concejales):
    id = 1
    for concejal in concejales[:6]:
        if concejal[2] == 'Alcalde':
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id,
                                                              "province":concejal[0],
                                                              "ine_code": concejal[1],
                                                              "nombre": concejal[2],
                                                              "apellidos": concejal[3],
                                                              "partido": concejal[5],
                                                              "cargo": concejal[4],
            })
        else:
            scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id,
                                                              "province":concejal[0],
                                                              "ine_code": concejal[1],
                                                              "nombre": concejal[2],
                                                              "apellidos": concejal[3],
                                                              "partido": concejal[4],
                                                              "cargo": concejal[5],
            })

        id +=1


def getAllMunicipalitiesFromSoup(soup):
    options = soup.find_all('option')
    municipalities = []
    for opt in options[:]:
        if '--' in opt.get_text():
            continue
        ine_code = opt.get('value')
        name = opt.get_text()
        municipalities.append([ine_code, name])

    return municipalities


def soup2Concejales(province, ine_code, soup):
    concejales = []
    for tr in soup.find_all('tr'):
        concejal = []
        for td in tr.find_all('td'):
            concejal.append(td.get_text())
            #print td.get_text()
        if concejal:
            concejales.append([province, ine_code] + concejal)
        #print "================"

    return concejales


def using_urllib_1(province=1):
    try:
        req = urllib2.Request("https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes/getEntidades/provincia/" + str(province))
        req.add_header("Referer", "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes")
        cookie = "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; BALANCEID=balancer.prophpmodmz01; _ga=GA1.3.1489095445.1392115052"
        req.add_header("Cookie", cookie)

        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response)
        municipalities = getAllMunicipalitiesFromSoup(soup)
        for mun in municipalities:
            using_urllib_2(province, mun[0], cookie=cookie)

    except urllib2.URLError, e:
        raise
    except:
        raise


    return response

def using_urllib_2(province=2, ine_code=17978, cookie=''):
    try:
        req = urllib2.Request("https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        #req.add_header("Cookie", cookie)
        req.add_header("Cookie", "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; _ga=GA1.3.1489095445.1392115052; BALANCEID=balancer.prophpmodmz01")
        body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D="+str(province)+"&consulta_alcalde%5Bid_entidad%5D="+str(ine_code)

        response = urllib2.urlopen(req, body)
        soup = BeautifulSoup(response)
        concejales = soup2Concejales(soup)
        print concejales

    except urllib2.URLError, e:
        raise
    except:
        raise

    return response


def using_requests_1(province):
        url = "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes/getEntidades/provincia/" + str(province)
        cookies = dict(Cookie = "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; BALANCEID=balancer.prophpmodmz01; _ga=GA1.3.1489095445.1392115052")

        response = requests.get(url, cookies=cookies, verify=False)

        cookie = response.headers['set-cookie']
        soup = BeautifulSoup(response.text)
        municipalities = getAllMunicipalitiesFromSoup(soup)
        concejales_provincia = []
        for mun in municipalities:
            concejales_municipio = using_requests_2(province, mun[0], cookie)
            concejales_provincia = concejales_provincia + concejales_municipio

        return concejales_provincia

def using_requests_2(province, ine_code, cookie):
    url = 'https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               "Referer": "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes",
               "Cookie": "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; _ga=GA1.3.1489095445.1392115052; BALANCEID=balancer.prophpmodmz01"
               #'Cookie': cookie
    }
    body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D="+str(province)+"&consulta_alcalde%5Bid_entidad%5D="+str(ine_code)

    response = requests.get(url,
                             headers=headers,
                             #cookies=dict(Cookie=cookie),
                             params=body,
                             verify=False)
    soup = BeautifulSoup(response.text)
    concejales_municipio = soup2Concejales(province, ine_code, soup)
    return concejales_municipio

#lib URLLIB2
#for province in range(2):
#    response = using_urllib_1(province)

#lib REQUESTS
all_concejales = []
for province in range(1, 3):
    print province, " ===================== "
    concejales_provinciales = using_requests_1(province)
    all_concejales = all_concejales + concejales_provinciales
    print len(all_concejales)
#save2database(all_concejales)


print "Finished"