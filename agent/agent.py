from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from .llm import get_llm
from .tools import tools

# Load environment variables before creating agent
load_dotenv()

BASE_SYSTEM_PROMPT = """You are a helpful assistant that can answer questions and help with tasks. You can use the semantic_search tool to find relevant information from the knowledge base."""

_agent_instance = None

def create_agent_instance():
    """Initialize and return the LangChain agent"""
    llm = get_llm()
    
    agent = create_agent(
        model=llm,
        system_prompt=BASE_SYSTEM_PROMPT,
        tools=tools,
        debug=False
    )
    
    return agent


def get_agent_with_history():
    """Get agent instance (singleton pattern)"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_agent_instance()
    return _agent_instance