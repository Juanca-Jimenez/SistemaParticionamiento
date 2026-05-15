from core.csv_reader import leer_matriz
from core.validator import es_cuadrada
from core.partition_algorithms import particion_simple
from core.cut_function import calcular_cut

matriz = leer_matriz("datasets/small/matriz1.csv")

print("Matriz:")
print(matriz)

print("¿Es cuadrada?")
print(es_cuadrada(matriz))

g1, g2 = particion_simple(len(matriz))

print("Grupo 1:", g1)
print("Grupo 2:", g2)

costo = calcular_cut(matriz, g1, g2)

print("Costo total:", costo)