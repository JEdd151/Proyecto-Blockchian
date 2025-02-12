#*En esta clase se crean las claves privadas y publicas para cada
# tarjeta, al igual que se implementan funciones para el almacenamiento
# de esas claves
# *#

import json
from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Claves:
    def __init__(self, tamaño_clave = 2048):
        self.tamaño_clave = tamaño_clave
        self.clave_privada = None
        self.clave_publica = None
        self.generar_claves()

    def generar_claves(self):
        self.clave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.tamaño_clave,
            backend=default_backend()
        )
        self.clave_publica = self.clave_privada.public_key()
        
        
    def serializar_clave_publica(self):
        """Serializa la clave pública a formato PEM."""
        return self.clave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

    def serializar_clave_privada(self):
        """Serializa la clave privada a formato PEM."""
        return self.clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")



    def guardar_claves_json(self, id_tarjeta, ruta_archivo_json, datos_tarjeta, incluir_clave_privada=True, incluir_clave_publica=True):
        #Convertir los datos de la tarjeta a una cadena base64 para hacerlos serializables
        datos_tarjeta_base64 = b64encode(datos_tarjeta).decode("utf-8")

        #Construir el diccionario con los datos a guardar
        datos = {
            "id_tarjeta": id_tarjeta,
            "clave_publica": self.serializar_clave_publica(),
            "datos_tarjeta": datos_tarjeta_base64  # Datos de la tarjeta codificados en base64
        }
        
        #si se debe incluir la clave privada, agregarla al diccionario
        if incluir_clave_privada:
            datos["clave_privada"] = self.serializar_clave_privada()
        
        # Guardar el archivo JSON
        with open(ruta_archivo_json, "w", encoding="utf-8") as archivo_json:
            json.dump(datos, archivo_json, indent=4)

    def guardar_claves_separadas(self, ruta_privada="Clave_privada.pem", ruta_publica="clave_publica.pem"):
        with open(ruta_privada, "wb") as archivo_privado:
            archivo_privado.write(
                self.clave_privada.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        with open(ruta_publica, "wb") as archivo_publico:
            archivo_publico.write(
                self.clave_publica.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )