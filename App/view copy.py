import datetime, time

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

print(sacarfecha("1970-01-05 00:00:00"))
print(time.gmtime(0))