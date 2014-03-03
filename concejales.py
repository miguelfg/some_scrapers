import requests
import csv
import scraperwiki
from bs4 import BeautifulSoup

# FUNCION QUE:
# RECIBE: LISTADO DE CONCEJALES DENTRO DEL SOUP
# GUARDA EL LISTADO EN UN FICHERO .CSV
# NO DEVUELVE NADA
def save2csv(concejales):
    fOUTPUT = "all_concejales.csv"
    oFile = open(fOUTPUT, "wb")
    writer = csv.writer(oFile, delimiter=',')
    writer.writerow(["ID", "PROVINCE", "INE_CODE", "NAME", "LAST_NAME", "PARTY",  "POSITION"])
    for row in concejales:
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            print row
            pass
    print "csv generated:" + fOUTPUT


# FUNCION QUE:
# RECIBE: LISTADO DE CONCEJALES DENTRO DEL SOUP
# GUARDA EL LISTADO EN LA BASE DE DATOS
# NO DEVUELVE NADA
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


# FUNCION QUE:
# RECIBE: HTML - SOUP
# DEVUELVE: LISTADO DE CODIGOS DE MUNICIPIO
def getAllMunicipalitiesFromSoup(soup):
    # FILTRAMOS POR ETIQUETA 'OPTION'
    options = soup.find_all('option')
    municipalities = []

    for opt in options[:]:
        # SI LA OPCION ESTA VACIA PASAMOS
        if '--' in opt.get_text():
            continue
        # RECOGEMOS EL INE_CODE Y SU NOMBRE
        ine_code = opt.get('value')
        name = opt.get_text()

        # LO AGREGAMOS A LA LISTA
        municipalities.append([ine_code, name])

    return municipalities


# FUNCION QUE:
# RECIBE: HTML - SOUP
# DEVUELVE: LISTADO DE CONCEJALES DENTRO DEL SOUP
def soup2Concejales(province, ine_code, soup):
    concejales = []
    # SELECCIONAMOS LAS FILAS DE LA TABLA E ITERAMOS
    for tr in soup.find_all('tr'):
        concejal = []
        # SELECCIONAMOS LAS COLUMNAS DE CADA FILA E ITERAMOS
        for td in tr.find_all('td'):
            concejal.append(td.get_text())
            #print td.get_text()
        # SI COLUMNA NO ESTA VACIA, INCLUIMOS CONCEJAL EN LA LISTA
        if concejal:
            concejales.append([province, ine_code] + concejal)
        #print "================"

    return concejales

# PRIMERA WEB CON EL LISTADO DE MUNICIPIOS POR PROVINCIA
def using_requests_1(province):
        # PREPARAMOS EL REQUEST
        url = "https://ssweb.seap.minhap.es/portalEELL/consulta_alcaldes/getEntidades/provincia/" + str(province)
        cookies = dict(Cookie = "portalEELL=uos1gss8sr9e3scgo16m9pt1o7; ssoEELL=25fma5i9cabtduqcvaam8bs2q7; BALANCEID=balancer.prophpmodmz01; _ga=GA1.3.1489095445.1392115052")

        # VISITA WEB Y GUARDAMOS LA RESPUESTA
        response = requests.get(url, cookies=cookies, verify=False)

        # GUARDAMOS LA COOKIE QUE NOS DEVUELVE
        cookie = response.headers['set-cookie']

        soup = BeautifulSoup(response.text)
        # LLAMAMOS A LA FUNCION QUE NOS LIMPIA EL HTML Y
        # NOS DEVUELVE EL LISTADO DE CODIGOS DE MUNICIPIO
        municipalities = getAllMunicipalitiesFromSoup(soup)
        concejales_provincia = []
        for mun in municipalities:
            # VISITAMOS LA SEGGUNDA WEB
            concejales_municipio = using_requests_2(province, mun[0], cookie)

            # ACUMULAMOS LOS CONCEJALES DEL MUNICIPIO A LOS ACUMULADOS DE TODA LA PROVINCIA
            concejales_provincia = concejales_provincia + concejales_municipio

        # DEVOLVEMOS EL LISTADO DE TODOS LOS CONCEJALES EN LA PROVINCIA
        return concejales_provincia

def using_requests_2(province, ine_code, cookie):
    # PREPARAMOS EL REQUEST
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
    # VISITA WEB Y GUARDAMOS LA RESPUESTA
    soup = BeautifulSoup(response.text)

    # LLAMAMOS A LA FUNCION QUE NOS LIMPIA EL HTML Y
    # NOS DEVUELVE EL LISTADO DE CONCEJALES DEL MUNICIPIO
    concejales_municipio = soup2Concejales(province, ine_code, soup)

    # DEVOLVEMOS EL LISTADO DE TODOS LOS CONCEJALES DEL MUNICIPIO
    return concejales_municipio


# MAIN
# AQUI EMPIEZA
all_concejales = []
# for province in range(1, 3):
# BUCLE QUE RECORRE EL NUMERO DE PROVINCIAS
for province in range(1, 51):
    # VISITAMOS LA PRIMERA WEB
    concejales_provinciales = using_requests_1(province)

    # ACUMULAMOS LOS CONCEJALES ENCONTRADOS
    all_concejales = all_concejales + concejales_provinciales

    print len(all_concejales)

# save all data
#save2database(all_concejales)
save2csv(all_concejales)


print "Finished"