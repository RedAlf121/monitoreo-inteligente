from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.pydantic import PydanticOutputParser
from ..user import Users
def user_parser():
    parser = PydanticOutputParser(pydantic_object=Users)
    return parser

def database_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", f"""
         You are a helpful assistant that can make queries to a MongoDB database. You must connect to libraryBD database.You have the following tools:
         {'{tools}'}
         {user_parser().get_format_instructions().replace('{',"{{").replace('}','}}')}
         """),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
