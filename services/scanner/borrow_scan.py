from models.repositories.mongo_db_borrowing_repository import MongoDBBorrowingRepository
from langchain_openai import ChatOpenAI
from utils.prompt_store import database_prompt
from langchain.agents import AgentExecutor, create_react_agent
from env_utils import get_env_vars
from langchain_mcp_adapters.client import MultiServerMCPClient

def scan_borrowings(collection_name: str = 'borrowings'):
    repository = MongoDBBorrowingRepository()
    borrowings = repository.list_all()
    for borrowing in borrowings:
        print(borrowing)

def create_scanner_agent() -> AgentExecutor:
    agent_llm = prepare_llm()
    tools = []  # Aquí irán las herramientas MCP
    # Usar create_react_agent para que acepte {"input": ...}
    react_agent = create_react_agent(agent_llm, tools)
    agent = AgentExecutor(
        agent=react_agent,
        tools=tools,
        verbose=True
    )
    return agent

def prepare_mcp_client():
    #TODO usar mcp_json_fetcher y cargar el MCPServerClient desde el json
    return MultiServerMCPClient({
            "MongoDB": {
                "command": "npx",
                "args": [
                "-y",
                "mongodb-mcp-server",
                "--connectionString",
                "mongodb://localhost:27017/libraryBD"
                ]
            }
        }
    )

def prepare_llm():
    llm = ChatOpenAI(
        api_key=get_env_vars()["LLM_KEY"],
        model_name="mixtral-8x7b-32768",
        base_url=get_env_vars()["LLM_URL"],
        temperature=0
    )
    chain = llm | database_prompt()
    return chain

def use_scanner_agent() -> str:
    agent: AgentExecutor = create_scanner_agent()
    # Si tu versión de langchain es asíncrona, usa: result = await agent.ainvoke({"input": "Menciona 3 bases de datos"})
    result = agent.invoke({
        "input": "Menciona 3 bases de datos"
    })
    # El resultado puede ser un dict, revisa la clave correcta (usualmente 'output' o similar)
    if isinstance(result, dict) and "output" in result:
        return result["output"]
    return str(result)