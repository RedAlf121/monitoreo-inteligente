import os
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_cohere import ChatCohere
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
class ModelFactory:

    @staticmethod
    def build_groq_model(model_name: str = "qwen-qwq-32b"):
        return ChatGroq(model_name=model_name,temperature=0.01)

    @staticmethod
    def build_ollama_model(model_name: str):
        return ChatOllama(model=model_name, temperature=0.01)

    @staticmethod
    def build_gemini_model(model_name: str):
        return ChatGoogleGenerativeAI(model=model_name, temperature=0.01)

    @staticmethod
    def build_mistral_model(model_name: str):
        return ChatMistralAI(model_name=model_name, temperature=0.01)
    
    @staticmethod
    def build_cohere_model(model_name: str = ""):
        return ChatCohere(temperature=0.01)

    @staticmethod
    def build_anthropic_model(model_name:str):
        return ChatAnthropic(model_name=model_name, temperature=0.01)

    @staticmethod
    def build_azure_model(model_name: str):
        """
        Now the model available is: openai/gpt-4.1
        """
        return AzureAIChatCompletionsModel(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(os.getenv("GITHUB_MODELS_API_KEY")),
            model=model_name,
            temperature=0.01
        )

    @staticmethod
    def build_openai_model(model_name:str):
        return ChatOpenAI(model_name=model_name, temperature=0.01)

    @staticmethod
    def build_huggingface_model(model_name: str):
        """
        model_name: str for Hugging Face Inference Providers use this notation
        <provider>@<repo_id>
        """
        provider,model_id = model_name.split('@')
        endpoint = HuggingFaceEndpoint(
            repo_id=model_id,
            provider=provider,
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            temperature=0.01
        )

        return ChatHuggingFace(llm=endpoint)

CHAT_MODELS_DICT = {
    "ollama": ModelFactory.build_ollama_model,
    "groq": ModelFactory.build_groq_model,
    "huggingface": ModelFactory.build_huggingface_model,
    "azure": ModelFactory.build_azure_model,
    "cohere": ModelFactory.build_cohere_model,
    "mistral": ModelFactory.build_mistral_model,
    "gemini": ModelFactory.build_gemini_model,
    "openai": ModelFactory.build_openai_model,
    "anthropic": ModelFactory.build_anthropic_model
}
__all__ = [CHAT_MODELS_DICT]