def particion_simple(n):
    mitad = n // 2

    grupo1 = list(range(mitad))
    grupo2 = list(range(mitad, n))

    return grupo1, grupo2