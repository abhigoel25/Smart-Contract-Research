"""
Agent creation and configuration for CrewAI

Defines specialized agents for each translation phase:
- Parser Agent: Extract structured contract data
- Generator Agent: Create Solidity code
- Auditor Agent: Security analysis
- Refiner Agent: Fix security vulnerabilities (reinforcement loop)
- ABI Agent: Generate contract ABI
- MCP Agent: Generate MCP server code

The reinforcement logic is integrated directly into agent creation and the pipeline,
enabling automatic code refinement when security audits identify issues.
"""

import os
from typing import Dict, Any, Optional
from crewai import Agent, LLM as CrewLLM


# Default maximum refinement iterations for the reinforcement loop
DEFAULT_MAX_REFINEMENT_ITERATIONS = 2


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


def create_agents(crew_llm: CrewLLM, enable_reinforcement: bool = True) -> dict:
    """
    Create all specialized agents for the translation pipeline.
    
    Args:
        crew_llm: CrewAI LLM instance
        enable_reinforcement: If True, includes a Refiner Agent for the reinforcement loop
        
    Returns:
        Dictionary with agent instances for each phase, including refiner_agent if enabled
    """
    
    # Phase 2: Contract Parser Agent
    parser_agent = Agent(
        role="Contract Analysis Expert",
        goal=(
            "Extract every specific term, function name, variable name, state name, party role, "
            "financial amount, and obligation from the contract text exactly as written. "
            "Produce a fully-populated UniversalContractSchema JSON object with no generic placeholders "
            "and with obligations NEVER empty when functions or operations are described."
        ),
        backstory=(
            "You are an expert contract analyst who reads every sentence of a contract carefully. "
            "You extract EXACT terminology — if the contract says 'initializeLease' you write 'initializeLease', "
            "not 'initialize'. You map every described operation to an obligation with the correct authorized party. "
            "You never leave the obligations array empty when functions are described. "
            "You always produce valid JSON in the exact schema structure requested."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 3: Solidity Generator Agent
    generator_agent = Agent(
        role="Senior Solidity Smart Contract Engineer",
        goal=(
            "Implement the EXACT contract specification provided in the task. "
            "Read every MANDATORY requirement, every listed obligation, and every domain-specific rule, "
            "then implement each one completely with real on-chain logic. "
            "Produce a contract of 150-400 lines that fully and correctly satisfies the specification."
        ),
        backstory=(
            "You are a senior Solidity engineer with deep expertise in DeFi, tokens, governance, escrow, "
            "and marketplace contracts. You read every instruction in the task description carefully and "
            "implement every requirement with complete, production-quality code. "
            "You NEVER write empty functions, placeholder comments, or stub implementations. "
            "For every function you write, you ask: what real-world operation does this represent, "
            "what invariant must hold before and after, and what can go wrong? "
            "You enforce economic invariants (token supply conservation, escrow balance accounting), "
            "temporal logic (deadlines enforced with require(block.timestamp ...)), "
            "and access control (every sensitive function has a require()-backed modifier). "
            "You NEVER name a function parameter the same as a contract-level state variable "
            "(e.g. never use `owner` as a parameter if `address public owner` exists — use `tokenOwner` instead). "
            "You NEVER declare a public state variable with the same name as an interface function "
            "(e.g. never write `uint256 public totalSupply` when implementing IERC20 — use `uint256 private _totalSupply`). "
            "Your contracts are long, complete, and correct — a 300-line correct contract is "
            "far better to you than a 60-line stub."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 4: Security Auditor Agent
    auditor_agent = Agent(
        role="Blockchain Security Auditor",
        goal=(
            "Identify every exploitable vulnerability in the Solidity contract. "
            "For each issue, name the specific function affected and describe the exact exploit path. "
            "Provide severity_level, approved boolean, issues array, recommendations array with "
            "line-level fixes, vulnerability_count, and security_score in valid JSON."
        ),
        backstory=(
            "You are a blockchain security expert specializing in Solidity smart contract audits. "
            "You methodically check for reentrancy, access control gaps, integer overflow, "
            "timestamp manipulation, locked ether, unbounded loops, and input validation failures. "
            "Every issue you report names a specific function and explains how an attacker could exploit it. "
            "Every recommendation is a concrete code-level fix, not generic advice. "
            "You return only valid JSON — no markdown, no prose."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    # Phase 5: ABI Generator Agent
    abi_agent = Agent(
        role="Ethereum ABI Specialist",
        goal=(
            "Generate the complete, accurate ABI JSON array for the given Solidity contract. "
            "Include every public/external function with correct inputs, outputs, and stateMutability; "
            "every event with all parameters and indexed flags; and the constructor. "
            "Types must be exact Solidity types (uint256 not uint). Return ONLY the JSON array."
        ),
        backstory=(
            "You are an Ethereum developer who has spent years generating and validating ABI specifications. "
            "You know that 'uint' must be 'uint256', that view functions have no state mutations, "
            "that payable functions have stateMutability='payable', and that indexed event parameters "
            "must carry \"indexed\": true. You include every public/external function — never miss one. "
            "You preserve parameter names exactly. You return only the raw JSON array — no markdown fences, no prose."
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
    
    # Phase 7: Quality Evaluator Agent
    quality_evaluator_agent = Agent(
        role="Smart Contract Quality Analyst",
        goal=(
            "Score the generated Solidity contract across five metrics (functional completeness, "
            "variable fidelity, state machine correctness, business logic fidelity, code quality). "
            "Produce precise integer scores based on exact point calculations — never round to the nearest 5. "
            "Return only valid JSON with metric_1 through metric_5 objects and a composite_score."
        ),
        backstory=(
            "You are an expert smart contract quality analyst who evaluates generated Solidity code "
            "against natural language specifications. You read the specification line by line, "
            "then inspect the code and assign scores based on exact evidence — counting matched functions, "
            "checking that variables are written and read, verifying state transitions are reachable, "
            "and confirming economic invariants are enforced. "
            "Your scores are precise (73 not 75) because you show the arithmetic. "
            "You return only valid JSON — no markdown, no prose — with the exact keys required."
        ),
        llm=crew_llm,
        verbose=False,
        allow_delegation=False
    )
    
    agents = {
        'parser_agent': parser_agent,
        'generator_agent': generator_agent,
        'auditor_agent': auditor_agent,
        'abi_agent': abi_agent,
        'mcp_agent': mcp_agent,
        'quality_evaluator_agent': quality_evaluator_agent,
    }
    
    # Add Refiner Agent for reinforcement loop if enabled
    if enable_reinforcement:
        refiner_agent = Agent(
            role="Smart Contract Security Refiner",
            goal="Fix all identified security vulnerabilities in Solidity smart contracts",
            backstory=(
                "You are a Solidity security specialist who fixes smart contract vulnerabilities. "
                "Given a contract and a list of security issues from an audit, you rewrite the code "
                "to address every vulnerability while maintaining the original functionality. "
                "You follow the Checks-Effects-Interactions pattern, add reentrancy guards where needed, "
                "implement proper access control, validate all inputs with require(), "
                "and ensure no silent failures. You return ONLY the fixed Solidity code."\
            ),
            llm=crew_llm,
            verbose=False,
            allow_delegation=False
        )
        agents['refiner_agent'] = refiner_agent
    
    return agents


def should_refine(audit_report: Dict[str, Any], refinement_count: int, max_iterations: int = DEFAULT_MAX_REFINEMENT_ITERATIONS) -> bool:
    """
    Determine if the contract should go through refinement based on audit results.
    
    This is the decision function for the reinforcement loop. It checks:
    1. Whether there are remaining refinement iterations
    2. Whether the audit found issues requiring fixes
    
    Args:
        audit_report: The security audit report dictionary
        refinement_count: Current number of refinement iterations completed
        max_iterations: Maximum allowed refinement iterations
        
    Returns:
        True if refinement should be performed, False otherwise
    """
    if refinement_count >= max_iterations:
        print(f"🔄 Refinement check: Max iterations reached ({refinement_count}/{max_iterations})")
        return False
    
    severity = audit_report.get('severity_level', 'unknown').lower()
    approved = audit_report.get('approved', False)
    
    print(f"🔄 Refinement check: severity={severity}, approved={approved}, iteration={refinement_count}/{max_iterations}")
    
    # Refine if not approved and severity is medium or higher
    if not approved and severity in ['medium', 'high', 'critical']:
        print(f"✓ Triggering refinement loop (severity={severity}, approved={approved})")
        return True
    
    print(f"⏭️  Skipping refinement (severity={severity}, approved={approved})")
    return False


def create_refinement_task_description(solidity_code: str, audit_report: Dict[str, Any]) -> str:
    """
    Create task description for the Refiner Agent based on audit findings.
    
    Args:
        solidity_code: The current Solidity code that needs fixing
        audit_report: The security audit report with issues to fix
        
    Returns:
        Task description string for the refiner agent
    """
    issues = audit_report.get('issues', [])
    recommendations = audit_report.get('recommendations', [])
    severity = audit_report.get('severity_level', 'unknown')
    
    issues_text = "\n".join(f"  - {issue}" for issue in issues) if issues else "  - No specific issues listed"
    recommendations_text = "\n".join(f"  - {rec}" for rec in recommendations) if recommendations else "  - No specific recommendations"
    
    return f"""Fix ALL security vulnerabilities in this Solidity smart contract.

CURRENT CONTRACT CODE:
```solidity
{solidity_code}
```

SECURITY AUDIT FINDINGS (Severity: {severity.upper()}):
{issues_text}

REQUIRED FIXES:
{recommendations_text}

CRITICAL REQUIREMENTS:
1. Fix EVERY issue listed above - do not skip any vulnerability
2. Follow the Checks-Effects-Interactions pattern for all external calls
3. Add reentrancy guards (nonReentrant modifier) where needed
4. Ensure ALL state changes happen BEFORE external calls
5. Add proper access control (onlyOwner, role-based) on sensitive functions
6. Validate ALL inputs with require() statements - no silent failures
7. Check for zero addresses on address parameters
8. Ensure arithmetic operations are safe (Solidity ^0.8.0 has built-in overflow protection)
9. Preserve the original contract functionality while fixing security issues

Return ONLY the complete, fixed Solidity code with ALL vulnerabilities addressed.
Do not include explanations - just the corrected code."""


__all__ = [
    'create_agents',
    'should_refine',
    'create_refinement_task_description',
    '_convert_to_crew_llm',
    'DEFAULT_MAX_REFINEMENT_ITERATIONS'
]
