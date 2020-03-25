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
from ADT import map as hashmap
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
    #La fecha de cada accidente repetido se va a cambiar por unos milisegundos(no afectará mucho la fecha) para que no hayan datos repetidos    
    #Esta es la estrategía usada para evitar la pérdida de datos por sobreescritura
    # ESTA EN PRUEBA
    catalog["accidentsByDate"] = hashmap.newMap(1830, maptype='CHAINING') # 365 (días) * 5 (años) = 1825 (1830 por si las moscas jaja, también hay años bisiestos y eso)
    
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
    arbol = catalog["accidentsTree"]
    accident = newAccident(row)
    fecha = int(sacarfecha(accident["start_time"]))
    
    DataDistributionByDate(catalog, tabla, row, fecha)

    fecha_encontrada = True
    while fecha_encontrada:
        encontrado = map.contains(arbol, fecha, greater)
        if encontrado:
            fecha += 1
        else:
            catalog["accidentsTree"] = map.put(arbol, fecha, accident, greater)
            hashmap.put(tabla, fecha, accident, greater)
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

def DataDistributionByDate(catalog, tabla, row, fecha):
    dia_fecha = (fecha-18000)//86400
    contiene = hashmap.contains(tabla, dia_fecha, greater)
    if not contiene:
        crear_fecha(tabla, dia_fecha)
    ActualizarFecha(tabla[dia_fecha], row)

def crear_fecha(tabla, dia_fecha):
    datos = {"size":0, "data":None}
    datos["data"] = hashmap.newMap(4, maptype='CHAINING') # 4 severidades de accidente
    hashmap.put(tabla, dia_fecha, datos, greater)

def ActualizarFecha(tabla_fecha, row):
    tabla_fecha["size"] =+ 1
    severidad = int(row["Severity"])
    contiene = hashmap.contains(tabla_fecha, severidad, greater)
    if not contiene:
        crear_severidad(tabla_fecha, row, severidad)
    ActualizarSeveridad(tabla_fecha[severidad], row)

def crear_severidad(tabla_fecha, row, severidad):
    datos = {"size":None, "data":None, "ciudad_mas_accidentada":None, "num_accidentes_ciudad_mas_accidentada":0}
    datos["data"] = hashmap.newMap(1613, maptype='CHAINING') # 3225 ciudades en USA (Aprox.)
    hashmap.put(tabla_fecha, severidad, datos, greater)

def ActualizarSeveridad(tabla_severidad, row):
    tabla_severidad["size"] += 1
    ciudad = row["City"]
    contiene = hashmap.contains(tabla_severidad, ciudad, compareByKey)
    if not contiene:
        crear_ciudad(tabla_severidad, ciudad)
    ActualizarCiudad(tabla_severidad[ciudad])

    if tabla_severidad[ciudad]["accidentes"] > tabla_severidad["num_accidentes_ciudad_mas_accidentada"]:
       tabla_severidad["num_accidentes_ciudad_mas_accidentada"] = tabla_severidad[ciudad]["accidentes"]
       tabla_severidad["ciudad_mas_accidentada"] = ciudad

def crear_ciudad(tabla_severidad, ciudad):
    datos = {"num_accidentes":0}
    hashmap.put(tabla_severidad, ciudad, datos, compareByKey)

def ActualizarCiudad(tabla_ciudad):
    tabla_ciudad["accidentes"] += 1

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