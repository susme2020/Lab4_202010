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
import model
import csv
from ADT import list as lt
from ADT import hashmap as hashmap

from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)



def compareratings (movie1, movie2):
    return ( float(movie1['vote_average']) > float(movie2['vote_average']))


# Funciones para la carga de datos 

def loadBooks (catalog, sep=','):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea un arbol de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    booksfile = cf.data_dir + 'GoodReads/books.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(booksfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona el libro a la lista de libros
            model.addBookList(catalog, row)
            # Se adiciona el libro al mapa de libros (key=title)
            model.addBookMap(catalog, row)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga libros:",t1_stop-t1_start," segundos")

def loadAccidents (catalog, sep=','):
    """
    Carga los accidentes del archivo. Se crea un árbol con las fechas como llaves
    """
    t1_start = process_time() #tiempo inicial
    #accidentsfile = cf.data_dir + 'Accidents/us_accidents_dis_2016.csv'
    #accidentsfile = cf.data_dir + 'Accidents/us_accidents_small.csv'
    accidentsfile = cf.data_dir + 'Accidents/US_Accidents_Dec19.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(accidentsfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader:
            # Se adiciona el libro al mapa de libros (key=title)
            model.addAccidentMap(catalog, row)
            # Se adiciona el libro a la lista de libros
            model.addAccidentList(catalog, row)
            # Se adiciona el SÓLAMENTE la llave a la tabla de hash de los accidentes
            # Esto ocurre dentro de la función que ingresa los datos al árbol de accidentes

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga accidentes:",t1_stop-t1_start," segundos")

def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    #loadBooks(catalog)
    loadAccidents(catalog)  

# Funciones llamadas desde la vista y enviadas al modelo


def getBookMap(catalog, bookTitle):
    t1_start = process_time() #tiempo inicial
    #book=model.getBookInList(catalog, bookTitle)
    book=model.getBookMap(catalog, bookTitle) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro:",t1_stop-t1_start," segundos")   
    if book:
        return book
    else:
        return None

def getAccidentMap(catalog, fecha):
    t1_start = process_time() #tiempo inicial
    accidente = model.getAccidentMap(catalog, fecha) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar accidente:",t1_stop-t1_start," segundos")   
    if accidente:
        return accidente
    else:
        return None

def rankBookMap(catalog, bookTitle):
    t1_start = process_time() #tiempo inicial
    rank=model.rankBookMap(catalog, bookTitle)  
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro (rank):",t1_stop-t1_start," segundos")   
    return rank

def rankAccidentMap(catalog, fecha):
    t1_start = process_time() #tiempo inicial
    rank=model.rankAccidentMap(catalog, fecha)  
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar accidente (rank):",t1_stop-t1_start," segundos")   
    return rank
    
def DaterankAccidentMap(catalog, fecha1, fecha2):
    t1_start = process_time() #tiempo inicial
    rank=model.DaterankAccidentMap(catalog, fecha1, fecha2)  
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar accidentes en un rango de fechas:",t1_stop-t1_start," segundos")   
    return rank

def selectBookMap(catalog, pos):
    t1_start = process_time() #tiempo inicial
    rank=model.selectBookMap(catalog, pos) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar libro (rank):",t1_stop-t1_start," segundos")   
    return rank

def selectAccidentMap(catalog, pos):
    t1_start = process_time() #tiempo inicial
    rank=model.selectAccidentMap(catalog, pos) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución buscar accidente (rank):",t1_stop-t1_start," segundos")   
    return rank

def sacarfecha(fecha):
    return model.sacarfecha(fecha)

def greater(key1, key2):
    return model.greater(key1, key2)