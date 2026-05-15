import time
from core.partition_algorithms import particion_simple, fuerza_bruta_partition, greedy_partition, local_search_partition
from core.cut_function import calcular_cut
from analysis.metrics import calcular_estadisticas

def ejecutar_algoritmo(algoritmo_func, grafo, k, *args):
    """
    Ejecuta un algoritmo de particionamiento midiendo su tiempo.
    """
    inicio = time.perf_counter()
    if args:
        particion = algoritmo_func(grafo, *args)
    else:
        particion = algoritmo_func(grafo, k)
    fin = time.perf_counter()
    
    tiempo = fin - inicio
    costo = calcular_cut(grafo, particion)
    return particion, costo, tiempo

def comparar_algoritmos(grafo, k=2, iteraciones=1):
    """
    Compara el rendimiento de los algoritmos en el grafo dado.
    """
    resultados = {
        "Simple": {"tiempos": [], "costos": []},
        "Greedy": {"tiempos": [], "costos": []},
        "LocalSearch": {"tiempos": [], "costos": []},
        "FuerzaBruta": {"tiempos": [], "costos": []}
    }
    
    print(f"\nIniciando benchmark (N={grafo.num_nodos}, k={k}, iteraciones={iteraciones})...")
    
    for _ in range(iteraciones):
        # 1. Simple
        p_sim, c_sim, t_sim = ejecutar_algoritmo(particion_simple, grafo, k)
        resultados["Simple"]["tiempos"].append(t_sim)
        resultados["Simple"]["costos"].append(c_sim)
        
        # 2. Greedy
        p_gr, c_gr, t_gr = ejecutar_algoritmo(greedy_partition, grafo, k)
        resultados["Greedy"]["tiempos"].append(t_gr)
        resultados["Greedy"]["costos"].append(c_gr)
        
        # 3. Búsqueda Local (usando Greedy como inicial para un mejor arranque)
        p_ls, c_ls, t_ls = ejecutar_algoritmo(local_search_partition, grafo, k, p_gr)
        resultados["LocalSearch"]["tiempos"].append(t_ls)
        resultados["LocalSearch"]["costos"].append(c_ls)
        
        # 4. Fuerza Bruta (solo si N es pequeño y k=2 para evitar bloqueos)
        if k == 2 and grafo.num_nodos <= 20:
            try:
                p_fb, c_fb, t_fb = ejecutar_algoritmo(fuerza_bruta_partition, grafo, k)
                resultados["FuerzaBruta"]["tiempos"].append(t_fb)
                resultados["FuerzaBruta"]["costos"].append(c_fb)
            except NotImplementedError:
                pass

    # Mostrar resultados estructurados
    print("\n" + "="*75)
    print(f"{'Algoritmo':<15} | {'Mejor Costo':<12} | {'T Promedio (s)':<15} | {'Desviación T':<12}")
    print("-" * 75)
    
    for nombre, datos in resultados.items():
        if not datos["tiempos"]:
            continue
        stats = calcular_estadisticas(datos["tiempos"], datos["costos"])
        print(f"{nombre:<15} | {stats['mejor_costo']:<12.2f} | {stats['tiempo_promedio_s']:<15.6f} | {stats['tiempo_desviacion_s']:<12.6f}")
    print("="*75)
    
    return resultados
