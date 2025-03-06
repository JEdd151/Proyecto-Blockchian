#la funcion para generar la prueba de trabajo se desarrolla fuera de la clase ya 
#que realiza un calculo independiente basado en los datos de un bloque por lo que 
# puede colocarse como una función auxiliar.
"""import hashlib
def generar_proof(dato, dificultad = 4):
    #Generar un proof, la dificultad determinara cuantos 0 debe estar al inicio del hash
    proof = 0
    while True:
        #concatenamos los datos del bloque con el proof
        prueba = f"{dato}{proof}".encode('utf-8')
        hash_resultado = hashlib.sha256(prueba).hexdigest()
        
        #verificamos si el hash cumple con la dificultad
        if hash_resultado[:dificultad] == '0' * dificultad:
            return proof
        proof += 1
"""    
#*En esta clase se crea la cadena de bloques, con la clase Bloque creamos 
# un "nodo", se crea el bloque genesis con un indice inicial en 0, datis
# y un hash previo como str
# 
# Inicialmente se agrega el bloque a una lista para contenerlo.*#
from App.Blockchain.Bloque import Bloque
from App.BD.GestorBD import GestorBD
from App.Blockchain.Prueba_Concenso import Prueba_Concenso
import json
import base64

class Blockchain:
    def __init__(self, gestorBD):
        #recibe la instancia de la bd
        self.gestorBD = gestorBD
        #self.clave_publica = clave_publica #clave proporcionada desde el main
        #Inicializamos la blockchain con un bloque genesis
        self.cadena = []
        self.pow = Prueba_Concenso(dificultad = 4)
        self.cargar_cadenaBD()

    def cargar_cadenaBD(self):
        """
        Carga la cadena de bloques desde la base de datos.
        """
        try:
            bloques = self.gestorBD.cargar_bloques()
            for bloque in bloques:
                nuevo_bloque = Bloque(bloque.index, bloque.datos, bloque.hash_anterior, bloque.proof)
                nuevo_bloque.hash_actual = bloque.hash_actual
                self.cadena.append(nuevo_bloque)

            if not self.cadena:
                self.crea_bloque_genesis()
        except Exception as e:
            raise Exception(f"Error al cargar la cadena desde la base de datos: {e}")
            
            
    def crea_bloque_genesis(self):
        #como es el primer bloque tiene datos basicos y no tiene hash anterior
        bloque_genesis = Bloque(0, {"mensaje": "Bloque Genesis"}, "")
        #calculamos el proof
        bloque_genesis.proof = self.pow.generar_proof("Bloque Genesis")
        self.cadena.append(bloque_genesis)
        self.gestorBD.guardar_bloque(bloque_genesis)


    def agregar_bloques(self, datos_cifrados):
        """
        Agrega un nuevo bloque a la cadena.

        :param datos_cifrados: Datos cifrados del bloque.
        """
        try:
            # Convertir los datos cifrados a base64
            datos_cifrados_base64 = base64.b64encode(datos_cifrados.encode()).decode('utf-8')
            datos = {"datos_cifrados": datos_cifrados_base64}

            # Obtener el último bloque
            ultimo_bloque = self.obtener_ultimo_bloque()

            # Generar el proof para el nuevo bloque
            proof = self.pow.generar_proof(datos)

            # Crear el nuevo bloque
            nuevo_bloque = Bloque(ultimo_bloque.index + 1, datos, ultimo_bloque.hash_actual, proof)
            self.cadena.append(nuevo_bloque)

            # Guardar el bloque en la base de datos
            self.gestorBD.guardar_bloque(nuevo_bloque)
        except Exception as e:
            raise Exception(f"Error al agregar un bloque: {e}")


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

            #validamos la prueba
            if not self.pow.validar_proof(bloque_actual.datos, bloque_actual.proof):
                print(f"Error: el proof del bloque {i} no es valido")
                return False
        
        return True

    def mostrar_cadena(self):
        for bloque in self.cadena:
            print(bloque)