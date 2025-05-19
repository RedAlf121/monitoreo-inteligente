from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

def crear_agente_basico():
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear una instancia del modelo de lenguaje usando Groq
    llm = ChatGroq(
        model_name="llama3-8b-8192",  # Puedes cambiar al modelo que prefieras de Groq
        temperature=0,
        max_retries=2
    )
    
    # Crear una plantilla de prompt
    template = """
    Por favor, responde a la siguiente pregunta de manera clara y concisa:
    
    Pregunta: {pregunta}
    
    Respuesta:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["pregunta"])
    
    # Crear una cadena usando el método moderno con operador pipe
    # Esto reemplaza al LLMChain que está deprecado
    cadena = (
        {"pregunta": RunnablePassthrough()} 
        | prompt 
        | llm
    )
    
    return cadena

def responder_pregunta(pregunta):
    # Crear el agente
    agente = crear_agente_basico()
    
    # Obtener respuesta
    respuesta = agente.invoke(pregunta)
    
    return respuesta.content

# Ejemplo de uso
if __name__ == "__main__":
    pregunta_usuario = "q es una base de datos?"
    respuesta = responder_pregunta(pregunta_usuario)
    print("\nRespuesta:")
    print(respuesta) 