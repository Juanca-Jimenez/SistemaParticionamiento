import csv
import os

def leer_matriz(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")

    matriz = []
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for i, fila in enumerate(lector):
            fila_numerica = []
            for j, valor in enumerate(fila):
                try:
                    fila_numerica.append(float(valor))
                except ValueError:
                    raise ValueError(f"Valor no numérico '{valor}' en fila {i}, columna {j}.")
            matriz.append(fila_numerica)

    return matriz