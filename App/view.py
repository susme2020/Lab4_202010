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
import sys
import controller 
import csv
from ADT import list as lt
from ADT import map as hashmap
from ADT import orderedmap as map
import sys

from DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Laboratorio 4")
    print("1- Cargar información")
    print("2- Buscar accidente por llave (fecha)")
    print("3- Consultar cuantos accidentes hubo antes a una fecha - (rank)")
    print("4- Consultar accidente por posición")
    print("5- Consultar total de accidentes ocurridos en una fecha específica. Estos totales se presentarán divididos entre las diferentes severidades de accidente posibles (1 - 4) y se mostrará la ciudad más accidentada por severidad en la fecha dada.") 
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga los datos en la estructura de datos
    """
    controller.loadData(catalog)

def pedir_fecha():
    anio = int(input("Año del accidente: "))
    mes = int(input("Mes(#) del accidente: "))
    if mes < 10:
        mes = "0"+str(mes)
    dia = int(input("Día(#) del accidente: "))
    if dia < 10:
        dia = "0"+str(dia)
    hora = int(input("Hora (en formato militar): "))
    if hora < 10:
        hora = "0"+str(hora)
    minuto = int(input("Minuto: "))
    if minuto < 10:
        minuto = "0"+str(minuto)
    segundo = int(input("Segundo: "))
    if segundo < 10:
        segundo = "0"+str(segundo)
    fecha = str(anio)+"-"+str(mes)+"-"+str(dia)+str(hora)+":"+str(minuto)+":"+str(segundo)
    fecha = controller.sacarfecha(fecha)
    return fecha

"""
Menu principal
"""
def main():
    datos_cargados = False
    while True:
        printMenu() 
        inputs =input('Seleccione una opción para continuar\n')
        if int(inputs[0])==1: # 1- Cargar información

            print("Cargando información de los archivos ....")
            print("Recursion Limit:",sys.getrecursionlimit())
            catalog = initCatalog ()
            loadData (catalog)
            """
            print ('Arbol Libros cargados: ' + str(map.size(catalog['booksTree'])))
            print ('Lista libros cargados: ' + str(lt.size(catalog['booksList'])))
            print ('Altura arbol: ' + str(map.height(catalog['booksTree'])))
            """
            print ('Arbol Accidentes cargados: ' + str(map.size(catalog['accidentsTree'])))
            print ('Hash Accidentes cargados: ' + str(hashmap.size(catalog['accidentsHash'])))
            print ('Lista Accidentes cargados: ' + str(lt.size(catalog['accidentsList'])))
            print ('Altura arbol: ' + str(map.height(catalog['accidentsTree'])))

            datos_cargados = True
            
        elif int(inputs[0])==2: # 2- Buscar accidente por llave (fecha)
            if datos_cargados:
                fecha = pedir_fecha()
                accidente = controller.getAccidentMap(catalog,fecha)

                if accidente:
                    print("Accidente encontrado:\nID: ", accidente["accident_id"], "\nTiempo de inicio: ", accidente["start_time"], "\nTiempo de finalización: ", accidente["end_time"], "\nSeveridad tipo ", accidente["severity"], "\nLatitud ", accidente["start_lat"], "\nLongitud ", accidente["start_lng"])
                else:
                    print("Accidente No encontrado")
            else:
                print("No ha cargado los datos")    

        elif int(inputs[0])==3: # 3- Consultar cuantos accidentes hubo antes a una fecha - (rank)
            if datos_cargados:
                print("Para consultar tiene que ingresar una fecha")
                fecha = pedir_fecha()
                rank = controller.rankAccidentMap(catalog,fecha)
                print("Ocurrieron ", rank, " accidentes antes (rank) de la fecha ingresada")
            else:
                print("No ha cargado los datos")

        elif int(inputs[0])==4: # 4- Consultar accidente por posición
            if datos_cargados:
                pos = int(input("Posición del k-esimo accidente del mapa (select) a obtener: "))
                accidente = controller.selectAccidentMap(catalog, pos)
                if accidente:
                    print("Accidente en posición:",pos,":\nID: ", accidente["accident_id"], "\nTiempo de inicio: ", accidente["start_time"], "\nTiempo de finalización: ", accidente["end_time"], "\nSeveridad tipo ", accidente["severity"], "\nLatitud : ", accidente["start_lat"], "\nLongitud : ", accidente["start_lng"])
                else:
                    print("Accidente no encotrado en posicion: ",pos)
            else:
                print("No ha cargado los datos")

        elif int(inputs[0])==5: # 5- Consultar total de accidentes ocurridos en una fecha específica. Estos totales se presentarán divididos entre las diferentes severidades de accidente posibles (1 - 4) y se mostrará la ciudad más accidentada por severidad en la fecha dada.
            if datos_cargados:
                print("Para ejecutar esta opción debe proporcionar una fecha (año, mes, día). Esta fecha debe estar dentro del rango de años de los datos cargados. No tiene ingresar datos de hora, minuto o segundo ya que no se tendrán en cuenta.")
                fecha = (pedir_fecha()-18000)//86400
                
                print("En la fecha se presentaron ", catalog["accidentsByDate"][fecha]["size"], " accidentes.\n")
                print("SEVERIDAD 1")
                print("Para la severidad 1 se presentaron ", catalog["accidentsByDate"][fecha][1]["size"], " accidentes en la fecha ingresada y la ciudad que más accidentes tuvo de este tipo fue: ", catalog["accidentsByDate"][fecha][1]["ciudad_mas_accidentada"])

                print("En la fecha se presentaron ", catalog["accidentsByDate"][fecha]["size"], " accidentes.\n")
                print("SEVERIDAD 2")
                print("Para la severidad 2 se presentaron ", catalog["accidentsByDate"][fecha][2]["size"], " accidentes en la fecha ingresada y la ciudad que más accidentes tuvo de este tipo fue: ", catalog["accidentsByDate"][fecha][2]["ciudad_mas_accidentada"])

                print("En la fecha se presentaron ", catalog["accidentsByDate"][fecha]["size"], " accidentes.\n")
                print("SEVERIDAD 3")
                print("Para la severidad 3 se presentaron ", catalog["accidentsByDate"][fecha][3]["size"], " accidentes en la fecha ingresada y la ciudad que más accidentes tuvo de este tipo fue: ", catalog["accidentsByDate"][fecha][3]["ciudad_mas_accidentada"])

                print("En la fecha se presentaron ", catalog["accidentsByDate"][fecha]["size"], " accidentes.\n")
                print("SEVERIDAD 4")
                print("Para la severidad 4 se presentaron ", catalog["accidentsByDate"][fecha][4]["size"], " accidentes en la fecha ingresada y la ciudad que más accidentes tuvo de este tipo fue: ", catalog["accidentsByDate"][fecha][4]["ciudad_mas_accidentada"])
            else:
                print("No ha cargado los datos")

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    sys.setrecursionlimit(11000)
    main()