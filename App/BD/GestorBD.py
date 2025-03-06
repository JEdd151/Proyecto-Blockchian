#En esta clase hace la conexion a la bd
from App.Blockchain.Bloque import Bloque
import sqlite3
import json
from contextlib import contextmanager

class GestorBD:
    def __init__(self, bd_path="blockchain.db"):
        self.bd_path = bd_path
        self.crear_tabla_si_no_existe()

    @contextmanager
    def conectar_bd(self):
        """
        Context manager para manejar la conexión a la base de datos.
        """
        conn = sqlite3.connect(self.bd_path)
        conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.commit()
            conn.close()

    def crear_tabla_si_no_existe(self):
        """
        Crea la tabla 'bloques' si no existe.
        """
        with self.conectar_bd() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bloques (
                    indice INTEGER PRIMARY KEY,
                    datos TEXT NOT NULL,
                    hash_anterior TEXT,
                    hash_actual TEXT,
                    proof INTEGER NOT NULL
                )
            """)

    def guardar_bloque(self, bloque):
        """
        Guarda un bloque en la base de datos.
        """
        with self.conectar_bd() as cursor:
            cursor.execute("""
                INSERT INTO bloques (indice, datos, hash_anterior, hash_actual, proof)
                VALUES (?, ?, ?, ?, ?)
            """, (bloque.index, json.dumps(bloque.datos), bloque.hash_anterior, bloque.hash_actual, bloque.proof))

    def cargar_bloques(self):
        """
        Carga todos los bloques de la base de datos.

        :return: Lista de instancias de la clase Bloque.
        """
        with self.conectar_bd() as cursor:
            cursor.execute("SELECT * FROM bloques ORDER BY indice")
            bloques = cursor.fetchall()

            bloques_recuperados = []
            for bloque in bloques:
                index = bloque["indice"]
                datos = json.loads(bloque["datos"])
                hash_anterior = bloque["hash_anterior"]
                hash_actual = bloque["hash_actual"]
                proof = bloque["proof"]

                nuevo_bloque = Bloque(index, datos, hash_anterior, proof)
                nuevo_bloque.hash_actual = hash_actual
                bloques_recuperados.append(nuevo_bloque)

            return bloques_recuperados

    def borrar_todos_los_bloques(self):
        """
        Borra todos los bloques de la tabla 'bloques'.
        """
        with self.conectar_bd() as cursor:
            cursor.execute("DELETE FROM bloques")

    def borrar_tabla(self):
        """
        Elimina la tabla 'bloques' completamente.
        """
        with self.conectar_bd() as cursor:
            cursor.execute("DROP TABLE IF EXISTS bloques")

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos.
        """
        # No es necesario cerrar la conexión manualmente cuando se usa contextmanager
        print("La conexión se cierra automáticamente al salir del contexto.")
        
#if __name__ == "__main__":
#    gestor = GestorBD()
#    gestor.borrar_todos_los_bloques()
#    gestor.borrar_tabla()
    