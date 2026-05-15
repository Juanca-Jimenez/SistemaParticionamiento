class Grafo:
    def __init__(self, matriz):
        self.num_nodos = len(matriz)
        self.matriz = matriz

    def obtener_peso(self, u, v):
        return self.matriz[u][v]

    def nodos(self):
        return list(range(self.num_nodos))
