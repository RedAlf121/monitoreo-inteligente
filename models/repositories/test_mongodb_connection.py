from models.repositories.mongo_db_utils import MongoDBUtils
import json
from dotenv import load_dotenv
import os

def main():
    """
    Script simple para probar la conexión a MongoDB y listar documentos.
    Solo usa operaciones de lectura.
    """
    print("Iniciando prueba de conexión a MongoDB...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    try:
        # Paso 1: Conectar a la base de datos usando variables de entorno
        print("Conectando a MongoDB usando variables de entorno...")
        print(f"Conexión: {os.getenv('DB_ROUTE')}")
        print(f"Base de datos: libraryBD")
        MongoDBUtils.connect_from_env()
        print("Conexión establecida con éxito.")
        
        # Paso 2: Listar bases de datos disponibles
        print("\nListando bases de datos disponibles:")
        databases = MongoDBUtils.list_databases()
        print(json.dumps(databases, indent=2))
        
        # Paso 3: Listar colecciones en la base de datos actual
        print("\nListando colecciones en la base de datos libraryBD:")
        collections = MongoDBUtils.list_collections()
        print(json.dumps(collections, indent=2))
        
        # Paso 4: Contar documentos en algunas colecciones
        print("\nContando documentos en colecciones:")
        for collection_name in collections:
            count = MongoDBUtils.get_count(collection_name)
            print(f"- {collection_name}: {count} documentos")
        
        # Paso 5: Mostrar algunos documentos de la colección 'documents' si existe
        print("\nIntentando mostrar documentos de la colección 'documents':")
        if 'documents' in collections:
            documents = MongoDBUtils.find_all("documents", limit=5)
            print(f"Encontrados {len(documents)} documentos (mostrando hasta 5):")
            # Simplificamos el output para mejor visualización
            simplified_docs = []
            for doc in documents:
                # Solo mostramos algunos campos para claridad
                simplified = {
                    "id": doc.get("_id"),
                    "title": doc.get("title", "Sin título"),
                }
                simplified_docs.append(simplified)
            print(json.dumps(simplified_docs, indent=2))
        else:
            print("La colección 'documents' no existe en esta base de datos.")
            
            # Mostrar documentos de la primera colección disponible (como alternativa)
            if collections:
                first_collection = collections[0]
                print(f"\nMostrando documentos de la colección '{first_collection}':")
                docs = MongoDBUtils.find_all(first_collection, limit=5)
                print(f"Encontrados {len(docs)} documentos (mostrando hasta 5):")
                print(json.dumps(docs, indent=2, default=str))
    
    except Exception as e:
        print(f"Error durante la prueba de conexión: {e}")
    
    finally:
        # Cerrar la conexión al finalizar
        print("\nCerrando conexión a MongoDB...")
        MongoDBUtils.close_connection()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main() 