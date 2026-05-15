import csv

def leer_matriz(ruta):
    matriz = []

    with open(ruta, newline='') as archivo:
        lector = csv.reader(archivo)

        for fila in lector:
            matriz.append([int(valor) for valor in fila])

    return matriz