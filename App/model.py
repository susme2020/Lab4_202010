"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import hashmap
from ADT import orderedmap as map
from DataStructures import listiterator as it

import datetime, time


"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    
    catalog = {'booksTree':None,'booksList':None}
    catalog['booksTree'] = map.newMap ("BST")
    catalog['booksList'] = lt.newList("ARRAY_LIST")

    """
    catalog = {'accidentsTree':None,'accidentsList':None, "accidentsHash": None, 'accidentsByDate':None}
    catalog['accidentsTree'] = map.newMap ("RBT")
    catalog['accidentsList'] = lt.newList("ARRAY_LIST")
    catalog['accidentsHash'] = hashmap.newMap(6000011, maptype='PROBING') # 3`000,000 accidentes
    #Esta tabla de Hash se va a usar para encontrar datos repetidos por lo que sólo va a contener un dato por cada accidente: la fecha exacta
    #La fecha de cada accidente repetido se va a cambiar por unos segundos(no afectará mucho la fecha) para que no hayan datos repetidos    
    #Esta es la estrategía usada para evitar la pérdida de datos por sobreescritura
    # ESTA EN PRUEBA
    #catalog["accidentsByDate"] = hashmap.newMap(1831, maptype='CHAINING') # 365 (días) * 5 (años) = 1825 (1830 por si las moscas jaja, también hay años bisiestos y eso)
    catalog["accidentsByDate"] = map.newMap('RBT')
    #catalog["accidentsBySeverity"] = {"size":0, "data": hashmap.newMap(4, maptype='CHAINING')} # 4 Severidades posibles
    #catalog["accidentsByCity"] = {"size":0, "data":hashmap.newMap(1613, maptype='CHAINING'), "ciudad_mas_accidentada":None, "num_accidentes_ciudad_mas_accidentada":0} # 3225 ciudades en USA (Aprox.)

    return catalog


def newBook (row):
    """
    Crea una nueva estructura para almacenar un libro 
    """
    book = {"book_id": row['book_id'], "title":row['title'], "average_rating":row['average_rating'], "ratings_count":row['ratings_count']}
    return book

def newAccident (row):
    """
    Crea una nueva estructura para almacenar un accidente
    """
    accident = {"accident_id": row["ID"], "severity": int(row["Severity"]), "start_time": row["Start_Time"], "end_time": row["End_Time"], "start_lat": row["Start_Lat"], "start_lng": row["Start_Lng"]}
    return accident

def addBookList (catalog, row):
    """
    Adiciona libro a la lista
    """
    books = catalog['booksList']
    book = newBook(row)
    lt.addLast(books, book)

def addAccidentList (catalog, row):
    """
    Adiciona un accidente a la lista
    """
    accidents = catalog['accidentsList']
    accident = newAccident(row)
    lt.addLast(accidents, accident)

def addBookMap (catalog, row):
    """
    Adiciona libro al map con key=title
    """
    book = newBook(row)
    #catalog['booksTree'] = map.put(catalog['booksTree'], int(book['book_id']), book, greater)
    catalog['booksTree']  = map.put(catalog['booksTree'] , book['title'], book, greater)

def addAccidentMap (catalog, row):
    """
    Adiciona accidente al map y a la tabla hash
    """
    #catalog['booksTree'] = map.put(catalog['booksTree'], int(book['book_id']), book, greater)
    #catalog['booksTree']  = map.put(catalog['booksTree'] , book['title'], book, greater)
    
    #Se ingresa cada accidente a la tabla hash con un único valor/llave : su fecha exacta

    tabla = catalog["accidentsByDate"]
    tabla_todos = catalog["accidentsHash"]
    arbol = catalog["accidentsTree"]
    accident = newAccident(row)
    fecha = int(sacarfecha(accident["start_time"]))

    dia_fecha = int(((fecha-18000)//86400)-16801)
    DataDistributionByDate(catalog, tabla, row, dia_fecha)

    fecha_encontrada = True
    while fecha_encontrada:
        encontrado = map.contains(arbol, fecha, greater)
        if encontrado:
            fecha += 1
        else:
            catalog["accidentsTree"] = map.put(arbol, fecha, accident, greater)
            hashmap.put(tabla_todos, fecha, accident, greater)
            fecha_encontrada = False
    

def sacarfecha(start_time):
    llave = start_time
    llave = llave.replace(" ", "")
    llave = llave.split("-")
    anio = int(llave[0])
    mes = int(llave[1])
    dia = int(llave[2][0:2])
    hora = llave[2][2:10]
    hora = hora.split(":")
    horas = int(hora[0])
    minuto = int(hora[1])
    segundo = int(hora[2])
    fecha = time.mktime(datetime.datetime(anio, mes, dia, horas, minuto, segundo, 0).timetuple())

    return fecha

def DataDistributionByDate(catalog, tabla, row, dia_fecha):
    contiene_fecha = map.get(tabla, dia_fecha, greater)
    if contiene_fecha == None:
        datos = {} # 4 Severidades posibles
        info = {"size":0, "data": hashmap.newMap(1613, maptype='CHAINING'), "num_accidentes_ciudad_mas_accidentada": 0, "ciudad_mas_accidentada": None, "num_ciudades_accidentadas": 0, "ciudades_accidentadas":[]}
        datos[1] = info
        datos[2] = info
        datos[3] = info
        datos[4] = info
        catalog["accidentsByDate"] = map.put(catalog["accidentsByDate"], dia_fecha, {"size":0,"data":datos}, greater)
        contiene_fecha = map.get(catalog["accidentsByDate"], dia_fecha, greater)
    contiene_fecha["size"] += 1
    contiene_fecha["data"][int(row["Severity"])]["size"] += 1
    contiene_ciudad = hashmap.get(contiene_fecha["data"][int(row["Severity"])]["data"], row["City"], compareByKey)
    if contiene_ciudad == None:
        datos = {"nombre":row["City"], "accidentes":0}
        hashmap.put(contiene_fecha["data"][int(row["Severity"])]["data"], row["City"], datos, compareByKey)
        contiene_ciudad = hashmap.get(contiene_fecha["data"][int(row["Severity"])]["data"], row["City"], compareByKey)
        contiene_fecha["data"][int(row["Severity"])]["num_ciudades_accidentadas"] += 1
        contiene_fecha["data"][int(row["Severity"])]["ciudades_accidentadas"].append(row["City"])

    contiene_ciudad["value"]["accidentes"] += 1
    if contiene_ciudad["value"]["accidentes"] > contiene_fecha["data"][int(row["Severity"])]["num_accidentes_ciudad_mas_accidentada"]:
        contiene_fecha["data"][int(row["Severity"])]["num_accidentes_ciudad_mas_accidentada"] = contiene_ciudad["value"]["accidentes"]
        contiene_fecha["data"][int(row["Severity"])]["ciudad_mas_accidentada"] = contiene_ciudad["value"]["nombre"]

# Funciones de consulta


def getBookMap (catalog, bookTitle):
    """
    Retorna el libro desde el mapa a partir del titulo (key)
    """
    return map.get(catalog['booksTree'], bookTitle, greater)

def getAccidentMap (catalog, fecha):
    """
    Retorna el accidente desde el mapa a partir de la fecha (key)
    """
    return map.get(catalog['accidentsTree'], fecha, greater)

def rankBookMap (catalog, bookTitle):
    """
    Retorna la cantidad de llaves menores (titulos) dentro del arbol
    """
    return map.rank(catalog['booksTree'], bookTitle, greater)

def rankAccidentMap (catalog, fecha):
    """
    Retorna la cantidad de accidentes que ocurrieron antes que la fecha obtenida por parámetro
    """
    return map.rank(catalog['accidentsTree'], fecha, greater)

def DaterankAccidentMap(catalog, fecha1, fecha2):
    """
    Retorna un diccionario con la cantidad de accidentes en el rango de fechas (desde fecha #1 a fecha #2) y con el número de accidentes por ciudad en ese intervalo.
    """
    info = {}
    accidentes_totales = 0
    ciudades = {}
    for fecha in range(fecha1, fecha2 + 1):
        for severidad in range(1, 5):
            accidentes = map.get(catalog["accidentsByDate"], fecha, greater)
            if accidentes != None:
                accidentes_totales += accidentes["size"]
                ciudades_totales = accidentes["data"][severidad]["data"]
                if ciudades_totales != None:
                    llaves_ciudades = accidentes["data"][severidad]["ciudades_accidentadas"]
                    for llave in llaves_ciudades:
                        if ciudades.get(llave) == None:
                            get = hashmap.get(ciudades_totales, llave, compareByKey)
                            ciudades[llave] = get["value"]["accidentes"]
                        else:
                            get = hashmap.get(ciudades_totales, llave, compareByKey)
                            ciudades[llave] += get["value"]["accidentes"]
    info["accidentes_totales"] = accidentes_totales
    info["ciudades"] = ciudades
    return info

def selectBookMap (catalog, pos):
    """
    Retorna la operación select (titulos) dentro del arbol
    """
    return map.select(catalog['booksTree'], pos) 

def selectAccidentMap (catalog, pos):
    """
    Retorna la operación select (fecha) dentro del arbol
    """
    return map.select(catalog['accidentsTree'], pos)

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'])  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1