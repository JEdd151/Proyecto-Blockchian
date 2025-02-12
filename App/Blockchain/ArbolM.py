import hashlib, math

class ArbolMerkle:
    def __init__(self, datos):
        self.datos = datos
        self.nodos = []
        self.raiz = None
        self.generar_arbol()

    def hash (self, dato):
        #se crea un hash del dato
        return hashlib.sha256(dato.encode('utf-8')).hexdigest()

    def generar_arbol(self):
        #crear los hashes de las hojas
        nivel_actual = [self.hash(d) for d in self.datos]
        self.nodos.append(nivel_actual)
        
        #generar los niveles superiores hasta la raiz
        while len(nivel_actual) > 1:
            
            siguiente_nivel = []
            
            for i in range (0, len(nivel_actual), 2):
                #convinar hashes vecinos
                izquierda = nivel_actual[i]
                derecha = nivel_actual[i + 1] if i + 1 < len (nivel_actual) else izquierda
                combinado = izquierda + derecha
                siguiente_nivel.append(self.hash(combinado))
                
            nivel_actual = siguiente_nivel
            self.nodos.append(nivel_actual)
            
        #la raiz esta en ultimo nivel
        self.raiz = self.nodos[-1][0]

    def obtener_raiz (self):
        return self.raiz
    
    def mostrar_arbol (self):
        for nivel in self.nodos:
            print(nivel)
            
    
    def verificar(self, dato):
        #verificar si un datos pertenece al arbol de merkle
        hash_dato = self.hash(dato)
        for nivel in self.nodos:
            if hash_dato in nivel:
                return True
        return False