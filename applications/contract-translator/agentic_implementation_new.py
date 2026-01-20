"""
IBM Agentics Contract Translator - Main Entry Point

This file maintains backward compatibility by re-exporting all components from the core package.

Modular structure:
- core/schemas.py: Pydantic data models
- core/programs.py: Legacy Program classes
- core/task_builders.py: Task description generators
- core/agents.py: Agent creation functions
- core/translator.py: Main translator orchestration

Usage:
    from agentic_implementation import IBMAgenticContractTranslator
    
    translator = IBMAgenticContractTranslator(model="gpt-4o-mini")
    results = translator.translate_contract("contract.pdf")
"""

import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Re-export all core components for backward compatibility
from .core.schemas import (
    PartyRole,
    ContractType,
    ContractParty,
    FinancialTerm,
    ContractDate,
    ContractObligation,
    ContractAsset,
    UniversalContractSchema,
)

from .core.programs import (
    UniversalContractParserProgram,
    UniversalSolidityGeneratorProgram,
    SecurityAuditorProgram,
    ABIGeneratorProgram,
    MCPServerGeneratorProgram,
)

from .core.task_builders import (
    create_parser_task_description,
    create_solidity_generator_task_description,
    create_audit_task_description,
    create_abi_generator_task_description,
)

from .core.agents import (
    create_agents,
    _convert_to_crew_llm,
)

from .core.translator import IBMAgenticContractTranslator

# Main CLI function
def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
Usage: python agentic_implementation.py <contract_file> [output_dir] [--no-mcp]

Arguments:
  contract_file    Path to contract (PDF or text file)
  output_dir       Output directory (default: ./output)
  --no-mcp         Skip MCP server generation

Example:
  python agentic_implementation.py my_contract.pdf ./output
        """)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = "./output"
    generate_mcp = True
    
    # Parse arguments
    for arg in sys.argv[2:]:
        if arg == "--no-mcp":
            generate_mcp = False
        elif not arg.startswith("--"):
            output_dir = arg
    
    try:
        translator = IBMAgenticContractTranslator(model="gpt-4o-mini")
        
        print(f"\n📄 Translating: {input_file}")
        print(f"📁 Output: {output_dir}")
        print(f"🔧 MCP Server: {'Yes' if generate_mcp else 'No'}\n")
        
        results = translator.translate_contract(
            input_path=input_file,
            output_dir=output_dir,
            generate_mcp_server=generate_mcp,
            use_agentic_pipeline=True  # Use new Agent/Task approach by default
        )
        
        print(f"\n✅ Translation complete!")
        print(f"📊 Generated files in: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__ = [
    # Schemas
    'PartyRole',
    'ContractType',
    'ContractParty',
    'FinancialTerm',
    'ContractDate',
    'ContractObligation',
    'ContractAsset',
    'UniversalContractSchema',
    # Programs
    'UniversalContractParserProgram',
    'UniversalSolidityGeneratorProgram',
    'SecurityAuditorProgram',
    'ABIGeneratorProgram',
    'MCPServerGeneratorProgram',
    # Task Builders
    'create_parser_task_description',
    'create_solidity_generator_task_description',
    'create_audit_task_description',
    'create_abi_generator_task_description',
    # Agents
    'create_agents',
    '_convert_to_crew_llm',
    # Main Translator
    'IBMAgenticContractTranslator',
]
