import numpy as np

#Tolerancias de los decimales
_RTOL = 1e-5
_ATOL = 1e-8

def validar_matriz(matriz: np.ndarray) -> tuple[bool, str]:
    verificaciones = [
        es_cuadrada,
        tiene_valores_no_negativos,
        es_simetrica,
    ]
    for verificar in verificaciones:
        ok, mensaje = verificar(matriz)
        if not ok:
            return False, mensaje

    return True, "Matriz válida."

def es_cuadrada(matriz: np.ndarray) -> tuple[bool, str]:
    if matriz.ndim != 2:
        return False, (
            f"Se esperaba una matriz 2D, pero se recibió un array de "
            f"{matriz.ndim} dimensiones."
        )

    filas, cols = matriz.shape

    if filas == 0 or cols == 0:
        return False, "La matriz está vacía (0 elementos)."

    if filas == 1:
        return False, (
            "La matriz debe representar al menos 2 nodos para "
            "que tenga sentido particionarla."
        )

    if filas != cols:
        return False, (
            f"Matriz no cuadrada: {filas} filas × {cols} columnas. "
            f"Se requiere una matriz n×n."
        )

    n = filas
    return True, f"Es cuadrada ({n}×{n})."

def tiene_valores_no_negativos(matriz: np.ndarray) -> tuple[bool, str]:
    mascara_negativos = matriz < 0

    if not mascara_negativos.any():
        return True, "Todos los valores son no negativos."

    cantidad = int(mascara_negativos.sum())
    posiciones = np.argwhere(mascara_negativos)
    i0, j0 = posiciones[0]
    valor0 = matriz[i0, j0]

    return False, (
        f"Se encontraron {cantidad} valor(es) negativo(s). "
        f"Primer caso: D[{i0},{j0}] = {valor0:.4g}. "
        "Las dependencias deben ser valores ≥ 0."
    )

def es_simetrica(matriz: np.ndarray) -> tuple[bool, str]:
    traspuesta = matriz.T

    #Verifica si es simétrica teniendo en cuenta los errores de precision de los decimales
    if np.allclose(matriz, traspuesta, rtol=_RTOL, atol=_ATOL):
        return True, "Es simétrica."

    n = matriz.shape[0]
    pares_asimetricos = []
    for i in range(n):
        for j in range(i + 1, n):
            if not np.isclose(matriz[i, j], matriz[j, i], rtol=_RTOL, atol=_ATOL):
                pares_asimetricos.append((i, j, matriz[i, j], matriz[j, i]))

    cantidad = len(pares_asimetricos)
    i0, j0, a, b = pares_asimetricos[0]
    diferencia = abs(a - b)

    return False, (
        f"Matriz no simétrica: se encontraron {cantidad} par(es) asimétrico(s). "
        f"Ejemplo: D[{i0},{j0}] = {a:.4g} pero D[{j0},{i0}] = {b:.4g} "
        f"(diferencia: {diferencia:.4g})."
    )

def informe_validacion(matriz: np.ndarray) -> dict[str, tuple[bool, str]]:
    return {
        "cuadratica":  es_cuadrada(matriz),
        "no_negativa": tiene_valores_no_negativos(matriz),
        "simetrica":   es_simetrica(matriz),
    }

# ESTE MÓDULO SE ENCARGA DE LA VALIDACIÓN ESTRUCTURAL DE MATRICES DE DEPENDENCIAS.
# Verifica que una matriz NumPy cumpla con las propiedades de ser cuadrática (n, n),
# no negativa (D[i,j] >= 0), y simétrica (D[i,j] ≈ D[j,i] con tolerancia). No realiza
# operaciones de entrada/salida ni impresión.