import sys
import os

# Ajustar el path para permitir la ejecución directa desde la raíz o desde src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.csv_reader import leer_matriz
from core.validator import validar_matriz
from core.partition_algorithms import particion_simple, greedy_partition, fuerza_bruta_partition, local_search_partition
from core.cut_function import calcular_cut
from core.graph import Grafo
from analysis.benchmarks import comparar_algoritmos

def main():
    print("=" * 70)
    print("SISTEMA DE PARTICIONAMIENTO ÓPTIMO DE GRAFOS".center(70))
    print("=" * 70)
    
    # 1. Solicitar CSV
    ruta = input("\n[1] Ingrese la ruta del archivo CSV (ej: datasets/small/matriz1.csv): ").strip()
    
    # 2. Cargar matriz con manejo de errores (Instrucción 11)
    try:
        matriz = leer_matriz(ruta)
        print(" [OK] Matriz cargada exitosamente.")
    except Exception as e:
        print(f"\n[ERROR] Error crítico al cargar el archivo: {e}")
        return
        
    # 3. Validar matriz
    valida, msj = validar_matriz(matriz)
    if not valida:
        print(f"\n[ERROR] Error de validación de la estructura del grafo: {msj}")
        return
    print(" [OK] Estructura matricial validada.")
    
    grafo = Grafo(matriz)
    print(f"     -> Componentes (V) detectados: {grafo.num_nodos}")
    
    # 4. Solicitar particiones k
    try:
        k = int(input("\n[2] Ingrese el número de particiones (k) deseado: "))
        if k < 2 or k > grafo.num_nodos:
            raise ValueError(f"El valor de k debe estar en el rango [2, {grafo.num_nodos}].")
    except ValueError as e:
        print(f"\n[ERROR] Entrada inválida: {e}")
        return

    print("\n" + "=" * 70)
    print("RESULTADOS DEL PARTICIONAMIENTO".center(70))
    print("=" * 70)

    # 5 & 6. Ejecutar algoritmos y mostrar resultados
    p_sim = particion_simple(grafo, k)
    print(f"\n[+] Partición Simple")
    print(f"    Costo Cut: {calcular_cut(grafo, p_sim):.2f}")
    
    p_greedy = greedy_partition(grafo, k)
    print(f"\n[+] Heurística Greedy")
    print(f"    Costo Cut: {calcular_cut(grafo, p_greedy):.2f}")
    
    p_local = local_search_partition(grafo, p_greedy) # Inicia desde la greedy
    print(f"\n[+] Búsqueda Local (refinando Greedy)")
    print(f"    Costo Cut: {calcular_cut(grafo, p_local):.2f}")
    
    if k == 2 and grafo.num_nodos <= 20:
        print("\n[+] Algoritmo Exacto (Fuerza Bruta O(V!))")
        try:
            p_fb = fuerza_bruta_partition(grafo, k)
            print(f"    Costo Cut: {calcular_cut(grafo, p_fb):.2f} (Óptimo garantizado)")
        except NotImplementedError as e:
            print(f"    Omitido: {e}")
    else:
        print("\n[!] Fuerza Bruta omitido (requiere k=2 y N<=20 para evitar bloqueo).")

    # 7. Mostrar métricas (Módulo de Benchmarks)
    print("\n" + "=" * 70)
    print("ANÁLISIS DE RENDIMIENTO".center(70))
    print("=" * 70)
    respuesta = input("\n[3] ¿Desea ejecutar un benchmark estadístico completo? (s/n): ").strip().lower()
    
    if respuesta == 's':
        try:
            iteraciones = int(input("    Ingrese el número de iteraciones para la muestra (ej: 10): "))
        except ValueError:
            iteraciones = 1
        comparar_algoritmos(grafo, k, iteraciones=iteraciones)
    
    print("\nEjecución finalizada. Saliendo del sistema...")

if __name__ == "__main__":
    main()