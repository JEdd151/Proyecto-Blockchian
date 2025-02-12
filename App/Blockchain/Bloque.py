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
    def __init__(self, index, datos, hash_anterior=''):
        self.index = index
        self.datos = datos
        self.hash_anterior = hash_anterior
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
    
    #def generar_raiz_merkle(self):
    #   #crear el arbol de merkle con los datos y devuelve la raiz
    #    arbol = ArbolMerkle([json.dumps(tx) for tx in self.datos])
    #    return arbol.obtener_raiz()
    
    #def obtener_raiz_merkle(self):
    #    return self.raiz_merkle
    