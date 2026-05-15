import itertools
from core.cut_function import calcular_cut

def particion_simple(grafo, k=2):
    """
    Genera una partición simple dividiendo los nodos secuencialmente en k grupos.
    Garantiza cobertura completa y balance básico.
    """
    nodos = grafo.nodos()
    n = len(nodos)
    tamano_base = n // k
    residuo = n % k
    
    particiones = []
    inicio = 0
    for i in range(k):
        # Distribuir el residuo entre los primeros 'residuo' grupos
        fin = inicio + tamano_base + (1 if i < residuo else 0)
        particiones.append(nodos[inicio:fin])
        inicio = fin
        
    return particiones

def fuerza_bruta_partition(grafo, k=2):
    """
    Encuentra la partición óptima exacta evaluando combinaciones posibles.
    Complejidad: O(n! / ((n/2)! * (n/2)!)) para k=2 balanceado.
    Limitado a datasets pequeños (N < 20 aprox).
    """
    if k != 2:
        raise NotImplementedError("Fuerza bruta optimizada solo para k=2 grupos balanceados en esta versión.")
        
    n = grafo.num_nodos
    nodos = grafo.nodos()
    mitad = n // 2
    
    mejor_costo = float('inf')
    mejor_particion = []
    
    for g1 in itertools.combinations(nodos, mitad):
        g1_list = list(g1)
        g2_list = [v for v in nodos if v not in g1_list]
        particiones = [g1_list, g2_list]
        
        costo = calcular_cut(grafo, particiones)
        if costo < mejor_costo:
            mejor_costo = costo
            mejor_particion = particiones
            
    return mejor_particion

def greedy_partition(grafo, k=2):
    """
    Construye particiones incrementalmente minimizando el aumento local del cut.
    Complejidad: O(V * k * (V/k)) aprox O(V^2), mucho más eficiente que la fuerza bruta.
    """
    nodos = grafo.nodos()
    particiones = [[] for _ in range(k)]
    
    # Asignación inicial simple para evitar grupos vacíos
    for i in range(min(k, len(nodos))):
        particiones[i].append(nodos[i])
        
    # Asignación greedy del resto de nodos
    for nodo in nodos[k:]:
        mejor_grupo = 0
        menor_aumento = float('inf')
        
        for i in range(k):
            aumento_costo = 0
            # El costo aumenta por las aristas hacia nodos en otros grupos
            for j in range(k):
                if i != j:
                    for v in particiones[j]:
                        aumento_costo += grafo.obtener_peso(nodo, v)
                        
            # Si hay empate, elegimos el grupo más pequeño para balancear
            if aumento_costo < menor_aumento or (aumento_costo == menor_aumento and len(particiones[i]) < len(particiones[mejor_grupo])):
                menor_aumento = aumento_costo
                mejor_grupo = i
                
        particiones[mejor_grupo].append(nodo)
        
    return particiones

def local_search_partition(grafo, particion_inicial):
    """
    Mejora una partición inicial mediante búsqueda local.
    Itera buscando pares de nodos de distintos grupos cuyo intercambio 
    disminuya el costo total del corte.
    Complejidad: O(I * (V/k)^2 * O(cut)) donde I es el número de iteraciones.
    """
    mejor_particion = [list(p) for p in particion_inicial]
    mejor_costo = calcular_cut(grafo, mejor_particion)
    k = len(mejor_particion)
    
    mejorando = True
    while mejorando:
        mejorando = False
        
        # Intentar intercambiar un nodo del grupo i con un nodo del grupo j
        for i in range(k):
            for j in range(i + 1, k):
                # Iterar sobre todos los pares de nodos posibles entre i y j
                for u in mejor_particion[i]:
                    for v in mejor_particion[j]:
                        
                        # Simular el intercambio
                        nueva_particion = [list(p) for p in mejor_particion]
                        nueva_particion[i].remove(u)
                        nueva_particion[i].append(v)
                        nueva_particion[j].remove(v)
                        nueva_particion[j].append(u)
                        
                        # Validar si hay grupos vacíos tras un intercambio no balanceado (no aplicable a swap 1x1, pero por si acaso)
                        if len(nueva_particion[i]) == 0 or len(nueva_particion[j]) == 0:
                            continue
                            
                        nuevo_costo = calcular_cut(grafo, nueva_particion)
                        
                        if nuevo_costo < mejor_costo:
                            mejor_costo = nuevo_costo
                            mejor_particion = nueva_particion
                            mejorando = True
                            break # Romper iteración interna para reiniciar la búsqueda
                    if mejorando:
                        break
                if mejorando:
                    break
                    
    return mejor_particion