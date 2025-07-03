from .model_factory import CHAT_MODELS_DICT
from .prompt_factory import database_prompt, user_parser
from models.agent.local import mongodb_tools
from .tools_loader import get_tools_with_cache
from langchain.agents import AgentExecutor, create_tool_calling_agent
from .tools_loader import get_tools_with_cache
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationSummaryMemory
class MCPAgent:
    def __init__(self, model_type="groq",model_name: str = "qwen-qwq-32b", max_iterations: int = 30):
        self.model_name = model_name
        self.model_type = model_type
        self.max_iterations = max_iterations
        self.tools = None
        self.llm = None
        self.prompt = None
        self.agent = None
        self.executor = None
        self.mcp_config = {}
        self.agent_function = create_tool_calling_agent
        self.memory = None
        self.use_memory = False

    def set_memory(self):
        self.use_memory = True

    def set_mcp_servers(self, mcp_servers: dict):
        self.mcp_config = mcp_servers

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_tools(self, tools: list):
        self.tools = tools

    def set_model(self,model_type:str, model_name:str):
        self.model_name = model_name
        self.model_type = model_type
    
    def set_max_iterations(self,max_iterations):
        self.max_iterations = max_iterations
    
    def set_agent(self, create_agent_function):
        self.agent_function = create_agent_function
        return self

    async def setup(self):
        print("Loading language model...")
        self.llm = CHAT_MODELS_DICT[self.model_type](model_name=self.model_name)
        if self.use_memory:
            self.memory = ConversationSummaryMemory(llm=self.llm)
        print("Loading tools...")
        mcp_tools = []
        if self.mcp_config != {}:
            mcp_tools = await get_tools_with_cache(self.mcp_config)
            self.tools = mcp_tools
        else:
            self.tools = mongodb_tools.get_tools()
        
        print(self.tools)
        print("Creating agent...")
        self.agent = self.agent_function(self.llm, self.tools, self.prompt)
        print("Creating executor...")
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            prompt=self.prompt,
            max_iterations=self.max_iterations,
            verbose=True,
        )

    async def run(self, user_input: str):
        if not self.executor:
            await self.setup()
        print("Executing agent...")
        result = await self.executor.ainvoke({
            "input": user_input,
            "tools": self.tools,
            "tool_names": [tool.name for tool in self.tools],
            "format_instructions": user_parser().get_format_instructions()
        })
        print("Execution finished.")
        print(result)
        return result

class MCPAgentBuilder:
    def __init__(self, agent_class: type[MCPAgent] = MCPAgent):
        self._agent = agent_class()
        print(type(self._agent))

    def with_model(self, model_type:str, model_name:str):
        """
        model_type: str type of model (e.g. "huggingface", "ollama", "groq")
        model_name: str model name it can be gpt-4o, qwen3-qwq and so on. For Hugging Face Inference Providers use this notation:
        provider@repo_id (e.g. novita@NousResearch/Hermes-2-Pro-Llama-3-8B)
        if you don't know which provider use, you can use auto instead
        """
        self._agent.set_model(model_type,model_name)
        return self
    def with_max_iterations(self,max_iterations):
        self._agent.set_max_iterations(max_iterations)
        return self

    def with_memory(self):
        self._agent.set_memory()
        return self

    def with_mcp_servers(self, mcp_servers: dict):
        print(f"[AgentBuilder] Setting MCP servers: {list(mcp_servers.keys())}")
        self._agent.set_mcp_servers(mcp_servers)
        return self
    
    def with_agent_function(self, create_agent_function):
        self._agent.set_agent(create_agent_function)
        return self

    def with_prompt(self, prompt):
        print(f"[AgentBuilder] Setting prompt.")
        self._agent.set_prompt(prompt)
        return self

    def with_tools(self, tools: list):
        print(f"[AgentBuilder] Setting tools: {len(tools)} tool(s)")
        self._agent.set_tools(self._tools)
        return self

    async def build(self):
        print("[AgentBuilder] Building agent...")
        agent = self._agent
        await agent.setup()
        self.clear()
        print("[AgentBuilder] Agent built successfully.")
        return agent

    def clear(self):
        self._agent = None
