import math

def calcular_estadisticas(tiempos, costos):
    """
    Calcula métricas estadísticas básicas para ejecuciones de algoritmos.
    """
    if not tiempos or not costos:
        return {}

    n = len(tiempos)
    
    tiempo_promedio = sum(tiempos) / n
    varianza_tiempo = sum((t - tiempo_promedio) ** 2 for t in tiempos) / n
    desviacion_tiempo = math.sqrt(varianza_tiempo)
    
    mejor_costo = min(costos)
    peor_costo = max(costos)
    costo_promedio = sum(costos) / len(costos)
    varianza_costo = sum((c - costo_promedio) ** 2 for c in costos) / len(costos)
    desviacion_costo = math.sqrt(varianza_costo)

    return {
        "tiempo_promedio_s": round(tiempo_promedio, 6),
        "tiempo_desviacion_s": round(desviacion_tiempo, 6),
        "mejor_costo": mejor_costo,
        "peor_costo": peor_costo,
        "costo_promedio": round(costo_promedio, 2),
        "costo_desviacion": round(desviacion_costo, 2)
    }
