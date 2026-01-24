"""
Task description builders for CrewAI agents

These functions create detailed task descriptions for each phase:
- Parser: Extract structured data from contract text
- Generator: Create Solidity smart contract
- Auditor: Security analysis
- ABI Generator: Generate contract ABI
"""

from .schemas import UniversalContractSchema


def create_parser_task_description(contract_text: str) -> str:
    """
    Create task description for the Contract Parser Agent.
    Returns the full task description including the contract text.
    Uses the comprehensive prompt from programs.py for maximum accuracy.
    """
    return f"""Analyze this contract and extract ALL SPECIFIC information exactly as mentioned.

CONTRACT TEXT:
{contract_text}

CRITICAL INSTRUCTIONS:
1. Extract the EXACT function names mentioned in the contract (e.g., "initializeLease", "payRent", "confirmDelivery")
2. Extract the EXACT variable names mentioned (e.g., "monthlyRent", "securityDeposit", "deliveryDate")
3. Extract the EXACT state names mentioned (e.g., "Pending", "Active", "Completed", "Terminated")
4. Extract the EXACT party roles as described in the contract
5. DO NOT use generic placeholders - use the specific terminology from the contract
6. Capture ALL conditions, transitions, and logic flows mentioned

Your goal: Create a structured representation that preserves ALL specific details from the contract text.

PAY CLOSE ATTENTION TO:
1. **Specific Function Names**: If the contract says "The main functions include [initializeLease(), payRent(), terminateLease()]", extract EXACTLY those names
2. **Specific Variable Names**: If it mentions "monthlyRent", "securityDeposit", "leaseStartDate", extract those EXACT names
3. **Specific States**: If it mentions states like "Initializing", "Active", "Processing", "Terminated", extract those EXACT state names
4. **State Transitions**: Capture the EXACT transition logic (e.g., "Initializing → Active when lease starts")
5. **Specific Conditions**: Extract the EXACT conditions mentioned (e.g., "rent must be paid by day 5 of each month")
6. **Specific Events**: If events are mentioned like "LeaseInitialized", "RentPaid", extract those EXACT names

Return ONLY valid JSON with this structure:
{{
    "contract_type": "rental|employment|sales|service|loan|nda|partnership|investment|other",
    "title": "specific contract title from text",
    "parties": [
        {{
            "name": "EXACT party name from contract",
            "role": "EXACT role as described (not generic)",
            "address": "blockchain address if mentioned",
            "email": "if mentioned",
            "entity_type": "individual|company|organization"
        }}
    ],
    "financial_terms": [
        {{
            "amount": number,
            "currency": "ETH|USD|etc",
            "purpose": "EXACT purpose from contract (not 'payment' but 'monthly rent' or 'security deposit')",
            "frequency": "EXACT frequency from contract",
            "due_date": "EXACT due date or day of month"
        }}
    ],
    "dates": [
        {{
            "date_type": "EXACT date type from contract (leaseStartDate, deliveryDeadline, etc)",
            "value": "date string if provided",
            "day_of_month": number or null,
            "frequency": "if recurring"
        }}
    ],
    "assets": [
        {{
            "type": "SPECIFIC asset type from contract",
            "description": "EXACT description from contract",
            "location": "if mentioned",
            "quantity": number or null,
            "value": number or null
        }}
    ],
    "obligations": [
        {{
            "party": "EXACT party name",
            "description": "EXACT obligation as written",
            "deadline": "EXACT deadline if mentioned",
            "penalty_for_breach": "EXACT penalty if mentioned"
        }}
    ],
    "special_terms": ["EXACT special conditions word-for-word"],
    "conditions": {{
        "function_names": ["EXACT function names from contract: initializeLease, payRent, etc"],
        "variable_names": ["EXACT variable names: monthlyRent, securityDeposit, tenantAddress, etc"],
        "state_names": ["EXACT state names: Pending, Active, Completed, Terminated, etc"],
        "state_transitions": ["EXACT transitions: Pending->Active when X, Active->Completed when Y"],
        "events": ["EXACT event names: LeaseInitialized, RentPaid, LeaseTerminated, etc"],
        "logic_conditions": ["EXACT conditions: rent due on day 5, penalty if late > 7 days, etc"]
    }},
    "termination_conditions": ["EXACT termination conditions from contract"]
}}

EXTRACT EVERYTHING SPECIFIC - DO NOT USE GENERIC NAMES OR PLACEHOLDERS."""


def create_solidity_generator_task_description(schema: UniversalContractSchema) -> str:
    """
    Create task description for the Solidity Generator Agent.
    Uses the comprehensive prompt from programs.py with 10-point rules,
    forbidden patterns, and complete code examples.
    """
    conditions = schema.conditions if schema.conditions else {}
    function_names = conditions.get('function_names', [])
    variable_names = conditions.get('variable_names', [])
    state_names = conditions.get('state_names', [])
    state_transitions = conditions.get('state_transitions', [])
    events = conditions.get('events', [])
    logic_conditions = conditions.get('logic_conditions', [])
    
    return f"""Generate a COMPLETE, FUNCTIONAL Solidity ^0.8.0 smart contract that FULLY implements this specification.

CRITICAL GENERATION RULES - STRICT COMPLIANCE REQUIRED:

1. SEMANTIC FIDELITY OVER NAME MATCHING
   - Never generate functions without FULL implementation
   - No placeholder logic, no "// logic goes here" comments
   - Every function mentioned must have complete, executable behavior

2. EXPLICIT STATE MACHINE ENFORCEMENT
   - All states must be reachable and mutually exclusive
   - State transitions use require() with clear error messages
   - Never allow invalid state transitions
   - Every state-dependent function must enforce valid state with require()

3. ACCESS CONTROL MUST BE ENFORCED
   - All administrative functions use modifiers (onlyOwner, onlyRole, etc)
   - No state-changing function callable by arbitrary addresses unless specified
   - Define and use access roles consistently

4. NO SILENT FAILURES - PROHIBITED PATTERN
   - NEVER use: if (condition) return;
   - ALWAYS use: require(condition, "Error message");
   - All invalid conditions MUST revert with descriptive messages

5. ECONOMIC LOGIC MUST BE COMPLETE
   - If pricing/fees/swaps/payments mentioned: implement ALL calculations
   - Funds MUST be transferred or accounted for
   - Variables like price, feeRate, amountRaised MUST be read and written in live logic
   - No passive declarations - every financial variable must affect behavior

6. TIME-BASED CONDITIONS MUST BE ENFORCED
   - If deadlines/start times/durations mentioned: store AND check using block.timestamp
   - Time variables MUST affect contract behavior
   - Implement automatic state transitions based on time

7. EVENT SEMANTICS MUST MATCH ACTIONS
   - Events represent real, completed actions only
   - Each state change or economic transfer emits separate, specific event
   - Never merge unrelated actions into single event (e.g., no "TransferAndApproval")
   - Event names must be clear: Transfer, Approval, Swap, Paused, etc

8. NO UNUSED OR DECORATIVE CODE
   - Every variable, state, function, event MUST be actively used
   - If something cannot be implemented: either infer reasonable behavior or omit it
   - No "filler" code

9. STANDARD SOLIDITY SAFETY - MANDATORY
   - Use require() for all validation
   - Validate zero addresses
   - Ensure invariants (e.g., total supply consistency)
   - Use SafeMath patterns where needed

10. INTERNAL COHERENCE REQUIRED
    - Names must reflect actual behavior
    - States correspond to real operational modes
    - Functions must not contradict each other
    - Variables must not represent multiple concepts

FORBIDDEN PATTERNS:
- Empty function bodies
- Unused state variables
- Silent failures (if/return pattern)
- Placeholder comments
- Decorative events that don't represent real actions
- State variables that are never read
- Time variables that are never checked
- Access-controlled functions without modifiers

YOUR GOAL: Generate production-ready, complete, semantically accurate Solidity code.

CONTRACT ANALYSIS:
{schema.model_dump_json(indent=2)}

SPECIFIC REQUIREMENTS TO IMPLEMENT:

**EXACT Function Names to Implement (WITH FULL LOGIC):**
{chr(10).join(f"- {fn} (must be fully functional, not a stub)" for fn in function_names) if function_names else "- Extract function names from the obligations and implement them completely"}

**EXACT Variable Names to Use (MUST BE ACTIVELY USED IN LOGIC):**
{chr(10).join(f"- {vn} (must be read/written in functions, not decorative)" for vn in variable_names) if variable_names else "- Extract variable names from financial terms and dates"}

**EXACT State Names (MUST ALL BE REACHABLE WITH TRANSITIONS):**
{chr(10).join(f"- {sn} (implement transition logic TO and FROM this state)" for sn in state_names) if state_names else "- Determine if contract needs states based on transitions"}

**EXACT State Transitions (IMPLEMENT WITH require() CHECKS):**
{chr(10).join(f"- {st} (use require() to enforce this transition)" for st in state_transitions) if state_transitions else "- Implement any state changes mentioned in obligations"}

**EXACT Event Names (EMIT ON REAL ACTIONS ONLY):**
{chr(10).join(f"- {ev} (emit when the actual action completes)" for ev in events) if events else "- Create events based on function names (e.g., FunctionNameExecuted)"}

**EXACT Logic Conditions (IMPLEMENT WITH require() AND CALCULATIONS):**
{chr(10).join(f"- {lc} (enforce this condition in code)" for lc in logic_conditions) if logic_conditions else "- Implement conditions from obligations and special_terms"}

PARTIES TO HANDLE:
{chr(10).join(f"- {p.name} ({p.role}) - store as state variable with proper type" for p in schema.parties)}

FINANCIAL TERMS TO IMPLEMENT COMPLETELY:
{chr(10).join(f"- {t.purpose}: {t.amount} {t.currency} ({t.frequency if t.frequency else 'one-time'}) - implement full payment/transfer logic" for t in schema.financial_terms)}

OBLIGATIONS TO IMPLEMENT AS COMPLETE FUNCTIONS:
{chr(10).join(f"- {o.party} must: {o.description} (deadline: {o.deadline if o.deadline else 'none'}) - implement full logic with checks" for o in schema.obligations)}

MANDATORY IMPLEMENTATION CHECKLIST:
□ All functions have COMPLETE implementation (no "// TODO" or empty bodies)
□ All financial variables (price, fee, amount) are USED in calculations
□ All time variables (deadline, startTime) are CHECKED with block.timestamp
□ All state transitions use require() to prevent invalid changes
□ All administrative functions have access control modifiers
□ All economic transfers actually move funds (msg.value, transfer calls)
□ All events are emitted when their corresponding action completes
□ No silent failures - all invalid conditions revert with require()
□ All declared variables are read or written in at least one function
□ State machine is complete - all states are reachable and have transitions

STRUCTURE YOUR CONTRACT:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract [ContractName] {{
    // === STATE ENUM (if states mentioned) ===
    enum State {{ {', '.join(state_names) if state_names else 'Active, Completed, Terminated'} }}
    State public currentState;
    
    // === ACCESS CONTROL ===
    address public owner;
    // Add role-based addresses for each party
    
    modifier onlyOwner() {{
        require(msg.sender == owner, "Not authorized");
        _;
    }}
    
    modifier inState(State _state) {{
        require(currentState == _state, "Invalid state for this action");
        _;
    }}
    
    // === STATE VARIABLES (using EXACT names) ===
    // Declare all variables mentioned in contract
    // CRITICAL: Every variable MUST be used in at least one function
    
    // === EVENTS (using EXACT names, separate events for different actions) ===
    // One event per action type, never merge unrelated actions
    
    // === CONSTRUCTOR ===
    constructor(...) {{
        owner = msg.sender;
        // Initialize all state variables
        // Set initial state
        currentState = State.[InitialState];
    }}
    
    // === MAIN FUNCTIONS (using EXACT names with FULL implementation) ===
    // Implement complete logic for each function:
    // - Access control (modifiers)
    // - State checks (require currentState)
    // - Validation (require conditions)
    // - State updates
    // - Fund transfers (if applicable)
    // - Event emissions
    // - State transitions (if applicable)
    
    // === VIEW FUNCTIONS (getters for all state variables) ===
    // Provide read access to all state
    
    // === INTERNAL HELPER FUNCTIONS (if needed) ===
    // Extract complex logic into private functions
}}
```

EXAMPLE OF COMPLETE vs INCOMPLETE:

❌ INCOMPLETE (forbidden):
```solidity
function swapTokensForEth(uint256 amount) external {{
    require(swappingEnabled, "Swap disabled");
    // Logic goes here
}}
```

✅ COMPLETE (required):
```solidity
function swapTokensForEth(uint256 amount) external {{
    require(swappingEnabled, "Swap disabled");
    require(balances[msg.sender] >= amount, "Insufficient balance");
    require(address(this).balance >= amount * ethPrice, "Insufficient ETH");
    
    balances[msg.sender] -= amount;
    totalSupply -= amount;
    
    uint256 ethAmount = amount * ethPrice;
    (bool success, ) = msg.sender.call{{value: ethAmount}}("");
    require(success, "ETH transfer failed");
    
    emit TokensSwapped(msg.sender, amount, ethAmount);
}}
```

Return ONLY complete, production-ready Solidity code with ALL logic fully implemented."""


def create_audit_task_description(solidity_code: str) -> str:
    """
    Create task description for the Security Auditor Agent.
    """
    return f"""Perform a comprehensive security audit on this Solidity smart contract:

{solidity_code}

SYSTEMATIC AUDIT CHECKLIST - Check each category:

1. **REENTRANCY ATTACKS**: 
   - Look for external calls (call, transfer, send, delegatecall) followed by state changes
   - Check if state is updated BEFORE external calls (Checks-Effects-Interactions pattern)
   - Verify reentrancy guards (nonReentrant modifier) on sensitive functions

2. **ACCESS CONTROL**:
   - Verify onlyOwner or role-based modifiers on critical functions (withdraw, changeOwner, etc.)
   - Check if constructor properly initializes owner
   - Look for functions that should be internal/private but are public/external

3. **ARITHMETIC SAFETY**:
   - Check for unchecked arithmetic that could overflow/underflow
   - Verify SafeMath usage or Solidity ^0.8.0 built-in checks
   - Look for division by zero possibilities

4. **ETHER HANDLING**:
   - Check payable functions have proper access control
   - Verify withdraw/transfer functions validate amounts and recipients
   - Look for locked ether (payable functions with no withdrawal mechanism)

5. **DOS VULNERABILITIES**:
   - Look for unbounded loops that could hit gas limits
   - Check for external calls in loops
   - Verify functions can't be blocked by reverting recipients

6. **INPUT VALIDATION**:
   - Check require() statements validate all critical parameters
   - Verify address parameters check for address(0)
   - Ensure amount checks prevent zero or negative values

7. **TIMESTAMP DEPENDENCE**:
   - Check if block.timestamp is used for critical logic
   - Verify it's not used for randomness or precise timing

8. **EXTERNAL CALL SAFETY**:
   - Verify return values of external calls are checked
   - Check low-level calls (call, delegatecall) have proper error handling

Return ONLY valid JSON with specific findings:
{{
    "severity_level": "none|low|medium|high|critical",
    "approved": boolean (true if severity is none/low, false for medium/high/critical),
    "issues": [
        "SPECIFIC issue with line reference and exploit scenario",
        "Example: HIGH: Reentrancy in withdraw() - external call before balance update allows recursive calls"
    ],
    "recommendations": [
        "SPECIFIC remediation step, not generic advice",
        "Example: Move 'balances[msg.sender] = 0' BEFORE 'msg.sender.call{{value: amount}}()'"
    ],
    "vulnerability_count": number (total count of issues found),
    "security_score": "A|B|C|D|F" (A = no issues, B = only low, C = medium, D = high, F = critical)
}}

Be specific about WHERE issues are and HOW to fix them. Reference actual function names and variables from the code."""


def create_abi_generator_task_description(solidity_code: str) -> str:
    """
    Create task description for the ABI Generator Agent.
    """
    return f"""Generate the complete, accurate ABI (Application Binary Interface) for this Solidity contract:

{solidity_code}

REQUIREMENTS - Extract ALL of these:

1. **CONSTRUCTOR**: 
   - Include ALL constructor parameters with exact types (address, uint256, string, etc.)
   - stateMutability should be "nonpayable" unless constructor is payable
   - type: "constructor"

2. **ALL PUBLIC/EXTERNAL FUNCTIONS**:
   - Extract function name exactly as written
   - Include ALL parameters with correct types and names
   - Include ALL outputs with correct types
   - Set stateMutability: "pure" (no state read/write), "view" (reads state), "payable" (accepts ETH), or "nonpayable" (default)
   - type: "function"

3. **ALL EVENTS**:
   - Extract event name exactly as written
   - Include ALL parameters with correct types and names
   - Mark indexed parameters with "indexed": true
   - type: "event"

4. **TYPE ACCURACY**:
   - Use exact Solidity types: uint256 (not uint), address, bool, string, bytes, bytes32, etc.
   - For arrays: uint256[], address[], etc.
   - For mappings in public vars: treat as getter function
   - For enums: use uint8
   - For structs: expand to individual fields if returned

5. **PARAMETER NAMES**:
   - Preserve parameter names from code (critical for debugging)
   - Use empty string "" only if parameter has no name in code

VALIDATION:
- Every public/external function must be included
- Every event must be included
- Constructor must be included if it exists
- Types must match Solidity declarations EXACTLY
- Output must be valid JSON array

Return ONLY the JSON array (no markdown, no explanation):
[
  {{
    "type": "constructor",
    "stateMutability": "nonpayable",
    "inputs": [...]
  }},
  {{
    "type": "function",
    "name": "functionName",
    "stateMutability": "view|pure|payable|nonpayable",
    "inputs": [...],
    "outputs": [...]
  }},
  {{
    "type": "event",
    "name": "EventName",
    "inputs": [
      {{"name": "param", "type": "uint256", "indexed": true}}
    ]
  }}
]"""


def create_mcp_task_description(abi, schema, contract_name: str) -> str:
    """
    Create task description for the MCP Server Generator Agent.
    Uses the comprehensive prompt from programs.py.
    """
    # Extract function information from ABI
    functions = [item for item in abi if item.get('type') == 'function']
    payable_functions = [f for f in functions if f.get('stateMutability') == 'payable']
    nonpayable_functions = [f for f in functions if f.get('stateMutability') == 'nonpayable']
    view_functions = [f for f in functions if f.get('stateMutability') in ['view', 'pure']]
    
    import json
    
    return f"""Generate a complete MCP server for this {schema.contract_type} smart contract.

CONTRACT NAME: {contract_name}
CONTRACT TYPE: {schema.contract_type}
PARTIES: {[f"{p.name} ({p.role})" for p in schema.parties]}

ABI SUMMARY:
- Payable functions: {len(payable_functions)}
- Non-payable functions: {len(nonpayable_functions)}
- View functions: {len(view_functions)}

COMPLETE ABI:
{json.dumps(abi, indent=2)}

Generate a Python MCP server file with CORRECT FastMCP API:

1. **Imports (MUST use FastMCP, not old MCP)**:
   ```python
   import os
   import json
   from pathlib import Path
   from web3 import Web3
   from dotenv import load_dotenv
   from fastmcp import FastMCP
   ```

2. **Setup (Load .env from SAME DIRECTORY as script, Load ABI from .abi.json file)**:
   ```python
   import os
   import json
   from pathlib import Path
   from dotenv import load_dotenv
   
   # Load .env from the same directory as this script
   env_path = Path(__file__).parent / '.env'
   load_dotenv(dotenv_path=env_path)
   
   # Load ABI from the same directory as this script
   abi_path = Path(__file__).parent / '{contract_name}.abi.json'
   with open(abi_path, 'r') as f:
       contract_abi = json.load(f)
   
   RPC_URL = os.getenv('RPC_URL')
   PRIVATE_KEY = os.getenv('PRIVATE_KEY')
   CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
   
   web3 = Web3(Web3.HTTPProvider(RPC_URL))
   account = web3.eth.account.from_key(PRIVATE_KEY)
   contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
   ```

3. **Create FastMCP instance**:
   ```python
   mcp = FastMCP("{contract_name}")
   ```

4. **Create @mcp.tool() decorated functions for EACH ABI function**:
   
   For PAYABLE functions:
   - Build transaction with correct value
   - Sign and send transaction
   - Return {{"tx_hash": hash}}
   
   For NON-PAYABLE functions:
   - Build transaction (no value)
   - Sign and send transaction
   - Return {{"tx_hash": hash}}
   
   For VIEW functions:
   - Call function (read-only)
   - Return result directly
   
5. **Documentation**:
   - Each @mcp.tool() function must have docstring
   - Explain what it does, who can call it, parameters, return value
   - Handle errors gracefully

6. **Error Handling**:
   - Wrap each tool in try/except
   - Return {{"error": str(e)}} on failure

7. **Main Block (CRITICAL)**:
   ```python
   if __name__ == "__main__":
       mcp.run()
   ```

CRITICAL CODE EXAMPLES:

Setup must use local .env file:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
```

Transaction building for non-payable:
```python
txn = contract.functions.function_name(param1).buildTransaction({{
    'from': account.address,
    'nonce': web3.eth.get_transaction_count(account.address),
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei')
}})
signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
return {{"tx_hash": tx_hash.hex()}}
```

Transaction building for payable:
```python
txn = contract.functions.makePayment().buildTransaction({{
    'from': account.address,
    'nonce': web3.eth.get_transaction_count(account.address),
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'value': web3.to_wei(5, 'ether')
}})
signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
return {{"tx_hash": tx_hash.hex()}}
```

View function:
```python
result = contract.functions.getBalance().call()
return {{"result": result}}
```

IMPORTANT RULES:
- Function names must match ABI exactly
- Include ALL functions from ABI
- Use @mcp.tool() decorator (not @tool())
- Load ABI from {contract_name}.abi.json file in same directory (do NOT hardcode ABI)
- Load .env from same directory as script
- ALWAYS initialize: account = web3.eth.account.from_key(PRIVATE_KEY)
- Use 'from': account.address in all transactions
- Use web3.eth.get_transaction_count(), NOT web3.eth.getTransactionCount()
- Use web3.to_wei(), NOT web3.toWei()
- Use web3.eth.send_raw_transaction(), NOT web3.eth.sendRawTransaction()
- Use Web3.to_checksum_address(), NOT Web3.toChecksumAddress()
- For payable functions, include 'value': web3.to_wei(amount, 'ether')
- File must be self-contained and runnable

Return ONLY the complete Python code, no explanations."""
