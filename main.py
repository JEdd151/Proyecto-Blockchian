from App.Modelo.Tarjetas import Tarjeta
from App.Modelo.Cifrado_datos import Cifrado_datos
from App.Modelo.Claves import Claves
from App.BD.GestorBD import GestorBD
from App.Blockchain.Modulo_Blockchain import Blockchain
import base64

def main():
    #inicializamos la blockchain
    gestorBD = GestorBD()
    #Generar claves
    claves = Claves()
    
    #blockchain = Blockchain(gestorBD, claves.clave_publica)
    blockchain = Blockchain(gestorBD)
    #Generar un tarjeta
    tarjeta = Tarjeta.generar_tarjeta()
    tarjeta.mostra_informacion()
    
    #Guardar los datos sin cifrar en datos_tarjeta.json
    ruta_datos_sin_cifrar = "C:\\Users\\lopez\\OneDrive\\PT\\Informacion\\datos_sin_cifrar.json"
    tarjeta.guardar_datos(ruta_datos_sin_cifrar, claves.clave_privada)
    #Cifrar los datos con la clave publica
    tarjeta_datos = tarjeta.obtener_datos()
    datos_cifrado = Cifrado_datos.cifrar_datos(tarjeta_datos, claves.clave_publica)
    print ("\nDatos Cifrados:\n", datos_cifrado)
    
    
    
    
    
    #Guardar datos cifrados (con clave pública)
    ruta_datos_cifrados = "C:\\Users\\lopez\\OneDrive\\PT\\Informacion\\datos_cifrados.json"
    claves.guardar_claves_json(tarjeta.id, ruta_datos_cifrados, datos_cifrado)
    print("\n======================")
    print(f"Datos guardados correctamente en ({ruta_datos_cifrados}) y ({ruta_datos_sin_cifrar})\n")

    #agregar un bloque a la blockchain con los datos cifrados
    blockchain.agregar_bloques({
            "tarjeta_id": tarjeta.id, 
            "datos_cifrados": datos_cifrado
        })
    print("\nBloque agregado a la Blockchain\n")
    
    #mostrar la cadena actual
    print("Estado actual de la blockchain:")
    blockchain.mostrar_cadena()
    
if __name__ == "__main__":
    main()