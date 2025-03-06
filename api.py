from fastapi import FastAPI, HTTPException, Depends
from App.BD.GestorBD import GestorBD
from App.Blockchain.Modulo_Blockchain import Blockchain
from pydantic import BaseModel
import uvicorn

##instancia de fastAPI
app = FastAPI()

# Función para obtener una instancia de GestorBD
def obtener_gestor_bd():
    gestor = GestorBD()
    return gestor

# Función para obtener una instancia de Blockchain
def obtener_blockchain(gestor_bd: GestorBD = Depends(obtener_gestor_bd)):
    return Blockchain(gestor_bd)


#print("\n\nConectando con la base de datos...")
##iniciar la conexion a la bbdd
#gestorBD = GestorBD()
#print("Base de datos conectada correctamente.\n\n")


#blockchain = Blockchain(gestorBD)

##modelo de datos para agregar un bloque
class BloqueEntrada (BaseModel):
    datos_cifrados: str

@app.get('/')
def home():
    return {"mensaje": "API funcionando", "status": 200}


@app.get("/bloques")
def obtener_cadena(blockchain: Blockchain = Depends(obtener_blockchain)):
    """
    Retorna la cadena de bloques almacenada en la base de datos.
    """
    try:
        print("Cadena de bloques", blockchain.cadena)
        return {
            "status": 200,
            "mensaje": "Cadena de bloques obtenida correctamente",
            "data": [
                {
                    "index": bloque.index,
                    "datos": bloque.datos,
                    "hash_anterior": bloque.hash_actual,
                    "proof": bloque.proof,
                }
                for bloque in blockchain.cadena
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la cadena de bloques: {str(e)}")


@app.post("/bloques")
def agregar_bloques(datos: BloqueEntrada, blockchain: Blockchain = Depends(obtener_blockchain)):
    try:
        print("Recibido:", datos)  #Agregar esto para ver qué llega
        blockchain.agregar_bloques(datos.datos_cifrados)  #No usesar .encode() aquí
        return {'mensaje': 'Bloque agregado correctamente'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/validar")
def validar_blockchain(blockchain: Blockchain = Depends(obtener_blockchain)):
    try:
        es_valida = blockchain.es_valida()
        return {
            "status": 200,
            "mensaje": "Validación completada",
            "valida": es_valida
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al validar la blockchain: {str(e)}")
    

if __name__ == '__main__':
    ##app.run(debug=True)
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)