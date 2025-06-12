from .model_factory import CHAT_MODELS_DICT
from .prompt_factory import database_prompt
from .tools_loader import get_tools_with_cache
from langchain.agents import AgentExecutor, create_tool_calling_agent
from .tools_loader import get_tools_with_cache

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
        self.toolkit = None
    
    def set_mcp_servers(self, mcp_servers: dict):
        self.mcp_config = mcp_servers

    def set_toolkit(self, toolkit):
        self.toolkit=toolkit

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_tools(self, tools: list):
        self.tools = tools

    def set_model(self,model_type:str, model_name:str):
        self.model_name = model_name
        self.model_type = model_type
    
    def set_max_iterations(self,max_iterations):
        self.max_iterations = max_iterations

    async def setup(self):
        print("Loading language model...")
        self.llm = CHAT_MODELS_DICT[self.model_type](model_name=self.model_name)
        print("Loading tools...")
        mcp_tools = []
        toolkit_tools = []
        if self.mcp_config != {}:
            mcp_tools = await get_tools_with_cache(self.mcp_config)
        if self.toolkit is not None:
            toolkit_tools = self.toolkit(self.llm).tools()
        self.tools = [*mcp_tools,*toolkit_tools]
        print("Loading prompt...")
        self.prompt = database_prompt()
        print("Creating agent...")
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        print("Creating executor...")
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            prompt=self.prompt,
            max_iterations=self.max_iterations,
            verbose=True
        )

    async def run(self, user_input: str):
        if not self.executor:
            await self.setup()
        print("Executing agent...")
        result = await self.executor.ainvoke({
            "input": user_input,
            "tools": [(tool.name, tool.description) for tool in self.tools],
            "top_k": 10
        })
        print("Execution finished.")
        print(result)
        return result["output"]

class MCPAgentBuilder:
    def __init__(self, agent_class: type[MCPAgent] = MCPAgent):
        self._agent = agent_class()
        print(type(self._agent))

    def with_model(self, model_type:str, model_name:str):
        self._agent.set_model(model_type,model_name)
        return self
    def with_toolkit(self,toolkit):
        self._agent.set_toolkit(toolkit)
        return self
    def with_max_iterations(self,max_iterations):
        self._agent.set_max_iterations(max_iterations)
        return self
    
    def with_mcp_servers(self, mcp_servers: dict):
        print(f"[AgentBuilder] Setting MCP servers: {list(mcp_servers.keys())}")
        self._agent.set_mcp_servers(mcp_servers)
        return self

    def with_prompt(self, prompt):
        print(f"[AgentBuilder] Setting prompt.")
        self._agent.set_prompt(prompt)
        return self

    def with_tools(self, tools: list):
        print(f"[AgentBuilder] Setting tools: {len(tools)} tool(s)")
        self._agent.set_tools(self._tools)
        return self

    def build(self):
        print("[AgentBuilder] Building agent...")
        
        agent = self._agent
        self.clear()
        print("[AgentBuilder] Agent built successfully.")
        return agent

    def clear(self):
        self._agent = None
