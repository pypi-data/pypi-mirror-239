import inspect
from typing import List
from types import ModuleType
from langchain.agents import AgentType
from langchain.tools.base import BaseTool
from langchain.agents import initialize_agent
from promptflow.contracts.types import FilePath
from langchain.chat_models import AzureChatOpenAI
from promptflow.connections import AzureOpenAIConnection
from promptflow._core.tool_meta_generator import load_python_module_from_file

def find_tools(file_path: FilePath, llm: AzureChatOpenAI):
    module: ModuleType = load_python_module_from_file(file_path)
    tool_functions = [m for m in dir(module) if 
                      inspect.isfunction(getattr(module, m)) and
                      inspect.signature(getattr(module, m)).return_annotation == List[BaseTool]]

    if not tool_functions or len(tool_functions) == 0:
        raise ValueError(f"No tools function found in {file_path}")
        
    if len(tool_functions) > 1:
        raise ValueError(f"Too many tools functions found in {file_path}")

    tools = getattr(module, tool_functions[0])(llm)
    return tools

def zeroshotreact(connection: AzureOpenAIConnection, deployment_name: str, file_path: FilePath, intent: str):
    
    llm = AzureChatOpenAI(
        openai_api_key=connection.api_key,
        openai_api_base=connection.api_base,
        openai_api_version=connection.api_version,
        openai_api_type=connection.api_type,
        deployment_name=deployment_name,
        temperature=0,
    )

    tools = find_tools(file_path, llm)

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    response = agent.run(intent)

    return response