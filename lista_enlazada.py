class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insertar_al_frente(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamano += 1

    def insertar_al_final(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cola is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self.tamano += 1

    def obtener_primero(self):
        if self.cabeza:
            return self.cabeza.vuelo
        return None

    def obtener_ultimo(self):
        if self.cola:
            return self.cola.vuelo
        return None

    def longitud(self):
        return self.tamano

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion < 0 or posicion > self.tamano:
            raise IndexError("Índice fuera de rango")
        nuevo_nodo = Nodo(vuelo)
        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.tamano:
            self.insertar_al_final(vuelo)
        else:
            nodo_actual = self.cabeza
            for _ in range(posicion):
                nodo_actual = nodo_actual.siguiente
            nuevo_nodo.anterior = nodo_actual.anterior
            nuevo_nodo.siguiente = nodo_actual
            nodo_actual.anterior.siguiente = nuevo_nodo
            nodo_actual.anterior = nuevo_nodo
            self.tamano += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Índice fuera de rango")
        nodo_actual = self.cabeza
        for _ in range(posicion):
            nodo_actual = nodo_actual.siguiente
        if nodo_actual.anterior:
            nodo_actual.anterior.siguiente = nodo_actual.siguiente
        if nodo_actual.siguiente:
            nodo_actual.siguiente.anterior = nodo_actual.anterior
        if nodo_actual == self.cabeza:
            self.cabeza = nodo_actual.siguiente
        if nodo_actual == self.cola:
            self.cola = nodo_actual.anterior
        self.tamano -= 1
        return nodo_actual.vuelo
