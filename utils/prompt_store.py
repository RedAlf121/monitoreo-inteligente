from langchain_core.prompts import ChatPromptTemplate
def database_prompt():
    prompt = ChatPromptTemplate(
        messages=[
            ("system", "You are a helpful assistant that can answer questions about a database."),
            ("user", "{input}")
        ]
    )
    return prompt

def document_prompt():
    prompt = ChatPromptTemplate(
        messages=[
            ("system", "You are a helpful assistant that can answer questions about a document."),
            ("user", "{input}")
        ]
    )
    return prompt
