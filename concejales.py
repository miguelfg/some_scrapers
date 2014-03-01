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

def using_urllib_1(province=1):
    try:
        req = urllib2.Request("https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes/getEntidades/provincia/" + str(province))
        req.add_header("Referer", "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes")
        cookie = "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; BALANCEID=balancer.prophpmodmz01; _ga=GA1.3.1489095445.1392115052"
        req.add_header("Cookie", cookie)

        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response)
        options = soup.find_all('option')
        for opt in options[:3]:
            if '--' in opt.get_text():
                continue
            #print opt.get('value'), opt.get_text()
            ine_code = opt.get('value')
            using_urllib_2(province, ine_code, cookie=cookie)

    except urllib2.URLError, e:
        if not hasattr(e, "code"):
            return False
        response = e
    except:
        return False


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
        for tr in soup.find_all('tr'):
            for td in tr.find_all('td'):
                print td.get_text()
            print "================"


    except urllib2.URLError, e:
        if not hasattr(e, "code"):
            return False
        response = e
        print "Error"
        print response
    except:
        print "Error"
        return False

    return response

def using_requests_1(province):
        url = "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes/getEntidades/provincia/" + str(province)
        response = requests.get(url, verify=False)
        cookie = response.headers['set-cookie']
        soup = BeautifulSoup(response.text)
        options = soup.find_all('option')
        for opt in options[:3]:
            if '--' in opt.get_text():
                continue
            #print opt.get('value'), opt.get_text()
            ine_code = opt.get('value')
            using_requests_2(province, ine_code, cookie)

def using_requests_2(province, ine_code, cookie):
    url = 'https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               "Referer": "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes",
               #'Cookie': cookie
    }
    #cookies = dict(Cookie = r"portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; _ga=GA1.3.1489095445.1392115052; BALANCEID=balancer.prophpmodmz01")
    cookies = dict(
                    BALANCEID=r"balancer.prophpmodmz01",
                    path=r"/",
                    domain=r"ssweb.seap.minhap.es",
                    #portalEELL=r"uos1gss8sr9e3scgo16m9pt1o7",
                    #ssoEELL=r"25fma5i9cabtduqcvaam8bs2q7",
                    #_ga=r"GA1.3.1489095445.1392115052",
    )
    body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D="+str(province)+"&consulta_alcalde%5Bid_entidad%5D="+str(ine_code)
    #body = r"consulta_alcalde%5B_csrf_token%5D=fc69f17c058187dc3b02a79c5a02d6bb&consulta_alcalde%5Bid_provincia%5D=2&consulta_alcalde%5Bid_entidad%5D=17978"
    #payload = {'body': body}

    response = requests.post(url,
                             headers=headers,
                             cookies=cookies,
                             data=body,
                             verify=False)
    print response.status_code
    print response.headers['set-cookie']
    print response.text
    #print response.headers

#lib REQUESTS
response = using_requests_1(3)

#lib URLLIB2
#for province in range(2):
#    response = using_urllib_1(province)

