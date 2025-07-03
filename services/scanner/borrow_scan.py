import time
from services.messager.email.models import Customer
from services.messager.messager import send
from models.agent.agent_builder import MCPAgentBuilder, MCPAgent
from models.agent.prompt_factory import database_prompt
from models.agent.model_factory import ModelFactory
from models.agent.tools_loader import load_mcp_config_from_json
from models.user import Users
from models.agent.prompt_factory import user_parser
from models.notified_status import NotifiedStatus
from models.book import Book
import json
import asyncio
import re



def extract_json_from_text(text):
    """
    Extract the first valid JSON object or array from a string, even if nested or multiline.
    """
    import json

    # Remove leading/trailing whitespace
    text = text.strip()
    # Try to find the first '{' or '['
    start = min([i for i in [text.find('{'), text.find('[')] if i != -1], default=-1)
    if start == -1:
        return None

    stack = []
    for i, char in enumerate(text[start:], start=start):
        if char in '{[':
            stack.append(char)
        elif char in '}]':
            if not stack:
                break
            opening = stack.pop()
            if (opening == '{' and char != '}') or (opening == '[' and char != ']'):
                break
            if not stack:
                try:
                    return text[start:i+1]
                except Exception:
                    break
    return None

async def get_agent_response():
    start_time = time.time()
    prompt = database_prompt()
    print(prompt)
    agent = await MCPAgentBuilder(MCPAgent).\
                with_prompt(prompt).\
                with_max_iterations(30).\
                with_model("groq","qwen-qwq-32b").\
                build()
    response = await agent.run("""
            List all users that have borrowed a book
        """)
    # Post-process output to extract JSON
    end_time = time.time()
    print(f"Tiempo transcurrido {end_time-start_time}")
    clean_response = extract_json_from_text(response['output'][0]['text'])
    print(clean_response)
    return clean_response


def mock_agent_response():
    """
    Return a fake user list for testing other features.
    """
    return {
        "userList": [
            {
                "name": "Juan Perez",
                "email": "francismirezdpl@gmail.com",
                "books": [
                    {"title": "Python Básico", "code": "osdjasojdo", "due_date": "2025-07-01"},
                    {"title": "Machine Learning", "code": "osdjasojdo", "due_date": "2025-07-10"}
                ]
            },
            {
                "name": "Ana Gómez",
                "email": "francismirezdpl@gmail.com",
                "books": [
                    {"title": "Bases de Datos", "code": "osdjasojdo", "due_date": "2025-07-05"}
                ]
            }
        ]
    }

def process_notification_status(users):
    status = NotifiedStatus()
    for user in users.userList:
        customer = Customer(
            name=user.name,
            email=user.email,
            books=user.books,
        )
        try:
            send(message_type="email", customer=customer)
            print(f"mensaje al usuario {user.name} fue enviado!")
            status.add_notified(user.email)
        except Exception as e:
            print(f"No se pudo notificar a {user.name}")
            status.add_not_notified(user.email)
    return status

def save_notification_status(status: NotifiedStatus):
    with open("notified_status.json", "w", encoding="utf-8") as f:
        json.dump(status.to_dict(), f, ensure_ascii=False, indent=2)

async def scan_borrowings():
    try:
        response = await get_agent_response()
        parser = user_parser()
        try:
            users: Users = parser.parse(response)
            print(response)
        except Exception as e:
            print("error de parsing")
            print(e)
            return
        if users is None or users == []:
            print("No users found")
            return
        status = process_notification_status(users)
        save_notification_status(status)
        return status.to_dict()
    except EOFError as e:
        return EOFError("Cache is empty. Try a successful connection at least.")
    except Exception as e:
        print("Error en el envio")
        print(e)
async def scan_mock_borrowings():
    try:
        print("Working..")
        response = mock_agent_response()
        from models.user import User, Users
        # Corregir la conversión de la lista de libros
        users = Users(userList=[
            User(
                name=user["name"],
                email=user["email"],
                books=[Book(**book) for book in user["books"]]
            )
            for user in response["userList"]
        ])
        status = process_notification_status(users)
        save_notification_status(status)
        for user in users.userList:
            print(user)
        return status.to_dict()
    except EOFError as e:
        return EOFError("Cache is empty. Try a successful connection at least.")
    except Exception as e:
        print("Error en el envio")
        print(e)

def start_scanner():
    asyncio.run(scan_borrowings())