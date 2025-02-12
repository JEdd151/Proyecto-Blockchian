#*En esta clase se crearan las tarjetas:
# - numero
# - fecha de vencimiento
# - cvv
# 
# Funciones para mostrar los datos por tarjeta, guardar la informacion en
# un formato Json con la clave privada exportada de la clase Claves.py (esta
# informacion es para el usuario)
# *#

import random
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
import json

class Tarjeta:
    def __init__(self, id, numero, fecha_vencimiento, cvv):
        self.id = id
        self.numero = numero
        self.fecha_vencimiento = fecha_vencimiento
        self.cvv = cvv
        
    @classmethod
    def generar_tarjeta(cls):
        tarjeta_id = cls.generar_id()
        numero = cls.generar_numero_tarjeta()
        fecha_vencimiento = cls.generar_fecha_vencimiento()
        cvv = cls.generar_cvv()
        return cls(tarjeta_id, numero, fecha_vencimiento, cvv)
    
    @staticmethod
    def generar_numero_tarjeta():
        numero_por_defecto = "4000000"
        numero_cuanta = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        return numero_por_defecto + numero_cuanta
    
    @staticmethod
    def generar_fecha_vencimiento():
        hoy = datetime.now()
        fecha_vencimiento = hoy + timedelta(days=5 * 365)
        return fecha_vencimiento.strftime("%m/%y")
    
    @staticmethod
    def generar_cvv():
        return str(random.randint(100, 999))
    
    @staticmethod
    def generar_id():
        return str(random.randint(100000, 999999))
    
    def obtener_datos(self):
        return {
            "id": self.id,
            "numero_tarjeta": self.numero,
            "cvv": self.cvv,
            "fecha_expiracion": self.fecha_vencimiento
        }
    
    def mostra_informacion(self):
        print(f"\nID: {self.id}")
        print(f"Numero: {self.numero}")
        print(f"Fecha de vencimiento: {self.fecha_vencimiento}")
        print(f"CVV: {self.cvv}\n")
    
    def guardar_datos(self, ruta_archivo, clave_privada):
        clave_privada_serializada = clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        #Aquí vamos a guardar los datos sin cifrar de la tarjeta
        datos_tarjeta = {
            'id': self.id,
            'numero_tarjeta': self.numero,
            'cvv': self.cvv,
            'fecha_expiracion': self.fecha_vencimiento,
            'clave_privada': clave_privada_serializada
        }

        #Guardamos los datos sin cifrar en el archivo JSON
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
            json.dump(datos_tarjeta, archivo_json, ensure_ascii=False, indent=4)

        print(f"Datos sin cifrar de la tarjeta guardados en {ruta_archivo}")
    