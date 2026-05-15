def calcular_cut(matriz, grupo1, grupo2):
    costo = 0

    for i in grupo1:
        for j in grupo2:
            costo += matriz[i][j]

    return costo

    
