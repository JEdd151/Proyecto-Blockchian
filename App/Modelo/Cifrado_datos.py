
#*
# Cifrado de los datos de la tarjeta, se realiara con ayuda de la clave publica generada
# para cada tarjeta, se hara de la siguiente manera:
# *#

import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class Cifrado_datos:
    @staticmethod
    def cifrar_datos(datos, clave_publica):
        
        #Cifra los datos usando una clave pública.
        #Los datos deben ser un diccionario, que se convierte en una cadena JSON antes de cifrar.
        #Convertir los datos del diccionario a una cadena JSON, esto permite que los datos sean serializados
        #y compatibles con el cifrado 
        datos_json = json.dumps(datos) 
        
        #Convertir la cadena JSON a bytes, los algoritmos de cifrado trabajan a niveles de bytes
        datos_bytes = datos_json.encode("utf-8")

        #Cifrar los datos con la clave pública
        #*
        # Se usa el algoritmo RSA el cual utiliza una clave pública proporcionada para cifrar los datos.
        # 
        # El Padding OAEP es un esquema el cual agrega seguridad al cifrado RSA al incluir:
        # - MGF1; un funcion generadora de máscaras basadas en SHA-256
        # - SHA-256; algorimo de hash utilizado para generar el padding y el hash principal
        # - Label; en este caso se deja en NONE ya que no se utiliza un valor adicional para asiciar con los datos cifrados.
        # 
        # *#
        datos_cifrados = clave_publica.encrypt(
            datos_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return datos_cifrados
