"""
Agent creation and configuration for CrewAI

Defines specialized agents for each translation phase:
- Parser Agent: Extract structured contract data
- Generator Agent: Create Solidity code
- Auditor Agent: Security analysis
- ABI Agent: Generate contract ABI
- MCP Agent: Generate MCP server code
"""

import os
from crewai import Agent, LLM as CrewLLM


def _convert_to_crew_llm(agentics_llm) -> CrewLLM:
    """
    Convert Agentics LLM to CrewAI LLM format.
    Both use similar underlying structure, so we extract the model name and create a CrewAI LLM.
    """
    # Get the model name from the Agentics LLM
    model_name = getattr(agentics_llm, 'model', 'gpt-4o-mini')
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Create CrewAI LLM with same configuration
    return CrewLLM(
        model=model_name,
        api_key=api_key,
        temperature=0.7
    )


def create_agents(crew_llm: CrewLLM) -> dict:
    """
    Create all specialized agents for the translation pipeline.
    
    Args:
        crew_llm: CrewAI LLM instance
        
    Returns:
        Dictionary with agent instances for each phase
    """
    
    # Phase 2: Contract Parser Agent
    parser_agent = Agent(
        role="Contract Analysis Expert",
        goal="Extract precise, specific information from legal contracts",
        backstory=(
            "You are an expert contract analyst specializing in extracting exact terminology, "
            "function names, variable names, states, and conditions from legal documents. "
            "You never use generic placeholders - only specific terms from the contract."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 3: Solidity Generator Agent
    generator_agent = Agent(
        role="Solidity Smart Contract Developer",
        goal="Generate complete, production-ready Solidity smart contracts",
        backstory=(
            "You are a Solidity expert who generates COMPLETE, FUNCTIONAL smart contracts. "
            "You implement every function with full logic, use require() for validation, "
            "implement proper access control, and ensure all variables are actively used. "
            "You never write placeholder code or empty functions."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 4: Security Auditor Agent
    auditor_agent = Agent(
        role="Blockchain Security Auditor",
        goal="Identify security vulnerabilities in smart contracts",
        backstory=(
            "You are a blockchain security expert who audits smart contracts for vulnerabilities. "
            "You check for reentrancy, access control issues, integer overflow, and other common exploits."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 5: ABI Generator Agent
    abi_agent = Agent(
        role="Ethereum ABI Specialist",
        goal="Generate accurate ABI specifications from Solidity contracts",
        backstory=(
            "You are an Ethereum ABI expert who generates complete, accurate ABI JSON "
            "from Solidity contracts, including all functions, events, and constructor details."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 6: MCP Server Generator Agent
    mcp_agent = Agent(
        role="MCP Server Developer",
        goal="Generate production-ready MCP server code for blockchain interaction",
        backstory=(
            "You are an expert Python developer specializing in Web3.py and MCP server generation. "
            "You create complete, self-contained MCP servers with proper error handling and "
            "transaction management for smart contract interaction."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    return {
        'parser_agent': parser_agent,
        'generator_agent': generator_agent,
        'auditor_agent': auditor_agent,
        'abi_agent': abi_agent,
        'mcp_agent': mcp_agent,
    }


__all__ = ['create_agents', '_convert_to_crew_llm']
