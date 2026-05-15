import csv
import random
import os

def generar_matriz_aleatoria(n, max_peso=20):
    """
    Genera una matriz simétrica aleatoria para simular 
    un grafo de dependencias de sistemas distribuidos.
    """
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            peso = random.randint(1, max_peso)
            matriz[i][j] = peso
            matriz[j][i] = peso
    return matriz

def guardar_matriz_csv(matriz, ruta):
    """
    Guarda la matriz de adyacencia en un archivo CSV.
    Crea los directorios necesarios si no existen.
    """
    directorio = os.path.dirname(ruta)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
        
    with open(ruta, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(matriz)
