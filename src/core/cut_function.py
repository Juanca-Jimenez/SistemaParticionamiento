def calcular_cut(grafo, particiones):
    """
    Calcula el costo de comunicación (corte) entre k grupos distintos.
    
    Complejidad: O(V^2) en el peor caso (grafo denso), iterando sobre
    las conexiones inter-grupo. Solo se comparan pares de grupos
    distintos (i < j) para evitar doble conteo.
    """
    costo_total = 0
    num_grupos = len(particiones)

    for i in range(num_grupos):
        for j in range(i + 1, num_grupos):
            for u in particiones[i]:
                for v in particiones[j]:
                    costo_total += grafo.obtener_peso(u, v)

    return costo_total
