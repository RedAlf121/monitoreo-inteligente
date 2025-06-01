from services.messager.email.models import Customer
from services.messager.messager import send
from models.agent.agent_builder import MCPAgentBuilder, MCPAgent
from models.agent.prompt_factory import database_prompt
from models.agent.model_factory import ModelFactory
from models.agent.tools_loader import load_mcp_config_from_json

async def get_agent_response():
    prompt = database_prompt()
    agent = MCPAgentBuilder(MCPAgent).\
                with_prompt(prompt).\
                with_mcp_servers(load_mcp_config_from_json()).\
                with_model("groq","qwen-qwq-32b").\
                build()
    await agent.setup()
        
    response = await agent.run("""
            List all users with this format
            {
                name: string,
                email: string,
                books: [string],
                category: string
            }
        """)
    
    return response



async def scan_borrowings():
    try:
        response = await get_agent_response()
        print(response)
        if not response["users"]:
            raise Exception("Error trying to access the database")
        if response["users"]==[]:
            print("No users found")
            return
        
        #if there are users, send the message
        for user in response["users"]:
            customer = Customer(
                name=user["name"],
                email=user["email"],
                books=user["books"],
                category=user["category"]
            )
            send(message_type="email",customer=customer)
            print(f"mensaje al usuario {user['name']} fue enviado!")
    except EOFError as e:
        return EOFError("Cache is empty. Try a successful connection at least.")
    except Exception as e:
        print("Error en el envio")
        e.with_traceback()




#def scan_borrowings():
#    try:
#        response = {
#             "users": [
#                  {
#                       "name": "Joe",
#                       "email": "francismirezdpl@gmail.com",
#                       "books": ["a","b","c"],
#                       "category": "estudiante"
#                  },
#                  {
#                       "name": "Frank",
#                       "email": "francismirezdpl@gmail.com",
#                       "books": ["a","b","c"],
#                       "category": "estudiante"
#                  },
#                  {
#                       "name": "Evan",
#                       "email": "francismirezdpl@gmail.com",
#                       "books": ["a","b","c"],
#                       "category": "estudiante"
#                  }
#             ]
#        }
#        print(response)
#        for user in response["users"]:
#            customer = Customer(
#                name=user["name"],
#                email=user["email"],
#                books=user["books"],
#                category=user["category"]
#            )
#            send(message_type="email",customer=customer)
#            print(f"mensaje al usuario {user['name']} fue enviado!")
#    except EOFError as e:
#        return EOFError("Cache is empty. Try a successful connection at least.")
#    except Exception as e:
#        print("Error en el envio")
#        e.with_traceback()
#