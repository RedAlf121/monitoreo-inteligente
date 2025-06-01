from typing import Optional, List, Dict, Any
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.cursor import Cursor
from bson import ObjectId
from dotenv import load_dotenv
import os


class MongoDBUtils:
    """
    Clase utilitaria para operaciones de lectura en MongoDB.
    """
    
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    
    @classmethod
    def connect(cls, connection_string: str, db_name: str = "libraryBD") -> None:
        """
        Conecta a una base de datos MongoDB.
        
        Args:
            connection_string: URL de conexión a MongoDB
            db_name: Nombre de la base de datos, por defecto 'libraryBD'
        """
        cls._client = MongoClient(connection_string)
        cls._db = cls._client[db_name]
    
    @classmethod
    def connect_from_env(cls) -> None:
        """
        Conecta a MongoDB utilizando variables de entorno.
        Requiere que la variable DB_ROUTE esté definida.
        """
        load_dotenv()
        connection_string = os.getenv("DB_ROUTE")
        if not connection_string:
            raise ValueError("La variable de entorno DB_ROUTE debe estar definida.")
        cls.connect(connection_string, "libraryBD")
    
    @classmethod
    def get_collection(cls, collection_name: str) -> Collection:
        """
        Obtiene una colección de la base de datos.
        
        Args:
            collection_name: Nombre de la colección
            
        Returns:
            Objeto Collection de pymongo
        
        Raises:
            ValueError: Si no se ha establecido una conexión previamente
        """
        if not cls._db:
            raise ValueError("No se ha establecido una conexión a la base de datos. Llame primero a connect() o connect_from_env().")
        return cls._db[collection_name]
    
    @classmethod
    def find_by_id(cls, collection_name: str, id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un documento por su ID.
        
        Args:
            collection_name: Nombre de la colección
            id: ID del documento (string)
            
        Returns:
            Documento encontrado o None
        """
        collection = cls.get_collection(collection_name)
        try:
            doc = collection.find_one({"_id": ObjectId(id)})
            if doc:
                # Convertir ObjectId a string para facilitar el manejo
                doc["_id"] = str(doc["_id"])
                return doc
            return None
        except Exception:
            return None
    
    @classmethod
    def find_all(cls, collection_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Recupera todos los documentos de una colección con un límite opcional.
        
        Args:
            collection_name: Nombre de la colección
            limit: Número máximo de documentos a devolver
            
        Returns:
            Lista de documentos
        """
        collection = cls.get_collection(collection_name)
        cursor = collection.find().limit(limit)
        result = []
        
        for doc in cursor:
            # Convertir ObjectId a string para facilitar el manejo
            doc["_id"] = str(doc["_id"])
            # Convertir cualquier otro ObjectId que pueda haber en el documento
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            result.append(doc)
        
        return result
    
    @classmethod
    def find_with_filter(cls, collection_name: str, filter_query: Dict[str, Any], 
                         projection: Optional[Dict[str, Any]] = None, 
                         limit: int = 100) -> List[Dict[str, Any]]:
        """
        Busca documentos que coincidan con un filtro específico.
        
        Args:
            collection_name: Nombre de la colección
            filter_query: Filtro de consulta en formato de MongoDB
            projection: Proyección para especificar campos a incluir/excluir
            limit: Número máximo de documentos a devolver
            
        Returns:
            Lista de documentos que coinciden con el filtro
        """
        collection = cls.get_collection(collection_name)
        cursor = collection.find(filter_query, projection).limit(limit)
        result = []
        
        for doc in cursor:
            # Convertir ObjectId a string para facilitar el manejo
            doc["_id"] = str(doc["_id"])
            # Convertir cualquier otro ObjectId que pueda haber en el documento
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            result.append(doc)
        
        return result
    
    @classmethod
    def find_one_with_filter(cls, collection_name: str, filter_query: Dict[str, Any], 
                            projection: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Busca un único documento que coincida con un filtro específico.
        
        Args:
            collection_name: Nombre de la colección
            filter_query: Filtro de consulta en formato de MongoDB
            projection: Proyección para especificar campos a incluir/excluir
            
        Returns:
            Documento que coincide con el filtro o None
        """
        collection = cls.get_collection(collection_name)
        doc = collection.find_one(filter_query, projection)
        if doc:
            # Convertir ObjectId a string para facilitar el manejo
            doc["_id"] = str(doc["_id"])
            # Convertir cualquier otro ObjectId que pueda haber en el documento
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            return doc
        return None
    
    @classmethod
    def get_count(cls, collection_name: str, filter_query: Optional[Dict[str, Any]] = None) -> int:
        """
        Cuenta documentos en una colección, opcionalmente filtrados.
        
        Args:
            collection_name: Nombre de la colección
            filter_query: Filtro opcional de consulta
            
        Returns:
            Número de documentos que coinciden con el filtro
        """
        collection = cls.get_collection(collection_name)
        if filter_query is None:
            return collection.estimated_document_count()
        return collection.count_documents(filter_query)
    
    @classmethod
    def aggregate(cls, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta una operación de agregación en una colección.
        
        Args:
            collection_name: Nombre de la colección
            pipeline: Lista de etapas de agregación de MongoDB
            
        Returns:
            Resultado de la agregación
        """
        collection = cls.get_collection(collection_name)
        cursor = collection.aggregate(pipeline)
        result = []
        
        for doc in cursor:
            # Convertir ObjectId a string para facilitar el manejo
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])
            # Convertir cualquier otro ObjectId que pueda haber en el documento
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
            result.append(doc)
        
        return result
    
    @classmethod
    def list_collections(cls) -> List[str]:
        """
        Lista las colecciones disponibles en la base de datos.
        
        Returns:
            Lista de nombres de colecciones
        """
        if not cls._db:
            raise ValueError("No se ha establecido una conexión a la base de datos. Llame primero a connect() o connect_from_env().")
        return cls._db.list_collection_names()
    
    @classmethod
    def list_databases(cls) -> List[str]:
        """
        Lista las bases de datos disponibles en el servidor.
        
        Returns:
            Lista de nombres de bases de datos
        """
        if not cls._client:
            raise ValueError("No se ha establecido una conexión al servidor. Llame primero a connect() o connect_from_env().")
        return cls._client.list_database_names()
    
    @classmethod
    def get_current_datetime(cls) -> datetime:
        """
        Obtiene la fecha y hora actual.
        
        Returns:
            Objeto datetime con la fecha y hora actual
        """
        return datetime.utcnow()
    
    @classmethod
    def close_connection(cls) -> None:
        """
        Cierra la conexión a MongoDB.
        """
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None 