#En esta clase hace la conexion a la bd
from App.Blockchain.Bloque import Bloque
import sqlite3
import json

class GestorBD:
    def __init__(self, bd_path = "blockchian.db"):
        self.bd_path = bd_path
        self.conectar_bd()
        self.crear_tabla_si_no_existe()

    def conectar_bd(self):
        #establecer la conexión
        self.conn = sqlite3.connect(self.bd_path)
        self.cursor = self.conn.cursor()

    def crear_tabla_si_no_existe(self):
        #crear la tabla para los bloques si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bloques (
                indice INTEGER PRIMARY KEY,
                datos TEXT NOT NULL,
                hash_anterior TEXT,
                hash_actual TEXT
            )
        """)
        self.conn.commit()

    def guardar_bloque(self, bloque):
        self.cursor.execute("""
            INSERT INTO bloques (indice, datos, hash_anterior, hash_actual)
            VALUES (?, ?, ?, ?)
        """, (bloque.index, json.dumps(bloque.datos), bloque.hash_anterior, bloque.hash_actual)
        )
        self.conn.commit()


    def cargar_bloques(self):
        self.cursor.execute("SELECT * FROM bloques ORDER BY indice")
        bloques = self.cursor.fetchall()
        #cuando se cargen los bloqyes desde la base de datos, se debe recuperar la raiz
        #de merkle y asignarla a cada bloque
        bloques_recuperados = []
        for bloque in bloques:
            #recuperar los valores de cada bloque
            index, datos, hash_anterior, hash_actual = bloque
            #raiz_merkle = bloque
            datos = json.loads(datos)
            nuevo_bloque = Bloque(index, datos, hash_anterior)
            nuevo_bloque.hash_actual = hash_actual
            #nuevo_bloque.raiz_merkle = raiz_merkle  # Asignamos la raíz de Merkle
            bloques_recuperados.append(nuevo_bloque)
            
        return bloques_recuperados

    def borrar_todos_los_bloques(self):
        #Borrar todos los bloques de la tabla
        self.cursor.execute("DELETE FROM bloques")
        self.conn.commit()

    def borrar_tabla(self):
        #Eliminar la tabla 'bloques' completamente
        self.cursor.execute("DROP TABLE IF EXISTS bloques")
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()
        
        
#if __name__ == "__main__":
    #gestor = GestorBD()
    #gestor.borrar_todos_los_bloques()
    #gestor.borrar_tabla()
    