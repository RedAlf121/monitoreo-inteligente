from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain.output_parsers.pydantic import PydanticOutputParser
from ..user import Users
def user_parser():
    parser = PydanticOutputParser(pydantic_object=Users)
    return parser

def attach_rules():
    import os
    rules_path = os.path.join("cached_documents","rules", "rules.txt")
    with open(rules_path, "r", encoding="utf-8") as f:
        rules_text = f.read()
    return rules_text

def database_prompt():
    return ChatPromptTemplate([
        ("system", """
         You can make queries to a MongoDB database.
         You can only query the 'libraryBD' database.
         You have the following tool names: {tool_names}, and their descriptions: {tools}
         When building a query, ensure that:
         - The field names and value types match exactly those in the database (e.g., numbers as numbers, strings as strings).
         - At first check the collection and read the attributes. If you don't know the collections list the collections first
         - The filter is as specific as possible to retrieve the correct documents.
         You must return the answer only following these format instructions:
         {format_instructions}
         """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

def filter_prompt():
    return PromptTemplate(
        input_variables=["rules"],
        template="""
        Filtra las siguientes reglas para conservar SOLO aquellas que definen condiciones de 
        préstamo vencido (mora). Incluye únicamente reglas que especifiquen:
        1. Cuándo un préstamo se considera retrasado
        2. Condiciones que determinan que un ítem está fuera de plazo
        3. Definiciones explícitas de vencimiento
        Excluye:
        - Reglas sobre renovaciones
        - Sanciones aplicadas (excepto la condición de retraso)
        - Límites de préstamo no relacionados con el vencimiento
        Reglas extraídas:
        {rules}
        Reglas filtradas (SOLO condiciones de vencimiento):
        """
    )

def extraction_prompt():
    extraction_prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Eres un experto en reglas de negocio bibliotecarias. Analiza el siguiente texto y extrae 
        EXCLUSIVAMENTE reglas relacionadas con condiciones de préstamos que afecten al monitoreo 
        automatizado. Incluye solo reglas sobre:
        - Plazos de préstamo (por tipo de usuario o documento)
        - Condiciones de renovación
        - Sanciones por retraso
        - Restricciones de préstamo
        Ignora:
        - Procesos administrativos (formularios, registros)
        - Sistemas técnicos (como DOCTUS)
        - Reglas no relacionadas con préstamos/devoluciones
        Texto:
        {text}
        Reglas relevantes (solo condiciones verificables para monitoreo):
        """
    )
    
    return extraction_prompt
