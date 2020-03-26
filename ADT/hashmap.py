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


import config
from DataStructures import mapstructure as ht 



def newMap( capacity=17, prime=109345121, maptype='CHAINING') :
    """
    Crea una tabla de simbolos (map) con capacidad 'capacity'
    Prime es utilizado para la función de hash 
    maptype indica si se utiliza separate chaining o linear probing como mecanismo de solución de colisiones.
    """
    return ht.newMap (capacity, prime, maptype)

    

def put (map, key , value, comparefunction):
    """
    Ingresa una pareja llave,valor a la tabla de hash.  Si la llave ya existe en la tabla, se reemplaza el valor.
    Es necesario proveer una función de comparación para las llaves.
    """
    ht.put (map, key, value, comparefunction)



def get (map, key, comparefunction):
    """
    Retorna la pareja llave, valor, cuya llave sea igual a key.
    Es necesario proveer una función de comparación para las llaves.
    """
    return ht.get (map, key, comparefunction)




def remove (map , key, comparefunction):
    """
    Elimina la pareja llave,valor, donde llave == key.
    Es necesario proveer la función de comparación entre llaves 
    """
    ht.remove (map, key, comparefunction)



def contains (map, key, comparefunction):
    """
    Retorna True si la llave key se encuentra en la tabla de hash o False en caso contrario.  
    Es necesario proveer la función de comparación entre llaves. 
    """
    return ht.contains (map, key, comparefunction)



def size(map):
    """
    Retornar el número de entradas en la tabla de hash.
    """
    return ht.size (map)



def isEmpty(map ):
    """
    Informa si la tabla de hash se encuentra vacia
    """
    return ht.isEmpty (map)



def keySet (map):
    """
    Retorna una lista con todas las llaves de la tabla de hash
    """
    return ht.keySet (map)



def valueSet(map):
    """
    Retorna una lista con todos los valores de la tabla de hash
    """
    return ht.valueSet (map)
