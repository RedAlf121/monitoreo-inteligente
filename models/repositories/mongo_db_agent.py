from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

# Importamos nuestras utilidades de MongoDB que solo tienen operaciones de lectura
from models.repositories.mongo_db_utils import MongoDBUtils


def create_mongodb_tools() -> List[Tool]:
    """
    Crea las herramientas de MongoDB para operaciones de solo lectura.
    """
    
    # Herramienta para conectarse a MongoDB
    connect_tool = Tool(
        name="conectar_mongodb",
        func=lambda connection_string, db_name="libraryBD": MongoDBUtils.connect(connection_string, db_name),
        description="Conecta a una base de datos MongoDB. Requiere connection_string y opcionalmente db_name (por defecto es 'libraryBD').",
    )
    
    # Herramienta para conectarse a MongoDB usando variables de entorno
    connect_env_tool = Tool(
        name="conectar_mongodb_desde_env",
        func=lambda: MongoDBUtils.connect_from_env(),
        description="Conecta a MongoDB usando la variable de entorno DB_ROUTE, con base de datos 'libraryBD'.",
    )
    
    # Herramienta para listar bases de datos
    list_databases_tool = Tool(
        name="listar_bases_datos",
        func=lambda: MongoDBUtils.list_databases(),
        description="Lista todas las bases de datos disponibles en la conexión MongoDB actual.",
    )
    
    # Herramienta para listar colecciones
    list_collections_tool = Tool(
        name="listar_colecciones",
        func=lambda: MongoDBUtils.list_collections(),
        description="Lista todas las colecciones disponibles en la base de datos MongoDB actual.",
    )
    
    # Herramienta para buscar todos los documentos en una colección
    find_all_tool = Tool(
        name="buscar_todos",
        func=lambda collection_name, limit=100: MongoDBUtils.find_all(collection_name, limit),
        description="Busca todos los documentos en una colección. Argumentos: collection_name, limit (opcional, por defecto 100).",
    )
    
    # Herramienta para buscar un documento por ID
    find_by_id_tool = Tool(
        name="buscar_por_id",
        func=lambda collection_name, id: MongoDBUtils.find_by_id(collection_name, id),
        description="Busca un documento por ID. Argumentos: collection_name, id.",
    )
    
    # Herramienta para buscar documentos con un filtro
    find_with_filter_tool = Tool(
        name="buscar_con_filtro",
        func=lambda collection_name, filter_query, limit=100: MongoDBUtils.find_with_filter(collection_name, filter_query, limit=limit),
        description="Busca documentos con un filtro específico. Argumentos: collection_name, filter_query (dict), limit (opcional).",
    )
    
    # Herramienta para contar documentos
    count_tool = Tool(
        name="contar_documentos",
        func=lambda collection_name, filter_query=None: MongoDBUtils.get_count(collection_name, filter_query),
        description="Cuenta documentos en una colección, opcionalmente filtrados. Argumentos: collection_name, filter_query (opcional).",
    )
    
    # Herramienta para ejecutar agregaciones
    aggregate_tool = Tool(
        name="agregar",
        func=lambda collection_name, pipeline: MongoDBUtils.aggregate(collection_name, pipeline),
        description="Ejecuta una operación de agregación en una colección. Argumentos: collection_name, pipeline (lista de etapas).",
    )
    
    # Herramienta para obtener la fecha actual
    datetime_tool = Tool(
        name="obtener_fecha_hora",
        func=lambda: MongoDBUtils.get_current_datetime(),
        description="Obtiene la fecha y hora actual.",
    )
    
    # Herramienta para cerrar la conexión
    close_connection_tool = Tool(
        name="cerrar_conexion",
        func=lambda: MongoDBUtils.close_connection(),
        description="Cierra la conexión a MongoDB.",
    )
    
    return [
        connect_tool,
        connect_env_tool,
        list_databases_tool,
        list_collections_tool,
        find_all_tool,
        find_by_id_tool,
        find_with_filter_tool,
        count_tool,
        aggregate_tool,
        datetime_tool,
        close_connection_tool
    ]


def crear_agente_mongodb(llm=None):
    """
    Crea un agente de LangChain que utiliza herramientas de MongoDB.
    
    Args:
        llm: Opcional, modelo de lenguaje para el agente. Si es None, se usa ChatGroq.
    
    Returns:
        Un AgentExecutor configurado
    """
    # Cargar variables de entorno
    load_dotenv()
    
    if llm is None:
        # Usar ChatGroq en lugar de ChatOpenAI
        llm = ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",  # Modelo de Groq a utilizar
        )
    
    tools = create_mongodb_tools()
    
    prompt = PromptTemplate.from_template(
        """
        Eres un asistente especializado en consultar bases de datos MongoDB.
        Solo puedes realizar operaciones de lectura (no puedes escribir, actualizar ni eliminar datos).
        
        Tienes acceso a las siguientes herramientas:
        
        {tools}
        
        Para usar una herramienta, especifica `Action: nombre_herramienta` seguido de `Action Input: {{{{los argumentos JSON}}}}`.
        
        Humano: {input}
        
        Piénsalo paso por paso:
        """
    )
    
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )


# Ejemplo de uso del agente con una consulta sencilla
def ejemplo_consulta_simple():
    """
    Ejemplo sencillo de uso del agente para conectarse y listar documentos en MongoDB.
    """
    # Crear el agente
    agent = crear_agente_mongodb()
    
    # Definir la consulta
    consulta = """
    Conéctate a la base de datos MongoDB usando las variables de entorno,
    lista las colecciones disponibles y luego muestra los primeros 5 documentos
    de la colección 'documents' (si existe).
    """
    
    # Ejecutar la consulta
    try:
        resultado = agent.invoke({"input": consulta})
        print("Resultado:")
        print(resultado["output"])
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        # Asegurar que se cierre la conexión
        MongoDBUtils.close_connection()


if __name__ == "__main__":
    # Este bloque se ejecuta si el script se ejecuta directamente
    ejemplo_consulta_simple() 