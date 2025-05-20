from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from langchain_core.language_models import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Mapping, Optional
from langchain_core.prompts import PromptTemplate

load_dotenv()

client = InferenceClient(
    provider="novita",
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

class HuggingFaceLLM(LLM):
    client: InferenceClient
    model: str
    
    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    
    @property
    def _llm_type(self) -> str:
        return "huggingface_inference"
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model}
        


llm = HuggingFaceLLM(client=client, model="deepseek-ai/DeepSeek-R1")
question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm
print(chain.invoke({"question": question}))