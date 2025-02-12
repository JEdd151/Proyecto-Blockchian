from App.Blockchain.ArbolM import ArbolMerkle 

if __name__ == "__main__":
    datos_prueba = ["Transaccion1", "Transaccion2"]

    # Crear árbol de Merkle
    arbol = ArbolMerkle(datos_prueba)
    arbol.generar_arbol()

    # Mostrar el árbol y la raíz
    print("Niveles del árbol:")
    arbol.mostrar_arbol()
    print("\n")
    print("\nRaíz de Merkle:")
    print(arbol.obtener_raiz())
