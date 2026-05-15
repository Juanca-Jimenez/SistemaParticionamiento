def es_cuadrada(matriz):
    filas = len(matriz)
    for fila in matriz:
        if len(fila) != filas:
            return False, "La matriz no es cuadrada (filas inconsistentes)."
    return True, ""

def es_simetrica(matriz):
    n = len(matriz)
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != matriz[j][i]:
                return False, f"La matriz no es simétrica en la posición ({i}, {j})."
    return True, ""

def validar_matriz(matriz):
    if not matriz or len(matriz) == 0 or len(matriz[0]) == 0:
        return False, "La matriz está vacía."

    cuadrada, msg_cuadrada = es_cuadrada(matriz)
    if not cuadrada:
        return False, msg_cuadrada

    simetrica, msg_simetrica = es_simetrica(matriz)
    if not simetrica:
        return False, msg_simetrica

    # La validación de tipos numéricos ya se cubre en gran parte en el lector,
    # pero aseguramos consistencia de tipos.
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if not isinstance(valor, (int, float)):
                return False, f"Valor inválido no numérico en ({i}, {j})."

    return True, "Matriz válida."