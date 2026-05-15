import pytest
import sys
import os

# Ajustar el path para que los módulos dentro de src se encuentren entre sí (core.x)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.csv_reader import leer_matriz
from core.validator import validar_matriz
from core.graph import Grafo
from core.cut_function import calcular_cut
from core.partition_algorithms import particion_simple, greedy_partition, fuerza_bruta_partition, local_search_partition

def test_validar_matriz_correcta():
    matriz = [[0, 5, 1], [5, 0, 2], [1, 2, 0]]
    valida, msg = validar_matriz(matriz)
    assert valida == True

def test_validar_matriz_asimetrica():
    matriz = [[0, 1], [5, 0]]
    valida, msg = validar_matriz(matriz)
    assert valida == False
    assert "no es simétrica" in msg

def test_calcular_cut():
    matriz = [[0, 5, 1], [5, 0, 2], [1, 2, 0]]
    grafo = Grafo(matriz)
    particiones = [[0], [1, 2]]
    # Costo: w(0,1) + w(0,2) = 5 + 1 = 6
    costo = calcular_cut(grafo, particiones)
    assert costo == 6.0

def test_algoritmos_generan_k_grupos():
    matriz = [[0, 5, 1], [5, 0, 2], [1, 2, 0]]
    grafo = Grafo(matriz)
    k = 2
    
    assert len(particion_simple(grafo, k)) == k
    assert len(greedy_partition(grafo, k)) == k
    assert len(fuerza_bruta_partition(grafo, k)) == k

def test_busqueda_local_mejora_o_mantiene():
    matriz = [[0, 10, 1, 1], [10, 0, 1, 1], [1, 1, 0, 10], [1, 1, 10, 0]]
    grafo = Grafo(matriz)
    
    # Partición mala intencional
    p_mala = [[0, 2], [1, 3]]
    costo_malo = calcular_cut(grafo, p_mala)
    
    p_mejorada = local_search_partition(grafo, p_mala)
    costo_mejorado = calcular_cut(grafo, p_mejorada)
    
    assert costo_mejorado <= costo_malo
