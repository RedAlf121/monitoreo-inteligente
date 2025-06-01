from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
class ModelFactory:

    @staticmethod
    def build_groq_model(model_name: str = "qwen-qwq-32b"):
        return ChatGroq(model_name=model_name)

    @staticmethod
    def build_ollama_model(model_name: str):
        return ChatOllama(model=model_name)

CHAT_MODELS_DICT = {
    "ollama": ModelFactory.build_ollama_model,
    "groq": ModelFactory.build_groq_model
}
__all__ = [CHAT_MODELS_DICT]