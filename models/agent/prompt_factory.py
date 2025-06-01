from langchain.prompts import ChatPromptTemplate

def database_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
         You are a helpful assistant that can make queries to a MongoDB database. You must connect tu libraryBD database.You have the following tools:
         {tools}
         """),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
