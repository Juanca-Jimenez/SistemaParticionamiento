import csv

"""
Lee un archivo CSV, filtra filas vacías, descarta encabezados si los hay,
y convierte los datos a una matriz de flotantes.
"""
def leer_matriz(ruta: str) -> list[list[float]]:
    # Leer filas del CSV
    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            lector = csv.reader(f)
            filas = list(lector)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se encontró el archivo '{ruta}'. "
            "Verifique la ruta e intente de nuevo."
        )
    except UnicodeDecodeError:
        # Segundo intento con latin-1 (archivos exportados desde Excel en español)
        with open(ruta, newline="", encoding="latin-1") as f:
            lector = csv.reader(f)
            filas = list(lector)

    # Filtrar filas completamente vacías
    filas_filtradas = []
    for fila in filas:
        tiene_datos = False
        for celda in fila:
            if celda.strip():
                tiene_datos = True
                break
        if tiene_datos:
            filas_filtradas.append(fila)
    filas = filas_filtradas
    
    if not filas:
        return []

    # Descartar encabezados si hay
    try:
        float(filas[0][0].strip())
    except (ValueError, IndexError):
        # Si la primera celda no es numérica, hay encabezados
        filas = filas[1:]
        filas_sin_encabezados = []
        for fila in filas:
            filas_sin_encabezados.append(fila[1:])
        filas = filas_sin_encabezados

    # Convertir a matriz de flotantes
    resultado = []
    for i, fila in enumerate(filas):
        fila_float = []
        for j, celda in enumerate(fila):
            celda = celda.strip()
            if celda == "":
                raise ValueError(
                    f"Celda vacía en fila {i + 1}, columna {j + 1} "
                    f"del archivo '{ruta}'."
                )
            try:
                fila_float.append(float(celda))
            except ValueError:
                raise ValueError(
                    f"Valor no numérico '{celda}' en fila {i + 1}, "
                    f"columna {j + 1} del archivo '{ruta}'. "
                    "Todos los valores deben ser números."
                )
        resultado.append(fila_float)
        
    return resultado

