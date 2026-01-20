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
    """
    return f"""Analyze this contract and extract ALL SPECIFIC information exactly as mentioned.

CONTRACT TEXT:
{contract_text}

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
    Extracts specific requirements from the schema.
    """
    conditions = schema.conditions if schema.conditions else {}
    function_names = conditions.get('function_names', [])
    variable_names = conditions.get('variable_names', [])
    state_names = conditions.get('state_names', [])
    state_transitions = conditions.get('state_transitions', [])
    events = conditions.get('events', [])
    logic_conditions = conditions.get('logic_conditions', [])
    
    return f"""Generate a COMPLETE, FUNCTIONAL Solidity ^0.8.0 smart contract that FULLY implements this specification.

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
