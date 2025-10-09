# aurelion_menu.py
# Sistema de consulta interactiva de documentación del proyecto Aurelion
# Curso: Guayerd
# Para hacerlo funcionar colocar en la terminal python aurelion_menu.py


import os
import re

# Ruta fija al archivo Documentacion.md
RUTA_DOC = os.path.join(os.path.dirname(__file__), "Documentacion.md")

def cargar_documentacion():
    """Lee y devuelve el contenido del archivo Documentacion.md."""
    if not os.path.exists(RUTA_DOC):
        print("⚠️ No se encontró el archivo Documentacion.md en el directorio actual.")
        return None
    with open(RUTA_DOC, "r", encoding="utf-8") as f:
        return f.read()

def extraer_seccion(contenido, numero):
    """
    Extrae el contenido de una sección específica según el número del encabezado.
    Por ejemplo: número = 1 extrae desde '## 1.' hasta antes de '## 2.'
    """
    # Busca el encabezado que empieza con "## {numero}."
    patron_inicio = rf"(^##\s*{numero}\..*?$)"
    # Busca el encabezado del siguiente punto
    patron_fin = rf"(^##\s*{numero + 1}\..*?$)"
    
    secciones = re.split(patron_inicio, contenido, flags=re.MULTILINE)
    
    if len(secciones) < 3:
        return "⚠️ No se encontró la sección solicitada."
    
    # Secciones: [antes, encabezado, contenido restante...]
    encabezado = secciones[1]
    contenido_restante = secciones[2]
    
    # Cortar hasta el siguiente encabezado
    partes = re.split(patron_fin, contenido_restante, maxsplit=1, flags=re.MULTILINE)
    texto_final = encabezado + partes[0]
    return texto_final.strip()

def mostrar_menu():
    print("\n📚 MENÚ DE DOCUMENTACIÓN AURELION")
    print("1️⃣  Tema, problema y solución")
    print("2️⃣  Dataset de referencia")
    print("3️⃣  Descripción de las tablas y análisis")
    print("4️⃣  Escala de medición")
    print("5️⃣  Sugerencias y mejoras de Copilot")
    print("6️⃣  Ver todo el documento")
    print("0️⃣  Salir")

def main():
    contenido = cargar_documentacion()
    if not contenido:
        return

    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "0":
            print("👋 Saliendo del programa.")
            break
        elif opcion == "6":
            print("\n📘 Mostrando todo el documento completo:\n")
            print("-" * 60)
            print(contenido)
            print("-" * 60)
        elif opcion in {"1", "2", "3", "4", "5"}:
            numero = int(opcion)
            seccion = extraer_seccion(contenido, numero)
            print(f"\n📘 Mostrando sección: {numero}\n" + "-" * 60)
            print(seccion)
            print("-" * 60)
        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
