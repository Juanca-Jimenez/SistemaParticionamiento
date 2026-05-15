def es_cuadrada(matriz):
    filas = len(matriz)

    for fila in matriz:
        if len(fila) != filas:
            return False

    return True