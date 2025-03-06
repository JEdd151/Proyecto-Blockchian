from App.Modelo.Tarjetas import Tarjeta
from App.Modelo.Cifrado_datos import Cifrado_datos
from App.Modelo.Claves import Claves
from App.BD.GestorBD import GestorBD
from App.Blockchain.Modulo_Blockchain import Blockchain
import os
import base64
import json

def mostrar_cadena_formateada(blockchain):
    """
    Muestra la cadena de bloques en un formato legible.
    """
    for bloque in blockchain.cadena:
        print(f"Bloque {bloque.index}:")
        print(f"  Datos: {bloque.datos}")
        print(f"  Hash Anterior: {bloque.hash_anterior}")
        print(f"  Hash Actual: {bloque.hash_actual}")
        print(f"  Proof: {bloque.proof}")
        print("-" * 30)

def main():
    """
    Función principal que genera una tarjeta, cifra sus datos,
    los guarda en archivos JSON y los agrega a la blockchain.
    """
    try:
        # Rutas relativas
        RUTA_DATOS_SIN_CIFRAR = os.path.join("Informacion", "datos_sin_cifrar.json")
        RUTA_DATOS_CIFRADOS = os.path.join("Informacion", "datos_cifrados.json")

        # Inicializar la blockchain y el gestor de la base de datos
        gestorBD = GestorBD()
        blockchain = Blockchain(gestorBD)

        # Generar claves
        claves = Claves()

        # Generar una tarjeta
        tarjeta = Tarjeta.generar_tarjeta()
        tarjeta.mostra_informacion()

        # Guardar los datos sin cifrar en un archivo JSON
        tarjeta.guardar_datos(RUTA_DATOS_SIN_CIFRAR, claves.clave_privada)

        # Cifrar los datos con la clave pública
        tarjeta_datos = tarjeta.obtener_datos()
        datos_cifrado = Cifrado_datos.cifrar_datos(tarjeta_datos, claves.clave_publica)
        print("\nDatos Cifrados:\n", datos_cifrado)

        # Guardar datos cifrados (con clave pública)
        claves.guardar_claves_json(tarjeta.id, RUTA_DATOS_CIFRADOS, datos_cifrado)
        print("\n======================")
        print(f"Datos guardados correctamente en ({RUTA_DATOS_CIFRADOS}) y ({RUTA_DATOS_SIN_CIFRAR})\n")

        # Agregar un bloque a la blockchain con los datos cifrados
        # Agregar un bloque a la blockchain con los datos cifrados
        datos_bloque = {
            "tarjeta_id": tarjeta.id,
            "datos_cifrados": datos_cifrado  # No codificar en base64 aquí
        }
        blockchain.agregar_bloques(datos_cifrado)  # Pasar los datos cifrados directamente
        print("\nBloque agregado a la Blockchain\n")

        # Mostrar la cadena actual
        print("Estado actual de la blockchain:")
        mostrar_cadena_formateada(blockchain)

    except Exception as e:
        print(f"Error en la ejecución: {e}")

if __name__ == "__main__":
    main()