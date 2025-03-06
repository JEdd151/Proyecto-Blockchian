#*Esta clase es la representacion de un bloque, contiene los 
# elementos de un bloque:
# - Indice
# - Datos
# - Hash previo
# - Hash actual
# 
# Se calcula el actual mediante la informacion del bloque actual
# *#
#from App.Blockchain.ArbolM import ArbolMerkle
import hashlib
import json

class Bloque:
    def __init__(self, index, datos, hash_anterior, proof = 0):
        if not isinstance(datos, dict):
            raise ValueError("Los datos deben ser un diccionario.")
        
        self.index = index
        self.datos = datos
        self.hash_anterior = hash_anterior
        self.proof = proof
        self.hash_actual = self.calcular_hash()
        #self.raiz_merkle = self.generar_raiz_merkle()

    #Este metodo genera un hash unico para cada bloque usando haslib con el Sha-256
    def calcular_hash(self):
        #combertir los datos en uan cadena json ordenada, esto para asegurar que el hash sea siempre el mismo
        # + concatenamos el hash anterior para garantizar la relación entre bloques
        # + el indice del bloque tambien forma parte del calculo
        bloque_string = json.dumps(self.datos, sort_keys=True) + self.hash_anterior + str(self.index)
        #se combierte la cadena en un formato de bytes que hashlib puede procesar
        #genera un hash con hashlib y devuelve el hash como una cadena hexadecimal
        return hashlib.sha256(bloque_string.encode('utf-8')).hexdigest()
    
    def actualizar_proof (self, proof):
        self.proof = proof
        self.hash_actual = self.calcular_hash()
    #def generar_raiz_merkle(self):
    #   #crear el arbol de merkle con los datos y devuelve la raiz
    #    arbol = ArbolMerkle([json.dumps(tx) for tx in self.datos])
    #    return arbol.obtener_raiz()
    
    #def obtener_raiz_merkle(self):
    #    return self.raiz_merkle
    
    def minar_bloque (self, dificultad = 2):
        """
        
        Minar el bloque encontrando un proof válido.

        :param dificultad: Número de ceros iniciales requeridos en el hash.
        
        """
        self.proof = 0
        while not self.hash_actual.startswith("0" * dificultad):
            self.proof += 1
            self.hash_actual = self.calcular_hash()

    def __str__(self):
        """
        Representación en cadena del bloque.

        :return: Cadena que representa el bloque.
        """
        return (f"Bloque {self.index}\n"
                f"Datos: {self.datos}\n"
                f"Hash Anterior: {self.hash_anterior}\n"
                f"Hash Actual: {self.hash_actual}\n"
                f"Proof: {self.proof}\n"
                "-" * 30)