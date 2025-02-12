#*En esta clase se crea la cadena de bloques, con la clase Bloque creamos 
# un "nodo", se crea el bloque genesis con un indice inicial en 0, datis
# y un hash previo como str
# 
# Inicialmente se agrega el bloque a una lista para contenerlo.*#
from App.Blockchain.Bloque import Bloque
from App.BD.GestorBD import GestorBD
import json
import base64

class Blockchain:
    def __init__(self, gestorBD):
        #recibe la instancia de la bd
        self.gestorBD = gestorBD
        #self.clave_publica = clave_publica #clave proporcionada desde el main
        #Inicializamos la blockchain con un bloque genesis
        self.cadena = []
        self.cargar_cadenaBD()

    def cargar_cadenaBD(self):
        #aqui se cargan los bloques de la bd
        bloques = self.gestorBD.cargar_bloques()
        for bloque in bloques:
            #index, datos, hash_anterior, hash_actual = bloque
            #datos = json.loads(datos)
            #nuevo_bloque = Bloque(index, datos, hash_anterior)
            #nuevo_bloque.hash_actual = hash_actual
            nuevo_bloque = Bloque(bloque.index, bloque.datos, bloque.hash_anterior)
            nuevo_bloque.hash_actual = bloque.hash_actual
            self.cadena.append(nuevo_bloque)
        
        #si no hay bloques, crear bloque génesis
        if not self.cadena:
            self.crea_bloque_genesis()
            
            
    def crea_bloque_genesis(self):
        #como es el primer bloque tiene datos basicos y no tiene hash anterior
        bloque_genesis = Bloque(0, {"mensaje": "Bloque Genesis"}, "")
        self.cadena.append(bloque_genesis)
        self.gestorBD.guardar_bloque(bloque_genesis)


    def agregar_bloques (self, datos):
        #convertimos los datos cifrados a base 64
        datos_cifrados_base64 = base64.b64encode(datos['datos_cifrados']).decode('utf-8')
        datos['datos_cifrados'] = datos_cifrados_base64
        
        #agregar nuevos bloques a la cadena
        ultimo_bloque = self.obtener_ultimo_bloque()
        #nuevo_bloque = Bloque(len(self.cadena), datos, ultimo_bloque.hash_actual)
        nuevo_bloque = Bloque(ultimo_bloque.index + 1, datos, ultimo_bloque.hash_actual)
        self.cadena.append(nuevo_bloque)
        self.gestorBD.guardar_bloque(nuevo_bloque)


    def obtener_ultimo_bloque(self):
        return self.cadena[-1]


    def es_valida(self):
        #se verifica la integridad de la cadena
        for i in range (1, len(self.cadena)):
            bloque_actual = self.cadena[i]
            bloque_anterior = self.cadena[i - 1]
            
            if bloque_actual.hash_anterior != bloque_anterior.hash_actual:
                print(f"Error: el hash anterior del bloque {i} no coincide")
                return False
            
            if bloque_actual.hash_actual != bloque_actual.calcular_hash():
                print(f"Error: el hash actual del bloqui {i} es inválido")
                return False
        
        return True

    def mostrar_cadena(self):
        for bloque in self.cadena:
            print(f"Índice: {bloque.index}")
            print(f"Datos: {bloque.datos}")
            print(f"Hash Anterior: {bloque.hash_anterior}")
            print(f"Hash Actual: {bloque.hash_actual}")
            #print(f"Raíz de Merkle: {bloque.raiz_merkle}")
            print("-" * 30)