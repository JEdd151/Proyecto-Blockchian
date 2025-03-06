#*
# La prueba de concenso puede ser una cadena de bits o un numero 
# que al conbinarlo con el contenido del bloque, cumpla con ciertas condiciones
# 
# Implementacion de un PoW como el de bitcoin
# 
# - calcular el proof de trabajo
# - verificar si el proof es correcto
#
# *

import hashlib

class Prueba_Concenso:
    
    #La dificultad define cuantos ceros debe deter el hash valido
    def __init__(self, dificultad = 2):
        self.dificultad = dificultad


    #Generar un proof en base a los datos de entrada, incrementando un numero hasta que 
    #el hash cumpla con la dificultad
    def generar_proof(self, datos):
        """
        Genera un proof válido para los datos dados.

        :param datos: Datos del bloque.
        :return: Proof válido.
        """
        if not datos:
            raise ValueError("Los datos no pueden estar vacíos.")

        proof = 0
        max_intentos = 1000000  #Límite de intentos para evitar bucles infinitos
        intentos = 0

        while intentos < max_intentos:
            prueba = f"{datos}{proof}".encode('utf-8')
            hash_resultado = hashlib.sha256(prueba).hexdigest()

            if hash_resultado[:self.dificultad] == '0' * self.dificultad:
                return proof

            proof += 1
            intentos += 1

        raise Exception("No se pudo generar un proof válido después de múltiples intentos.")


    def validar_proof (self, datos, proof):
        prueba = f"{datos}{proof}".encode('utf-8')
        hash_resultado = hashlib.sha256(prueba).hexdigest()
        return hash_resultado[:self.dificultad] == '0' * self.dificultad