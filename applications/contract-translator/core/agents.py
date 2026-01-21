"""
Agent creation and configuration for CrewAI

Defines specialized agents for each translation phase:
- Parser Agent: Extract structured contract data
- Generator Agent: Create Solidity code
- Auditor Agent: Security analysis
- ABI Agent: Generate contract ABI
- MCP Agent: Generate MCP server code

Also provides a reinforcement loop pipeline that iterates on contract generation
and validation, learning from previous errors through conditional task execution.
"""

import io
import sys
from contextlib import redirect_stdout
from typing import Callable, Optional

import os
from crewai import Agent, Task, Crew, LLM as CrewLLM
from pydantic import BaseModel


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


class ContractData(BaseModel):
    """Pydantic model for contract data passed through the task pipeline."""
    extracted_terms: Optional[dict] = None
    contract_code: Optional[str] = None
    security_audit: Optional[str] = None
    audit_passed: bool = False
    refinement_needed: bool = False
    error_log: Optional[str] = None
    abi_spec: Optional[str] = None
    mcp_server_code: Optional[str] = None


def create_reinforcement_pipeline(
    contract_input: str,
    crew_llm: CrewLLM,
    tools: Optional[list] = None,
    on_log: Optional[Callable[[str], None]] = None,
) -> tuple[ContractData, str]:
    """
    Create a reinforcement learning pipeline for contract generation.
    
    The pipeline follows this workflow:
    1. Parse: Extract contract terms and requirements
    2. Generate: Create initial Solidity code
    3. Audit: Perform security analysis
    4. Refine: Fix issues if audit fails (conditional)
    5. Re-audit: Re-validate after refinement (conditional)
    6. Generate ABI: Create ABI specification
    7. Generate MCP: Create MCP server code
    
    Args:
        contract_input: Legal contract or requirements as string
        crew_llm: CrewAI LLM instance
        tools: Optional list of tools to provide to agents
        on_log: Optional callback function to receive log updates
        
    Returns:
        Tuple of (final_contract_data, log_output)
    """
    if tools is None:
        tools = []
    
    # Create all agents
    agents_dict = create_agents(crew_llm)
    
    # Task 1: Parse contract and extract terms
    task_parse = Task(
        description=(
            f"Extract structured information from the contract:\n{contract_input}\n\n"
            "Identify: function names, state variables, business logic requirements, "
            "access control needs, and key states."
        ),
        expected_output="Extracted contract terms and requirements as structured data",
        agent=agents_dict['parser_agent'],
        tools=tools,
        memory_key="contract_data"
    )
    
    # Task 2: Generate initial Solidity contract
    task_generate = Task(
        description=(
            "Generate a complete, production-ready Solidity smart contract based on "
            "the extracted contract terms. Include proper error handling, access control, "
            "and comprehensive state management."
        ),
        expected_output="Complete Solidity smart contract code",
        agent=agents_dict['generator_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data"
    )
    
    # Task 3: Perform security audit
    task_audit = Task(
        description=(
            "Audit the generated Solidity contract for security vulnerabilities. "
            "Check for: reentrancy issues, integer overflow/underflow, access control "
            "problems, unchecked external calls, and other common exploits. "
            "Provide detailed findings."
        ),
        expected_output="Security audit report with vulnerabilities and risk assessment",
        agent=agents_dict['auditor_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data"
    )
    
    # Task 4: Refine contract based on audit findings (conditional)
    task_refine = Task(
        description=(
            "Fix all identified security vulnerabilities and issues in the Solidity contract. "
            "Rewrite problematic sections to follow best practices and ensure all audit "
            "findings are addressed."
        ),
        expected_output="Refined Solidity smart contract with vulnerabilities fixed",
        agent=agents_dict['generator_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data",
        should_write_memory=True,
        condition=lambda mem: (
            hasattr(mem, 'contract_data') and 
            mem.contract_data.refinement_needed
        )
    )
    
    # Task 5: Re-audit after refinement (conditional)
    task_re_audit = Task(
        description=(
            "Re-audit the refined Solidity contract to verify that all previously "
            "identified vulnerabilities have been fixed and no new issues were introduced."
        ),
        expected_output="Final security audit report confirming vulnerability fixes",
        agent=agents_dict['auditor_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data",
        should_write_memory=True,
        condition=lambda mem: (
            hasattr(mem, 'contract_data') and 
            mem.contract_data.refinement_needed
        )
    )
    
    # Task 6: Generate ABI specification
    task_abi = Task(
        description=(
            "Generate the complete Ethereum ABI (Application Binary Interface) "
            "specification from the final Solidity contract. Include all functions, "
            "events, constructor parameters, and state variable accessors."
        ),
        expected_output="JSON ABI specification for the smart contract",
        agent=agents_dict['abi_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data",
        should_write_memory=True
    )
    
    # Task 7: Generate MCP server code
    task_mcp = Task(
        description=(
            "Generate a complete, production-ready MCP (Model Context Protocol) server "
            "for interacting with the deployed smart contract. Include proper error handling, "
            "transaction management, and Web3.py integration."
        ),
        expected_output="Python MCP server code for smart contract interaction",
        agent=agents_dict['mcp_agent'],
        tools=tools,
        input_variables=["contract_data"],
        memory_key="contract_data",
        should_write_memory=True
    )
    
    # Create crew with all tasks in reinforcement order
    crew = Crew(
        agents=[
            agents_dict['parser_agent'],
            agents_dict['generator_agent'],
            agents_dict['auditor_agent'],
            agents_dict['mcp_agent'],
            agents_dict['abi_agent'],
        ],
        tasks=[task_parse, task_generate, task_audit, task_refine, task_re_audit, task_abi, task_mcp],
        verbose=True,
        output_memory_key="contract_data"
    )
    
    # Capture logs during execution
    log_buffer = io.StringIO()
    original_stdout = sys.stdout
    
    class _StdoutLogger:
        def write(self, data):
            original_stdout.write(data)
            log_buffer.write(data)
            if on_log:
                on_log(log_buffer.getvalue())
            return len(data)
        
        def flush(self):
            original_stdout.flush()
    
    # Run the reinforcement pipeline
    with redirect_stdout(_StdoutLogger()):
        result = crew.kickoff(inputs={"description": contract_input})
    
    # Extract final contract data from crew output
    final_data = None
    
    # Strategy 1: Check tasks_output for ContractData
    if hasattr(result, "tasks_output") and result.tasks_output:
        for task_output in reversed(result.tasks_output):
            if hasattr(task_output, "pydantic") and task_output.pydantic:
                pydantic_obj = task_output.pydantic
                if isinstance(pydantic_obj, ContractData):
                    final_data = pydantic_obj
                    break
            elif isinstance(task_output, ContractData):
                final_data = task_output
                break
    
    # Strategy 2: Check if result itself is ContractData
    if not final_data and isinstance(result, ContractData):
        final_data = result
    
    # Strategy 3: Create ContractData from dict if available
    if not final_data and isinstance(result, dict):
        try:
            final_data = ContractData(**result)
        except Exception:
            pass
    
    # Fallback: Create minimal ContractData with logs
    if not final_data:
        final_data = ContractData(
            error_log=str(result) if result else "No contract data extracted"
        )
    
    return final_data, log_buffer.getvalue()


__all__ = [
    'create_agents',
    'create_reinforcement_pipeline',
    'ContractData',
    '_convert_to_crew_llm'
]
