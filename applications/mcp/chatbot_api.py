"""
Chatbot API Server - Bridges demo.html with chatbot.py functionality

This provides a REST API for the demo.html to communicate with the actual chatbot
and MCP servers, allowing real contract function calls.
"""

import os
import asyncio
import json
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
from fastmcp import Client
import sys
import tempfile
import shutil
import importlib.util
from queue import Queue
import threading
import subprocess
import time

# Add contract-translator directory to path
contract_translator_path = Path(__file__).parent.parent / "contract-translator"
sys.path.insert(0, str(contract_translator_path))

from agentics import LLM, user_message, system_message

# Import ContractTranslator from agentic_implementation
try:
    from agentic_implementation import IBMAgenticContractTranslator
    ContractTranslator = IBMAgenticContractTranslator
except ImportError:
    # Fallback: try direct import
    import importlib.util
    spec = importlib.util.spec_from_file_location("agentic_implementation", contract_translator_path / "agentic_implementation.py")
    agentic_impl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agentic_impl)
    ContractTranslator = agentic_impl.IBMAgenticContractTranslator

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env")

llm = LLM(model="gpt-4o-mini")
app = Flask(__name__)
CORS(app)

# Global state
current_mcp_client = None
current_tools = []
current_contract_type = "sales"
current_mcp_process = None  # Track MCP server subprocess

# Store ongoing translation sessions for pause/resume
translation_sessions = {}


# ==================== SOLIDITY ERROR RECOVERY FUNCTIONS ====================

def _fix_empty_statements(solidity_code: str) -> str:
    """Remove incomplete statement fragments that cause syntax errors"""
    lines = solidity_code.split('\n')
    fixed_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip completely empty lines or lines with only whitespace
        if not stripped:
            fixed_lines.append('')
            continue
        
        # Skip lines that are just closing braces
        if stripped == '}':
            fixed_lines.append(line)
            continue
        
        # Skip lines that end with semicolon (complete statements)
        if stripped.endswith(';') or stripped.endswith('{'):
            fixed_lines.append(line)
            continue
        
        # Skip function declarations and control flow
        if any(keyword in stripped for keyword in ['function ', 'if (', 'for (', 'while (', 'else', 'event ', 'mapping', 'struct ', 'contract ']):
            fixed_lines.append(line)
            continue
        
        # Skip lines with common valid patterns
        if any(pattern in stripped for pattern in ['return ', 'require(', 'assert(', 'revert(', 'emit ', '=', 'public', 'private', 'internal', 'external']):
            fixed_lines.append(line)
            continue
        
        # Skip lines that look like valid statements
        if not any(char in stripped for char in ['(', ')', '[', ']']):
            # If it's just a word or simple identifier, likely incomplete
            if len(stripped.split()) <= 2 and not any(op in stripped for op in ['=', '>', '<', '+', '-', '*', '/']):
                continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def _fix_malformed_statements(solidity_code: str) -> str:
    """Fix missing semicolons, mismatched brackets, and malformed function calls"""
    import re
    
    lines = solidity_code.split('\n')
    fixed_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped or stripped.startswith('//'):
            fixed_lines.append(line)
            continue
        
        # Add missing semicolons to assignment and function call statements
        if stripped and not stripped.endswith((';', '{', '}', '(', ')', '/*', '*/')):
            # Check if it looks like a statement that needs a semicolon
            if any(kw in stripped for kw in ['return ', 'require(', 'assert(', 'emit ', 'revert(', '=']):
                # Make sure it's not a function declaration or control structure
                if not any(kw in stripped for kw in ['function ', 'if (', 'for (', 'while (', 'else if', 'contract ', 'event ']):
                    if not stripped.endswith(':'):
                        # Check if statement is complete (not missing closing parens)
                        if stripped.count('(') == stripped.count(')'):
                            line = line.rstrip() + ';'
        
        # Fix: Remove incomplete inline comments
        if ' //' in line:
            # Make sure comment doesn't cut off code
            comment_pos = line.find(' //')
            code_part = line[:comment_pos].strip()
            if code_part and not code_part.endswith((';', '{', '}')):
                if code_part.count('(') == code_part.count(')'):
                    line = line[:comment_pos].rstrip() + '; //' + line[comment_pos+3:]
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def _remove_problematic_modifiers(solidity_code: str) -> str:
    """Remove access modifiers and complex decorators that may cause issues"""
    import re
    
    # Remove problematic inline modifiers that aren't standard Solidity
    # Keep standard ones: public, private, internal, external, pure, view, payable, constant
    
    lines = solidity_code.split('\n')
    fixed_lines = []
    
    standard_modifiers = {'public', 'private', 'internal', 'external', 'pure', 'view', 'payable', 'constant', 'virtual', 'override', 'abstract'}
    
    for line in lines:
        # Skip comments
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            fixed_lines.append(line)
            continue
        
        # For lines with function declarations, clean up modifiers
        if 'function ' in line:
            # Split the line at function keyword
            before_func = line[:line.find('function')]
            func_part = line[line.find('function'):]
            
            # Try to preserve the line but remove non-standard modifiers
            # This is conservative - keep the line mostly as-is
            fixed_lines.append(line)
            continue
        
        # Remove lines that are just dangling modifiers
        stripped = line.strip()
        if stripped in standard_modifiers or (len(stripped.split()) == 1 and stripped not in standard_modifiers):
            if stripped and not any(kw in stripped for kw in ['return', 'require', 'assert', 'emit', 'revert']):
                # Check if this is a complete line (ends with { ; or })
                if not any(c in stripped for c in ['{', ';', '}']):
                    # Skip dangling single words that aren't keywords
                    if not any(kw in stripped for kw in ['contract', 'function', 'if', 'for', 'while']):
                        continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


# ==================== CONTRACT DEPLOYMENT SERVICE ====================

def deploy_contract_to_testnet(solidity_code: str, contract_name: str, private_key: str = None, schema: dict = None):
    """
    Deploy Solidity contract to testnet (Ganache local or Sepolia testnet)
    
    Args:
        solidity_code: The Solidity contract code
        contract_name: Name of the contract
        private_key: Optional private key for deployment
        schema: Optional contract schema (dict) for regeneration on error
    
    Returns: {
        'success': bool,
        'contract_address': str,
        'transaction_hash': str,
        'rpc_url': str,
        'network': str,
        'private_key': str (if generated)
    }
    """
    try:
        print(f"\n🚀 Deploying contract {contract_name} to testnet...")
        print(f"   Contract size: {len(solidity_code)} characters, {len(solidity_code.splitlines())} lines")
        print(f"   Schema available: {'✓ Yes' if schema and len(schema) > 0 else '❌ No'}")
        print(f"   Starting automatic deployment sequence...")
        
        # Try to use local Ganache first
        from web3 import Web3
        
        # Ganache RPC URL
        rpc_url = os.getenv("GANACHE_RPC_URL", "http://127.0.0.1:7545")
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            print(f"⚠️ Cannot connect to Ganache at {rpc_url}")
            print("ℹ️ Make sure Ganache is running: ganache-cli")
            raise Exception(f"Cannot connect to Ganache at {rpc_url}")
        
        print(f"✓ Connected to network: {rpc_url}")
        
        # Get or create account
        if private_key:
            from eth_account import Account
            account = Account.from_key(private_key)
            print(f"✓ Using provided account: {account.address}")
        else:
            # Get Ganache's first account (which has pre-funded ETH)
            # For Ganache, we can get all accounts directly
            accounts = web3.eth.accounts
            if not accounts:
                raise Exception("No Ethereum accounts available on Ganache")
            
            # Use the first available account (Ganache pre-funds these)
            account_address = accounts[0]
            print(f"✓ Using Ganache account: {account_address}")
            
            # For Ganache UI, we need to use eth_sign to avoid private key issues
            # Create a simple wrapper that uses web3 to sign
            class GanacheAccount:
                def __init__(self, address, web3_instance):
                    self.address = address
                    self.web3 = web3_instance
                
            account = GanacheAccount(account_address, web3)
            # We'll handle signing differently for Ganache accounts
            private_key = None  # Will use eth_sign instead


        
        # Compile Solidity code
        print("\n📝 Compilation Phase:")
        print("   Sanitizing and fixing Solidity code...")
        
        # Sanitize Solidity code - fix checksum issues in address literals
        # Replace address literals that look like examples with proper format
        import re
        sanitized_solidity = solidity_code
        
        # Fix: Remove event declarations inside functions (they must be at contract level)
        # Pattern: any "event" keyword inside function bodies and move them to contract level
        lines = sanitized_solidity.split('\n')
        fixed_lines = []
        events_found = []
        in_function = False
        function_indent = 0
        
        for line in lines:
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            
            # Track function context
            if stripped.startswith('function ') and '{' in line:
                in_function = True
                function_indent = current_indent
                fixed_lines.append(line)
            elif in_function and current_indent <= function_indent and stripped and not stripped.startswith('}'):
                # Exiting function
                in_function = False
                fixed_lines.append(line)
            elif in_function and stripped.startswith('event '):
                # Found event inside function - save it for later insertion at contract level
                events_found.append(line)
                print(f"   ✓ Found and relocating misplaced event declaration")
                continue
            else:
                fixed_lines.append(line)
        
        sanitized_solidity = '\n'.join(fixed_lines)
        
        # Insert events at contract level (after contract declaration, before functions)
        if events_found:
            # Find the first function and insert events before it
            contract_match = re.search(r'(contract\s+\w+.*?\{)', sanitized_solidity, re.DOTALL)
            if contract_match:
                insert_pos = contract_match.end()
                # Insert events after contract opening brace
                for event in events_found:
                    sanitized_solidity = sanitized_solidity[:insert_pos] + '\n    ' + event.strip() + sanitized_solidity[insert_pos:]
                    insert_pos += len(event) + 6
                print(f"   Inserted {len(events_found)} event(s) at contract level")
        
        # Fix: Multiline return statements - ensure they have matching parentheses and content
        # Pattern: fix return statements with mismatched arguments
        lines = sanitized_solidity.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            
            # Check if this is a return statement with opening paren
            if stripped.startswith('return ('):
                indent = len(line) - len(stripped)
                return_lines = [line]
                i += 1
                paren_count = 1  # Opening paren in 'return ('
                
                # Collect all lines until we find the matching closing paren
                while i < len(lines) and paren_count > 0:
                    next_line = lines[i]
                    return_lines.append(next_line)
                    # Count parens
                    paren_count += next_line.count('(') - next_line.count(')')
                    i += 1
                
                # Join the return statement
                return_text = '\n'.join(return_lines)
                
                # Simple fix: if it's malformed, just do a simple return
                if 'return (' in return_text and ')' in return_text:
                    # Try to extract what's being returned
                    match = re.search(r'return\s*\((.*?)\)', return_text, re.DOTALL)
                    if match:
                        return_val = match.group(1).strip()
                        if return_val:
                            # Fix the return to be single-line if possible
                            fixed_lines.append(' ' * indent + f'return ({return_val});')
                            print(f"   Fixed malformed return statement")
                        else:
                            # Empty return
                            fixed_lines.append(' ' * indent + 'return;')
                    else:
                        fixed_lines.extend(return_lines)
                else:
                    fixed_lines.extend(return_lines)
                continue
            
            fixed_lines.append(line)
            i += 1
        
        sanitized_solidity = '\n'.join(fixed_lines)
        
        # Find address patterns (40 hex chars after 0x) and convert to checksum format
        address_pattern = r'0x[0-9a-fA-F]{40}'
        addresses = re.findall(address_pattern, sanitized_solidity)
        
        if addresses:
            print(f"   Found {len(set(addresses))} address literal(s), fixing checksums...")
            from eth_account import Account
            for addr in set(addresses):
                try:
                    # Use eth_account to get checksummed address
                    checksummed = Account.from_key("0x" + "0" * 64).address  # Dummy to access method
                    from web3 import Web3
                    checksummed = Web3.to_checksum_address(addr)
                    if checksummed != addr:
                        sanitized_solidity = sanitized_solidity.replace(addr, checksummed)
                        print(f"     Fixed: {addr} → {checksummed}")
                except:
                    pass  # Keep original if conversion fails
        
        solidity_code = sanitized_solidity
        
        try:
            from solcx import compile_source, install_solc
            import solcx
        except ImportError:
            from py_solc_x import compile_source, install_solc
            import py_solc_x as solcx
        
        # Auto-install solc if not present
        solc_version = '0.8.0'
        
        # Try multiple times with progressive error fixing
        compilation_attempts = 0
        max_attempts = 3
        compiled_sol = None
        last_error = None
        
        while compilation_attempts < max_attempts and compiled_sol is None:
            compilation_attempts += 1
            try:
                if compilation_attempts == 1:
                    print("   ⏳ Attempting Solidity compilation (v0.8.0 with optimizations)...")
                else:
                    print(f"   ⏳ Compilation attempt {compilation_attempts}/{max_attempts}...")
                
                compiled_sol = compile_source(
                    solidity_code,
                    output_values=['abi', 'bin'],
                    solc_version=solc_version,
                    optimize=True,
                    optimize_runs=200
                )
                print("   ✓ Compilation successful!")
                break
                
            except Exception as e:
                last_error = str(e)
                
                if "has not been installed" in last_error:
                    print(f"⬇️ Installing solc {solc_version}...")
                    install_solc(solc_version)
                    continue
                
                elif "code size" in last_error.lower():
                    print(f"⚠️  Code too large even with optimization")
                    raise Exception("Contract bytecode exceeds size limits")
                
                # Syntax error - try to auto-fix
                print(f"   ⚠️  Syntax error detected, attempting auto-fix...")
                
                # Extract line number from error if possible
                line_match = re.search(r'<stdin>:(\d+):', last_error)
                if line_match:
                    error_line = int(line_match.group(1))
                    print(f"   📍 Error at line {error_line}")
                
                # Apply progressive fixes
                if compilation_attempts == 1:
                    # First fix attempt: Remove incomplete/empty lines
                    print(f"   🔧 Fix 1/3: Removing incomplete statement fragments...")
                    solidity_code = _fix_empty_statements(solidity_code)
                    
                elif compilation_attempts == 2:
                    # Second fix attempt: Fix missing semicolons and malformed statements
                    print(f"   🔧 Fix 2/3: Fixing missing semicolons and malformed statements...")
                    solidity_code = _fix_malformed_statements(solidity_code)
                    
                elif compilation_attempts == 3:
                    # Third fix attempt: Remove problematic modifiers and inline documentation
                    print(f"   🔧 Fix 3/3: Removing problematic modifiers...")
                    solidity_code = _remove_problematic_modifiers(solidity_code)
        
        if compiled_sol is None:
            # All compilation attempts failed - try LLM regeneration
            error_msg = last_error or "Unknown compilation error"
            print(f"\n   🔴 Compilation Analysis (after {max_attempts} fix attempts):")
            print(f"   ❌ The LLM-generated Solidity has persistent syntax errors.")
            
            # Save the problematic code to a debug file
            import time
            debug_filename = f"debug_solidity_{int(time.time())}.sol"
            debug_path = Path(__file__).parent.parent / "contract-translator" / "output" / debug_filename
            try:
                with open(debug_path, 'w') as f:
                    f.write("// SOLIDITY COMPILATION ERROR\n")
                    f.write(f"// Error: {error_msg}\n")
                    f.write(f"// This contract failed to compile after {max_attempts} fix attempts\n\n")
                    f.write(solidity_code)
                print(f"   📄 Saved debug Solidity to: {debug_path}")
            except:
                pass
            
            # Classify error
            if "Expected" in error_msg:
                print(f"   📌 Error Type: Syntax error (expected token)")
            elif "undeclared" in error_msg.lower():
                print(f"   📌 Error Type: Reference error (undeclared identifier)")
            elif "conflicts" in error_msg.lower():
                print(f"   📌 Error Type: Conflict error (duplicate declarations)")
            elif "is not" in error_msg.lower():
                print(f"   📌 Error Type: Type error (type mismatch)")
            else:
                print(f"   📌 Error Type: {error_msg[:80]}")
            
            # Try LLM regeneration if schema provided
            if schema and isinstance(schema, dict) and len(schema) > 0:
                print(f"\n   🔄 Attempting LLM regeneration with error feedback...")
                try:
                    # Build error context for LLM
                    contract_type = schema.get('contract_type', 'unknown')
                    parties = schema.get('parties', [])
                    financial_terms = schema.get('financial_terms', [])
                    
                    print(f"   📋 Contract type: {contract_type}")
                    print(f"   👥 Parties: {len(parties)}")
                    print(f"   💰 Financial terms: {len(financial_terms)}")
                    print(f"   📝 Requesting LLM regeneration with full error context...")
                    
                    # Create regeneration prompt for LLM
                    regen_messages = [
                        system_message(
                            f"""You are a Solidity expert fixing compilation errors in smart contracts.

The previous generation had a syntax error at line 102. MUST FIX:
1. Ensure EVERY statement ends with semicolon (;)
2. Match all parentheses, brackets, and braces
3. Complete all function bodies properly
4. No incomplete or dangling code
5. Only valid Solidity ^0.8.0 syntax

Error reported: {error_msg[:200]}

Generate a CORRECTED, COMPILABLE Solidity contract."""
                        ),
                        user_message(
                            f"""REGENERATE a corrected Solidity ^0.8.0 smart contract for: {contract_type}

Contract schema:
{json.dumps(schema, indent=2)[:1500]}

CRITICAL REQUIREMENTS:
1. Fix the compilation error: {error_msg[:150]}
2. Every statement MUST end with semicolon
3. All parentheses/brackets matched
4. No incomplete code
5. Defensive programming - handle missing data
6. Return sensible defaults for missing fields

Return ONLY valid, compilable Solidity code."""
                        )
                    ]
                    
                    regen_response = llm.chat(messages=regen_messages)
                    regenerated_solidity = str(regen_response).strip()
                    
                    # Remove markdown code fences if present
                    if "```solidity" in regenerated_solidity:
                        regenerated_solidity = regenerated_solidity.split("```solidity")[1].split("```")[0].strip()
                    elif "```" in regenerated_solidity:
                        regenerated_solidity = regenerated_solidity.split("```")[1].split("```")[0].strip()
                    
                    print(f"   ✅ LLM regenerated contract ({len(regenerated_solidity.splitlines())} lines)")
                    print(f"   ⏳ Retrying compilation with regenerated code...")
                    
                    # Try to compile the regenerated code (no more fixes, just compile)
                    try:
                        regenerated_compiled = compile_source(
                            regenerated_solidity,
                            output_values=['abi', 'bin'],
                            solc_version=solc_version,
                            optimize=True,
                            optimize_runs=200
                        )
                        print(f"   ✅ Regenerated contract compiled successfully!")
                        compiled_sol = regenerated_compiled
                        solidity_code = regenerated_solidity
                    except Exception as regen_error:
                        print(f"   ❌ Regenerated contract also failed to compile: {str(regen_error)[:100]}")
                        print(f"   Continuing with original error...")
                        raise Exception(f"Solidity compilation failed after {max_attempts} attempts and LLM regeneration: {error_msg[:200]}")
                
                except Exception as regen_ex:
                    print(f"   ⚠️  Regeneration failed: {str(regen_ex)[:100]}")
                    raise Exception(f"Solidity compilation failed after {max_attempts} attempts: {error_msg[:200]}")
            else:
                print(f"   ℹ️  Schema not provided, regeneration not possible")
                raise Exception(f"Solidity compilation failed after {max_attempts} attempts: {error_msg[:200]}")
        
        contract_id, contract_interface = compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        bytecode_size = len(bytecode) // 2  # Hex string is 2 chars per byte
        print(f"✓ Compiled successfully (bytecode size: {bytecode_size} bytes)")
        
        # Check if bytecode is too large
        if bytecode_size > 24576:  # 24KB limit
            print(f"⚠️  WARNING: Contract bytecode exceeds 24KB limit!")
            print(f"   Size: {bytecode_size} bytes (max: 24576)")
        
        # Create contract object
        contract = web3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Build transaction
        print("🔨 Building deployment transaction...")
        nonce = web3.eth.get_transaction_count(account.address)
        
        # Get gas price for EIP-1559 (London fork)
        # Ganache runs in EIP-1559 mode, so we need maxFeePerGas and maxPriorityFeePerGas
        try:
            # Try to get the latest block and base fee
            latest_block = web3.eth.get_block('latest')
            base_fee = latest_block.get('baseFeePerGas', 1)
            # Priority fee (tip) - set to 2x base fee or minimum
            max_priority_fee = max(base_fee * 2, web3.to_wei(2, 'gwei'))
            # Max fee = base fee + priority fee
            max_fee = base_fee + max_priority_fee
            
            print(f"   Base Fee: {base_fee / 1e9:.2f} gwei")
            print(f"   Max Priority Fee: {max_priority_fee / 1e9:.2f} gwei")
            print(f"   Max Fee: {max_fee / 1e9:.2f} gwei")
            
            use_eip1559 = True
        except Exception as e:
            print(f"   Warning: Could not get base fee, falling back to gasPrice: {e}")
            gas_price = web3.eth.gas_price
            use_eip1559 = False
        
        # Handle constructor arguments - extract from ABI and provide defaults if needed
        constructor_abi = next((item for item in abi if item.get('type') == 'constructor'), None)
        constructor_args = []
        
        if constructor_abi and constructor_abi.get('inputs'):
            print(f"   Constructor requires {len(constructor_abi['inputs'])} argument(s):")
            for input_item in constructor_abi['inputs']:
                arg_type = input_item.get('type', 'unknown')
                arg_name = input_item.get('name', 'arg')
                print(f"     - {arg_name}: {arg_type}")
                
                # Provide sensible defaults for common types
                # Check for array types first (e.g., address[], uint256[], string[])
                if arg_type.endswith('[]'):
                    base_type = arg_type[:-2]  # Remove '[]'
                    if 'address' in base_type:
                        constructor_args.append([account.address])
                        print(f"       → Using deployer address in array: [{account.address}]")
                    elif 'uint' in base_type:
                        constructor_args.append([0])
                        print(f"       → Using default uint array: [0]")
                    elif 'bool' in base_type:
                        constructor_args.append([False])
                        print(f"       → Using default bool array: [False]")
                    elif 'string' in base_type:
                        constructor_args.append([""])
                        print(f"       → Using default string array: ['']")
                    elif 'bytes' in base_type:
                        constructor_args.append([b''])
                        print(f"       → Using default bytes array: [b'']")
                    else:
                        constructor_args.append([])
                        print(f"       → Using empty array for unknown type")
                # Then check for scalar types
                elif 'address' in arg_type:
                    constructor_args.append(account.address)
                    print(f"       → Using deployer address: {account.address}")
                elif 'uint' in arg_type:
                    constructor_args.append(0)
                    print(f"       → Using default uint: 0")
                elif 'bool' in arg_type:
                    constructor_args.append(False)
                    print(f"       → Using default bool: False")
                elif 'string' in arg_type:
                    constructor_args.append("")
                    print(f"       → Using default string: ''")
                elif 'bytes' in arg_type:
                    constructor_args.append(b'')
                    print(f"       → Using default bytes: ''")
                else:
                    constructor_args.append(None)
                    print(f"       → Using default: None")
        
        # Build constructor with appropriate arguments
        tx_params = {
            'from': account.address,
            'nonce': nonce,
            'gas': 3000000,  # Increased for larger contracts (default 2M, max 3M)
        }
        
        # Add gas pricing parameters based on EIP-1559 support
        if use_eip1559:
            tx_params['maxFeePerGas'] = max_fee
            tx_params['maxPriorityFeePerGas'] = max_priority_fee
        else:
            tx_params['gasPrice'] = gas_price
        
        if constructor_args:
            tx_dict = contract.constructor(*constructor_args).build_transaction(tx_params)
        else:
            tx_dict = contract.constructor().build_transaction(tx_params)
        
        # Sign and send transaction
        print("✍️ Signing and sending transaction...")
        
        if private_key:
            # Use eth_account for signing with private key
            from eth_account import Account
            signed_txn = web3.eth.account.sign_transaction(tx_dict, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        else:
            # For Ganache accounts, use eth_sendTransaction (no signing needed)
            # Ganache handles signing automatically with pre-funded accounts
            print(f"   Using Ganache account (no private key needed)")
            tx_hash = web3.eth.send_transaction(tx_dict)
        
        print("⏳ Waiting for transaction receipt...")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        contract_address = tx_receipt.contractAddress
        print(f"✅ Contract deployed successfully!")
        print(f"   Address: {contract_address}")
        print(f"   Tx Hash: {tx_hash.hex()}")
        
        return {
            'success': True,
            'contract_address': contract_address,
            'transaction_hash': tx_hash.hex(),
            'rpc_url': rpc_url,
            'network': 'ganache-local',
            'private_key': private_key,
            'account_address': account.address
        }
        
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }


async def decide_tool_call(user_input: str, tools: list, contract_type: str) -> dict:
    """Use LLM to decide which tool to call based on user input."""
    import asyncio
    
    tool_descriptions = []
    for t in tools:
        if hasattr(t, 'name'):
            name = t.name
            desc = t.description if hasattr(t, 'description') else 'No description'
            input_schema = t.inputSchema if hasattr(t, 'inputSchema') else {}
        else:
            name = t.get('name', 'unknown')
            desc = t.get('description', 'No description')
            input_schema = t.get('inputSchema', {})
        
        tool_descriptions.append(f"- {name}: {desc}")
    
    tool_descriptions_str = "\n".join(tool_descriptions)
    
    messages = [
        system_message(
            f"""You are an AI assistant managing a {contract_type} smart contract.
            
Your job is to understand what the user wants and decide which contract tool to call.

Available tools:
{tool_descriptions_str}

When the user makes a request, respond with ONLY valid JSON (no explanations or markdown).
Format: {{"tool": "function_name", "args": {{"param1": value1, "param2": value2}}}}

Common requests:
- "What's the status?" → call a status/view function
- "Pay rent" → call payment functions
- "Check balance" → call balance checking functions
- "Get details" → call getter functions

Always use actual function names from the available tools.
If the user's request doesn't match any tool, respond with {{"tool": "none", "explanation": "I don't see a matching function for that request"}}"""
        ),
        user_message(
            f"""User request: "{user_input}"

Respond with ONLY the JSON, no extra text or markdown."""
        )
    ]
    
    try:
        # Wrap LLM call with timeout to prevent hanging
        def call_llm():
            return llm.chat(messages=messages)
        
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(None, call_llm),
            timeout=10.0  # 10 second timeout for LLM response
        )
        response_text = str(response).strip()
        
        # Remove markdown fences if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"⚠ LLM response parsing error: {response_text}")
            return {"error": f"Invalid response format: {response_text}", "exception": str(e)}
    
    except asyncio.TimeoutError:
        print("❌ LLM call timed out after 10 seconds")
        return {"error": "LLM request timed out", "tool": "none", "explanation": "The AI is taking too long to respond. Please try again."}
    except Exception as e:
        print(f"❌ Error in decide_tool_call: {str(e)}")
        return {"error": f"Failed to determine tool: {str(e)}", "tool": "none"}


def wait_for_approval(session_id: str, timeout: int = 600):
    """Wait for user approval before continuing translation"""
    import time
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if session_id in translation_sessions:
            session = translation_sessions[session_id]
            if 'user_approval' in session:
                approval = session['user_approval']
                del session['user_approval']  # Clear the approval flag
                return approval
        time.sleep(0.5)
    
    return False  # Timeout


@app.route('/api/translate-stream', methods=['POST'])
def translate_stream():
    """Stream real-time updates during 6-phase translation pipeline using Server-Sent Events"""
    import uuid
    
    try:
        # Get the uploaded PDF file
        if 'file' not in request.files:
            print("❌ No file in request")
            return Response(f"data: {json.dumps({'error': 'No file provided', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        file = request.files['file']
        if file.filename == '':
            print("❌ Empty filename")
            return Response(f"data: {json.dumps({'error': 'No file selected', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        if not file.filename.lower().endswith('.pdf'):
            print(f"❌ Invalid file type: {file.filename}")
            return Response(f"data: {json.dumps({'error': 'Only PDF files are supported', 'phase': 0})}\n\n", mimetype='text/event-stream'), 400
        
        print(f"📄 Processing file: {file.filename}")
        
        # Create a session ID for this translation
        session_id = str(uuid.uuid4())
        translation_sessions[session_id] = {'temp_path': None}
        print(f"📋 Created session: {session_id}")
        
        # Save to temporary location
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            file.save(tmp_file.name)
            temp_pdf_path = tmp_file.name
            translation_sessions[session_id]['temp_path'] = temp_pdf_path
            print(f"✓ Saved to temp: {temp_pdf_path}")
        
        def generate():
            """Generator for Server-Sent Events"""
            try:
                # Initialize the real translator
                print("🚀 Initializing ContractTranslator...")
                translator = ContractTranslator()
                print("✓ Translator initialized")
                
                # Run the streaming 6-phase pipeline
                print("📋 Starting 6-phase translation pipeline...")
                
                # Set output directory to contract-translator/output
                output_directory = str(contract_translator_path / "output")
                
                for phase_update in translator.translate_contract_streaming(
                    input_path=temp_pdf_path,
                    output_dir=output_directory,
                    require_audit_approval=False,
                    generate_mcp_server=True
                ):
                    # Send each phase update as an SSE event
                    print(f"📡 Streaming phase {phase_update['phase']}...")
                    
                    # For Phase 4 (security audit), pause and wait for approval
                    if phase_update['phase'] == 4 and phase_update['status'] == 'needs_approval':
                        print(f"⏸️  Waiting for user approval on Phase 4...")
                        # Include session_id in the event so frontend knows which session to approve
                        phase_update['session_id'] = session_id
                        yield f"data: {json.dumps(phase_update)}\n\n"
                        
                        # Wait for user approval
                        approval = wait_for_approval(session_id, timeout=600)
                        print(f"✓ User approval received: {approval}")
                        
                        if not approval:
                            print("❌ User rejected the audit or approval timed out")
                            error_event = {"error": "Security audit rejected or approval timed out", "phase": 0}
                            yield f"data: {json.dumps(error_event)}\n\n"
                            return
                        else:
                            # Continue to next phase
                            continue
                    
                    yield f"data: {json.dumps(phase_update)}\n\n"
                
                print("✓ Translation streaming completed")
                
            except Exception as e:
                print(f"❌ Translation error: {str(e)}")
                import traceback
                traceback.print_exc()
                error_event = {"error": str(e), "phase": 0}
                yield f"data: {json.dumps(error_event)}\n\n"
            
            finally:
                # Clean up temp file
                if session_id in translation_sessions and translation_sessions[session_id]['temp_path']:
                    temp_path = translation_sessions[session_id]['temp_path']
                    if Path(temp_path).exists():
                        try:
                            os.unlink(temp_path)
                            print(f"✓ Cleaned up temp file")
                        except:
                            pass
                # Clean up session
                if session_id in translation_sessions:
                    del translation_sessions[session_id]
        
        return Response(generate(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        })
    
    except Exception as e:
        print(f"❌ API error: {str(e)}")
        import traceback
        traceback.print_exc()
        error_event = {"error": str(e), "phase": 0}
        return Response(f"data: {json.dumps(error_event)}\n\n", mimetype='text/event-stream'), 500


def add_debug_output_to_mcp_server(mcp_server_path: Path) -> bool:
    """Inject comprehensive debug logging into MCP server tool functions
    
    NOTE: This function is DEPRECATED. The MCP server is now generated with
    debug output going to stderr from the start. This function is a no-op.
    """
    # No longer needed - debug output is generated correctly from _generate_mcp_server_code
    return True


def fix_mcp_server_for_ganache(mcp_server_path: Path, contract_name: str):
    """
    Fix MCP server generated code to work with Ganache and correct ABI filename
    
    Fixes:
    1. Replace hardcoded Solidity contract name with correct ABI filename
    2. Replace private key signing with Ganache native account sending
    3. Replace account.address references with account_address
    """
    try:
        with open(mcp_server_path, 'r') as f:
            content = f.read()
        
        # Fix ABI path: Find any .abi.json reference and replace with contract_name.abi.json
        import re
        # Match patterns like: 'ContractName.abi.json' or "ContractName.abi.json"
        abi_pattern = r"['\"][\w]+\.abi\.json['\"]"
        content = re.sub(abi_pattern, f"'{contract_name}.abi.json'", content)
        
        # Fix account initialization for Ganache:
        # Remove: account = web3.eth.account.from_key(PRIVATE_KEY)
        # Replace with: account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
        
        content = content.replace(
            "account = web3.eth.account.from_key(PRIVATE_KEY)",
            "account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))"
        )
        
        # Replace account.address with account_address (it's now a string, not an Account object)
        content = content.replace(
            "web3.eth.get_transaction_count(account.address)",
            "web3.eth.get_transaction_count(account_address)"
        )
        
        # Replace transaction signing pattern for non-payable functions
        # Old: account.address in 'from'
        # New: account_address
        content = content.replace(
            "'from': account.address,",
            "'from': account_address,"
        )
        
        # Replace manual signing + raw transaction sending with eth_sendTransaction
        # Pattern: signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        #         tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # With:    tx_hash = web3.eth.send_transaction(txn)
        
        signing_pattern = r"signed_txn = web3\.eth\.account\.sign_transaction\(txn, private_key=PRIVATE_KEY\)\s+tx_hash = web3\.eth\.send_raw_transaction\(signed_txn\.rawTransaction\)"
        content = re.sub(
            signing_pattern,
            "tx_hash = web3.eth.send_transaction(txn)",
            content,
            flags=re.DOTALL
        )
        
        # Write back
        with open(mcp_server_path, 'w') as f:
            f.write(content)
        
        print(f"✓ MCP server fixed for Ganache: {mcp_server_path}")
        return True
    except Exception as e:
        print(f"⚠ Warning: Could not fix MCP server: {str(e)}")
        return False


@app.route('/api/audit-approval', methods=['POST'])
def audit_approval():
    """Handle user approval/rejection of security audit"""
    data = request.json
    session_id = data.get('session_id')
    approved = data.get('approved', False)
    
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    
    if session_id not in translation_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    # Store the approval and resume the stream
    translation_sessions[session_id]['user_approval'] = approved
    print(f"📝 User approval: {approved} (Session: {session_id})")
    
    return jsonify({"success": True, "message": f"Audit {'approved' if approved else 'rejected'}"})


def _generate_mcp_server_code(contract_name: str, abi: list) -> str:
    """Generate MCP server code from contract ABI with proper error handling"""
    
    # Filter functions from ABI
    functions = [item for item in abi if item.get('type') == 'function']
    
    # Build tool functions
    tool_functions = []
    
    for func in functions:
        func_name = func.get('name', 'unknown')
        inputs = func.get('inputs', [])
        state_mutability = func.get('stateMutability', 'view')
        
        # Build parameter list
        params = ', '.join([f'{inp.get("name", "param")}' for inp in inputs])
        
        # Build parameter documentation
        param_docs = '\n        '.join([
            f'Args:',
            *[f'  {inp.get("name", "param")}: {inp.get("type", "unknown")}' 
              for inp in inputs]
        ]) if inputs else 'Returns: Contract data'
        
        # Determine if function writes to blockchain
        is_write = state_mutability in ['nonpayable', 'payable']
        
        if is_write:
            # Write function
            tool_code = f'''@mcp.tool()
async def {func_name}({params}):
    """Call {func_name} on the contract.
    
    {param_docs}
    """
    try:
        sys.stderr.write(f"[MCP] Calling {func_name}\\n")
        sys.stderr.flush()
        
        # Get nonce with timeout
        try:
            nonce = web3.eth.get_transaction_count(account_address, timeout=5)
        except Exception as e:
            return {{"error": f"Failed to get nonce: {{str(e)}}"}}
        
        # Build transaction with timeout
        try:
            txn = contract.functions.{func_name}({params}).build_transaction({{
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.eth.gas_price
            }})
        except Exception as e:
            return {{"error": f"Failed to build transaction: {{str(e)}}"}}
        
        # Send transaction
        try:
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Transaction sent: {{tx_hash.hex()}}\\n")
            sys.stderr.flush()
            return {{"tx_hash": tx_hash.hex()}}
        except Exception as e:
            return {{"error": f"Transaction failed: {{str(e)}}"}}
            
    except Exception as e:
        sys.stderr.write(f"[MCP] ERROR: {{str(e)}}\\n")
        sys.stderr.flush()
        return {{"error": str(e)}}
'''
        else:
            # Read function - make it async
            tool_code = f'''@mcp.tool()
async def {func_name}({params}):
    """Get {func_name} from the contract.
    
    {param_docs}
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function {func_name}\\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.{func_name}({params}).call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {{result}}\\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {{"result": result}}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {{error_msg}}\\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {{"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}}
            elif "invalid opcode" in error_msg.lower():
                return {{"error": "Invalid contract bytecode. The contract may not be deployed correctly."}}
            elif "timeout" in error_msg.lower():
                return {{"error": "RPC timeout. Check your Ganache connection."}}
            else:
                return {{"error": f"Contract call failed: {{error_msg}}"}}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {{error_msg}}\\n")
        sys.stderr.flush()
        return {{"error": error_msg}}
'''
        
        tool_functions.append(tool_code)
    
    # Build complete server code with connection validation
    server_code = f'''#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

sys.stderr.write("[MCP] Starting server initialization...\\n")
sys.stderr.flush()

try:
    from web3 import Web3
    from dotenv import load_dotenv
    from fastmcp import FastMCP
    sys.stderr.write("[MCP] Imports successful\\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] Import error: {{e}}\\n")
    sys.stderr.flush()
    sys.exit(1)

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
sys.stderr.write(f"[MCP] Loading env from: {{env_path}}\\n")
sys.stderr.flush()
load_dotenv(dotenv_path=env_path)

# Load ABI
abi_path = Path(__file__).parent / '{contract_name}.abi.json'
sys.stderr.write(f"[MCP] Loading ABI from: {{abi_path}}\\n")
sys.stderr.flush()
try:
    with open(abi_path, 'r') as f:
        contract_abi = json.load(f)
    sys.stderr.write(f"[MCP] ABI loaded ({{len(contract_abi)}} items)\\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] ABI load error: {{e}}\\n")
    sys.stderr.flush()
    sys.exit(1)

# Get environment variables
RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')

sys.stderr.write(f"[MCP] RPC_URL: {{RPC_URL}}\\n")
sys.stderr.flush()
sys.stderr.write(f"[MCP] CONTRACT_ADDRESS: {{CONTRACT_ADDRESS}}\\n")
sys.stderr.flush()
sys.stderr.write(f"[MCP] ACCOUNT_ADDRESS: {{ACCOUNT_ADDRESS}}\\n")
sys.stderr.flush()

# Initialize Web3 with timeout
try:
    web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={{'timeout': 10}}))
    
    # Test connection immediately
    if not web3.is_connected():
        sys.stderr.write(f"[MCP] ERROR: Cannot connect to RPC at {{RPC_URL}}\\n")
        sys.stderr.flush()
        sys.exit(1)
    
    sys.stderr.write(f"[MCP] Web3 connected successfully\\n")
    sys.stderr.flush()
    
    # Test if we can get latest block (verifies RPC is working)
    try:
        latest_block = web3.eth.block_number
        sys.stderr.write(f"[MCP] Latest block: {{latest_block}}\\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[MCP] WARNING: Cannot get latest block: {{e}}\\n")
        sys.stderr.flush()
    
except Exception as e:
    sys.stderr.write(f"[MCP] Web3 connection error: {{e}}\\n")
    sys.stderr.flush()
    sys.exit(1)

# Set up account and contract
try:
    account_address = Web3.to_checksum_address(ACCOUNT_ADDRESS)
    contract_address_checksum = Web3.to_checksum_address(CONTRACT_ADDRESS)
    
    # Verify contract exists
    try:
        code = web3.eth.get_code(contract_address_checksum)
        if code == b'' or code == '0x':
            sys.stderr.write(f"[MCP] ERROR: No contract code at address {{contract_address_checksum}}\\n")
            sys.stderr.flush()
            sys.exit(1)
        sys.stderr.write(f"[MCP] Contract code verified ({{len(code)}} bytes)\\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[MCP] ERROR checking contract code: {{e}}\\n")
        sys.stderr.flush()
        sys.exit(1)
    
    contract = web3.eth.contract(address=contract_address_checksum, abi=contract_abi)
    sys.stderr.write(f"[MCP] Contract initialized successfully\\n")
    sys.stderr.flush()
    
except Exception as e:
    sys.stderr.write(f"[MCP] Contract setup error: {{e}}\\n")
    sys.stderr.flush()
    sys.exit(1)

# Create FastMCP instance
mcp = FastMCP("{contract_name}")
sys.stderr.write("[MCP] FastMCP instance created\\n")
sys.stderr.flush()

# Log registered tools
sys.stderr.write("[MCP] Attempting to list registered tools...\\n")
sys.stderr.flush()
try:
    import inspect
    tool_count = 0
    for name, obj in inspect.getmembers(mcp):
        if name.startswith('_'):
            continue
        if callable(obj):
            tool_count += 1
    sys.stderr.write(f"[MCP] MCP has {{tool_count}} callable members\\n")
    sys.stderr.flush()
    
    # Try to get registered tools from FastMCP's internal registry
    if hasattr(mcp, '_tools'):
        sys.stderr.write(f"[MCP] Internal _tools attribute: {{mcp._tools}}\\n")
        sys.stderr.flush()
    
    if hasattr(mcp, 'tools'):
        sys.stderr.write(f"[MCP] Tools property: {{mcp.tools}}\\n")
        sys.stderr.flush()
        
except Exception as e:
    sys.stderr.write(f"[MCP] Could not inspect tools: {{e}}\\n")
    sys.stderr.flush()

''' + '\n'.join(tool_functions) + '''

if __name__ == "__main__":
    sys.stderr.write("[MCP] Starting mcp.run()...\\n")
    sys.stderr.flush()
    
    try:
        mcp.run()
    except Exception as e:
        sys.stderr.write(f"[MCP] Runtime error: {{e}}\\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
'''
    
    return server_code


@app.route('/api/auto-deploy', methods=['POST'])
def auto_deploy():
    """Automatically deploy contract to testnet and setup MCP server"""
    data = request.json
    solidity_code = data.get('solidity')
    contract_name = data.get('contract_name', 'GeneratedContract')
    schema = data.get('schema', {})
    abi = data.get('abi', [])
    
    # Log schema reception
    print(f"\n📋 Schema reception check:")
    print(f"   Type: {type(schema).__name__}")
    print(f"   Size: {len(str(schema))} chars")
    if isinstance(schema, dict):
        print(f"   Keys: {list(schema.keys())[:5]}")
        print(f"   Contract type: {schema.get('contract_type', 'N/A')}")
        print(f"   Parties: {len(schema.get('parties', []))}")
        print(f"   Financial terms: {len(schema.get('financial_terms', []))}")
    
    if not solidity_code:
        return jsonify({"error": "No Solidity code provided"}), 400
    
    try:
        print("\n" + "="*70)
        print("🚀 AUTOMATIC DEPLOYMENT INITIATED")
        print("="*70)
        
        # Deploy contract - pass schema for regeneration on error
        deployment_result = deploy_contract_to_testnet(solidity_code, contract_name, schema=schema)
        
        if not deployment_result['success']:
            return jsonify(deployment_result), 500
        
        contract_address = deployment_result['contract_address']
        private_key = deployment_result['private_key']
        rpc_url = deployment_result['rpc_url']
        account_address = deployment_result['account_address']
        
        print(f"\n💾 Setting up environment configuration...")
        
        # Create .env for MCP server
        mcp_output_dir = Path(__file__).parent.parent / "contract-translator" / "output"
        mcp_output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create unique contract directory
        contract_dir_name = f"{contract_name}_{deployment_result['transaction_hash'][:8]}"
        contract_dir = mcp_output_dir / contract_dir_name
        contract_dir.mkdir(exist_ok=True, parents=True)
        
        # Write .env file for MCP - only include private_key if it exists
        env_lines = [
            "# Auto-Generated MCP Server Configuration",
            f"# Contract: {contract_name}",
            f"# Deployed at: {deployment_result['transaction_hash']}",
            "",
            f"RPC_URL={rpc_url}",
            f"CONTRACT_ADDRESS={contract_address}",
            f"ACCOUNT_ADDRESS={account_address}"
        ]
        
        # Only add private key if it's not None
        if private_key:
            env_lines.insert(5, f"PRIVATE_KEY={private_key}")
        
        env_content = "\n".join(env_lines)
        
        env_file = contract_dir / ".env"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✓ Environment file created: {env_file}")
        
        # Save ABI
        abi_file = contract_dir / f"{contract_name}.abi.json"
        with open(abi_file, 'w') as f:
            json.dump(abi, f, indent=2)
        print(f"✓ ABI saved: {abi_file}")
        
        # Save Solidity
        sol_file = contract_dir / f"{contract_name}.sol"
        with open(sol_file, 'w') as f:
            f.write(solidity_code)
        print(f"✓ Solidity saved: {sol_file}")
        
        # Generate MCP server from the ABI (fresh, not copied from old deployment)
        mcp_server_path = None
        
        print(f"\n💾 Generating MCP server from ABI...")
        print(f"   Contract: {contract_name}")
        print(f"   ABI functions: {len(abi)}")
        
        try:
            # Create the MCP server code that works with THIS contract
            mcp_code = _generate_mcp_server_code(contract_name, abi)
            
            if mcp_code:
                mcp_server_path = contract_dir / f"{contract_name}_mcp_server.py"
                with open(mcp_server_path, 'w', encoding='utf-8') as f:
                    f.write(mcp_code)
                print(f"   ✓ MCP server generated: {mcp_server_path.name}")
                
                # Fix the MCP server for Ganache compatibility
                fix_mcp_server_for_ganache(mcp_server_path, contract_name)
                print(f"   ✓ Fixed for Ganache")
                
                # Add comprehensive debug output
                add_debug_output_to_mcp_server(mcp_server_path)
                print(f"   ✓ Added debug output")
            else:
                print(f"   ⚠️  MCP server generation returned empty code")
        except Exception as e:
            print(f"   Error generating MCP server: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print(f"\n✅ Deployment Complete!")
        print(f"   Contract Address: {contract_address}")
        print(f"   RPC URL: {rpc_url}")
        print(f"   Account: {account_address}")
        if mcp_server_path:
            print(f"   MCP Server: {mcp_server_path}")
        
        response_data = {
            'success': True,
            'contract_address': contract_address,
            'private_key': private_key,
            'rpc_url': rpc_url,
            'account_address': account_address,
            'transaction_hash': deployment_result['transaction_hash'],
            'env_file': str(env_file),
            'abi_file': str(abi_file),
            'sol_file': str(sol_file),
            'message': 'Contract deployed successfully'
        }
        
        if mcp_server_path:
            response_data['mcp_server_path'] = str(mcp_server_path)
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Auto-deployment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/api/translate', methods=['POST'])
def translate_contract_endpoint():
    """Legacy endpoint - redirects to stream"""
    return translate_stream()


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "mcp_connected": current_mcp_client is not None})


@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to verify API is working"""
    return jsonify({
        "status": "ok",
        "message": "API is working correctly",
        "openai_key": "✓ Set" if OPENAI_API_KEY else "❌ Not set",
        "translator_importable": True
    })


@app.route('/api/connect', methods=['POST'])
def connect_mcp():
    """Connect to MCP server"""
    global current_mcp_client, current_tools, current_contract_type
    
    data = request.json
    mcp_path = data.get('mcp_path')
    contract_type = data.get('contract_type', 'sales')
    
    # If already connected, return current connection
    if current_mcp_client:
        tool_names = []
        for t in current_tools:
            if hasattr(t, 'name'):
                tool_names.append(t.name)
            else:
                tool_names.append(t.get('name', 'unknown'))
        
        return jsonify({
            "status": "already_connected",
            "tools": tool_names,
            "count": len(current_tools)
        })
    
    if not mcp_path:
        return jsonify({"error": "No mcp_path provided"}), 400
    
    try:
        # Convert env file path to MCP server script path if needed
        mcp_file = Path(mcp_path)
        if mcp_file.name == ".env":
            # Look for MCP server in the same directory
            parent_dir = mcp_file.parent
            mcp_scripts = list(parent_dir.glob("*_mcp_server.py"))
            if mcp_scripts:
                mcp_file = mcp_scripts[0]
            else:
                # MCP server not found
                current_contract_type = contract_type
                return jsonify({
                    "status": "deployed_only",
                    "tools": [],
                    "count": 0,
                    "message": "Contract deployed. MCP server script not found for interactive mode."
                })
        
        if not mcp_file.exists():
            return jsonify({"error": f"MCP server not found: {mcp_file}"}), 404
        
        print(f"📡 Launching MCP server: {mcp_file}")
        
        global current_mcp_process
        
        # Kill any existing process
        if current_mcp_process:
            try:
                current_mcp_process.terminate()
                current_mcp_process.wait(timeout=2)
            except:
                current_mcp_process.kill()
        
        # Launch MCP server as subprocess
        try:
            # Use python to run the MCP server script
            python_exe = sys.executable
            current_mcp_process = subprocess.Popen(
                [python_exe, str(mcp_file)],
                cwd=str(mcp_file.parent),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
            
            print(f"   Process started (PID: {current_mcp_process.pid})")
            
            # Start a thread to capture MCP server output
            def capture_mcp_output():
                try:
                    print(f"   📺 MCP Server Output Stream:")
                    print(f"   " + "="*60)
                    if current_mcp_process.stdout:
                        for line in iter(current_mcp_process.stdout.readline, ''):
                            if line:
                                print(f"   [MCP] {line.rstrip()}")
                except Exception as e:
                    print(f"   ⚠️  Error reading MCP output: {str(e)}")
            
            import threading
            mcp_output_thread = threading.Thread(target=capture_mcp_output, daemon=True)
            mcp_output_thread.start()
            
            # Wait for server to start
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Failed to launch MCP server: {str(e)}")
            return jsonify({"error": f"Failed to launch MCP server: {str(e)}"}), 500
        
        # Now try to connect
        try:
            print(f"📡 Connecting to MCP server...")
            
            # Create event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def connect():
                # Give server more time to initialize with retries
                for attempt in range(5):
                    try:
                        print(f"   Connection attempt {attempt + 1}/5...")
                        print(f"   Creating Client with: {str(mcp_file)}")
                        client = Client(str(mcp_file))
                        print(f"   Client created, entering context...")
                        await client.__aenter__()
                        print(f"   Context entered, listing tools...")
                        tools = await client.list_tools()
                        print(f"   Tools listed successfully: {len(tools)} tools")
                        return client, tools
                    except Exception as e:
                        print(f"   Attempt {attempt + 1} failed: {type(e).__name__}: {str(e)}")
                        if attempt < 4:
                            print(f"   Waiting 1 second before retry...")
                            await asyncio.sleep(1)
                        else:
                            raise
            
            current_mcp_client, current_tools = loop.run_until_complete(connect())
            current_contract_type = contract_type
            
            tool_names = []
            for t in current_tools:
                if hasattr(t, 'name'):
                    tool_names.append(t.name)
                else:
                    tool_names.append(t.get('name', 'unknown'))
            
            print(f"✅ Connected! Found {len(tool_names)} tools: {tool_names}")
            
            return jsonify({
                "status": "connected",
                "tools": tool_names,
                "count": len(current_tools)
            })
            
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Kill the process if connection failed
            if current_mcp_process:
                try:
                    current_mcp_process.terminate()
                except:
                    pass
            return jsonify({"error": f"Connection failed: {str(e)}"}), 500
    
    except Exception as e:
        print(f"❌ Outer error in connect: {str(e)}")
        import traceback
        traceback.print_exc()
        # Kill the process if anything failed
        if current_mcp_process:
            try:
                current_mcp_process.terminate()
            except:
                pass
        return jsonify({"error": f"Connection setup failed: {str(e)}"}), 500


def _sync_decide_tool_call(user_input: str, tools: list, contract_type: str) -> dict:
    """Synchronous version of tool selection using LLM"""
    import json
    
    tool_descriptions = []
    for t in tools:
        if hasattr(t, 'name'):
            name = t.name
            desc = t.description if hasattr(t, 'description') else 'No description'
        else:
            name = t.get('name', 'unknown')
            desc = t.get('description', 'No description')
        
        tool_descriptions.append(f"- {name}: {desc}")
    
    tool_descriptions_str = "\n".join(tool_descriptions)
    
    messages = [
        system_message(
            f"""You are an AI assistant managing a {contract_type} smart contract.

Your job is to understand what the user wants and decide which contract tool to call.

Available tools:
{tool_descriptions_str}

When the user makes a request, respond with ONLY valid JSON (no explanations or markdown).
Format: {{"tool": "function_name", "args": {{"param1": value1, "param2": value2}}}}

If the user's request doesn't match any tool, respond with {{"tool": "none", "explanation": "I don't see a matching function for that request"}}"""
        ),
        user_message(
            f"""User request: "{user_input}"

Respond with ONLY the JSON, no extra text."""
        )
    ]
    
    try:
        print("   Calling LLM to decide tool...")
        response = llm.chat(messages=messages, timeout=10)  # 10 second timeout
        response_text = str(response).strip()
        print(f"   LLM response: {response_text[:100]}...")
        
        # Remove markdown fences if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"   ⚠️  Failed to parse LLM response as JSON: {response_text}")
            return {"tool": "none", "explanation": f"Could not parse response: {response_text}"}
    
    except Exception as e:
        print(f"   ❌ LLM error: {str(e)}")
        return {"error": f"LLM failed: {str(e)}", "tool": "none"}


def _sync_call_mcp_tool(tool_name: str, args: dict) -> str:
    """Call an MCP tool synchronously with enhanced debugging"""
    global current_mcp_client, current_mcp_process
    
    if not current_mcp_client:
        raise Exception("MCP client not connected")
    
    print(f"   📞 Calling tool: {tool_name}")
    print(f"   Arguments: {args}")
    if current_mcp_process:
        print(f"   MCP Process ID: {current_mcp_process.pid}")
        print(f"   Process Status: {'Running' if current_mcp_process.poll() is None else 'Terminated'}")
    
    # Call tool with extended timeout
    import time
    start = time.time()
    
    try:
        # Create a coroutine for the tool call
        coro = current_mcp_client.call_tool(tool_name, args)
        
        # Run it in a new event loop (since we're in sync context)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            print(f"   ⏳ Waiting for MCP server response (timeout: 30s)...")
            # Increase timeout to 30 seconds for MCP tool execution
            result = loop.run_until_complete(asyncio.wait_for(coro, timeout=30.0))
            elapsed = time.time() - start
            print(f"   ✅ Tool returned successfully in {elapsed:.2f}s")
            
            # Format the result for display
            if isinstance(result, dict):
                result_str = json.dumps(result, indent=2)
            elif isinstance(result, str):
                result_str = result
            else:
                result_str = str(result)
            
            print(f"   Result preview: {result_str[:200]}...")
            return result_str
        finally:
            loop.close()
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"   ⏱️  Tool execution timed out after {elapsed:.2f}s")
        
        # Check if MCP process is still alive
        if current_mcp_process:
            poll_result = current_mcp_process.poll()
            if poll_result is not None:
                print(f"   ⚠️  MCP process has terminated with code: {poll_result}")
            else:
                print(f"   ⚠️  MCP process still running but tool is not responding")
        
        error_msg = f"Tool execution timed out after {elapsed:.2f}s. The MCP server may be unresponsive, the smart contract interaction may be failing silently, or there may be an issue with the generated MCP server code."
        print(f"   ❌ {error_msg}")
        raise Exception(error_msg)
    except Exception as e:
        elapsed = time.time() - start
        error_msg = f"Tool execution failed after {elapsed:.2f}s: {type(e).__name__}: {str(e)}"
        print(f"   ❌ {error_msg}")
        print(f"   \n   DEBUG INFO:")
        print(f"      - Tool: {tool_name}")
        print(f"      - Args: {args}")
        if current_mcp_process:
            print(f"      - MCP Process running: {current_mcp_process.poll() is None}")
        import traceback
        print(f"      - Traceback: {traceback.format_exc()}")
        raise


@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message and call MCP tools"""
    global current_mcp_client, current_tools, current_contract_type
    
    print("\n" + "="*70)
    print("📨 /api/chat POST request received")
    print("="*70)
    
    data = request.json
    print(f"Request data: {data}")
    
    if not data:
        print("❌ No JSON data in request")
        return jsonify({"error": "No data provided"}), 400
    
    user_input = data.get('message', '').strip()
    print(f"User message: '{user_input}'")
    
    if not user_input:
        print("❌ Empty message received")
        return jsonify({"error": "Empty message"}), 400
    
    # If MCP client not connected, provide helpful response
    if not current_mcp_client:
        print("⚠️  MCP client not connected")
        return jsonify({
            "user_input": user_input,
            "response": "⚠️ MCP server not connected. The smart contract has been deployed, but the interactive tools aren't available yet. You can still view the contract details from the deployment section.",
            "success": False,
            "tool_called": None,
            "mcp_status": "disconnected"
        }), 200
    
    try:
        print("📡 Deciding which tool to call...")
        
        # Use synchronous version of tool selection
        decision = _sync_decide_tool_call(user_input, current_tools, current_contract_type)
        print(f"Decision: {decision}")
        
        if "error" in decision or decision.get("tool") == "none":
            response_text = decision.get("explanation", decision.get("error", "Could not process request"))
            print(f"✓ No matching tool found: {response_text}")
            return jsonify({
                "user_input": user_input,
                "response": response_text,
                "success": False,
                "tool_called": None
            }), 200
        
        tool_name = decision.get("tool")
        args = decision.get("args", {})
        print(f"📞 Calling tool: {tool_name} with args: {args}")
        
        # Call the tool synchronously
        try:
            result = _sync_call_mcp_tool(tool_name, args)
            print(f"✓ Tool result: {result}")
            return jsonify({
                "user_input": user_input,
                "tool_called": tool_name,
                "arguments": args,
                "response": str(result),
                "success": True
            }), 200
        except Exception as e:
            error_msg = f"Error calling tool {tool_name}: {str(e)}"
            print(f"❌ {error_msg}")
            return jsonify({
                "user_input": user_input,
                "tool_called": tool_name,
                "arguments": args,
                "response": error_msg,
                "success": False
            }), 200
    
    except Exception as e:
        error_msg = f"Chat processing error: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": error_msg,
            "user_input": user_input
        }), 500


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Get list of available tools"""
    if not current_mcp_client:
        return jsonify({"tools": [], "error": "Not connected"}), 400
    
    tool_info = []
    for t in current_tools:
        if hasattr(t, 'name'):
            name = t.name
            desc = t.description if hasattr(t, 'description') else ''
        else:
            name = t.get('name', 'unknown')
            desc = t.get('description', '')
        
        tool_info.append({"name": name, "description": desc})
    
    return jsonify({"tools": tool_info})


if __name__ == '__main__':
    import threading
    import time
    from werkzeug.serving import run_simple
    
    print("Starting Chatbot API Server...")
    print("Available endpoints:")
    print("  GET  /api/health          - Health check")
    print("  GET  /api/test            - Test endpoint")
    print("  POST /api/translate       - Translate contract PDF")
    print("  POST /api/connect         - Connect to MCP server")
    print("  POST /api/chat            - Send chat message")
    print("  GET  /api/tools           - List available tools")
    print("\nServer running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Set Flask to log output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    
    # Run server with logging enabled (blocking, so logs show)
    try:
        app.run(debug=False, port=5000, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        exit(0)
