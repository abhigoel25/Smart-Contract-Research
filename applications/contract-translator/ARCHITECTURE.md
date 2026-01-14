# Smart Contract Generation Pipeline Architecture

## 📐 System Architecture Overview

> **Note**: This architecture focuses on the 6-phase semantic translation pipeline for research and quality evaluation of AI-generated smart contracts. Automatic deployment features have been removed to focus on contract generation quality assessment.

```
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER INTERFACE                          │
│                      (demo.html - React)                        │
│                                                                  │
│  ┌──────────────────┐  ┌───────────────┐  ┌──────────────────┐│
│  │ Phase 0          │  │ Phases 1-6    │  │ Output Files     ││
│  │ Selection        │→ │ Visualization │→ │ & Downloads      ││
│  │                  │  │               │  │                  ││
│  │ • Contract Type  │  │ • Progress    │  │ • Solidity Code  ││
│  │ • Start Button   │  │ • Code Preview│  │ • ABI JSON       ││
│  │                  │  │ • Downloads   │  │ • Security Audit ││
│  └──────────────────┘  └───────────────┘  └──────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                             ↓
                    (downloads files for analysis)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│               LOCAL FILESYSTEM                                   │
│               (Generated Outputs for Research)                   │
│                                                                  │
│  Output Folder:                                                 │
│  ├── sales_contract.sol          ← Solidity source             │
│  ├── sales_contract.abi.json     ← Function interface          │
│  ├── security_audit.json         ← Security analysis           │
│  ├── contract_schema.json        ← Parsed contract data        │
│  └── sales_mcp_server.py         ← MCP server template         │
│                                                                  │
│  Purpose: Research & Quality Evaluation                         │
│  • Analyze code quality                                         │
│  • Compare across contract types                                │
│  • Evaluate semantic accuracy                                   │
│  • Assess security patterns                                     │
└─────────────────────────────────────────────────────────────────┘

---

## 🔄 Complete Workflow with Detailed Steps

### Phase 0: Selection
```
User selects contract type (e.g., Sales Agreement)
         ↓
React state updates: contractType = 'sales'
         ↓
UI displays selection with visual indicator
         ↓
User clicks "Start 6-Phase Translation"
```

### Phases 1-6: Generation Simulation

```
Phase 1: Document Processing
┌─────────────────────────────────────────┐
│ Simulated Process:                      │
│ • Extract text from PDF                 │
│ • Parse metadata                        │
│ • Normalize formatting                  │
│                                         │
│ Output: "Sales contract between..."     │
│ Progress: 20%                           │
└─────────────────────────────────────────┘
         ↓ (2 second delay)
         ↓

Phase 2: Contract Analysis
┌─────────────────────────────────────────┐
│ Simulated Process:                      │
│ • Extract parties: seller, buyer        │
│ • Extract amounts: price, delivery cost │
│ • Extract dates: deadline               │
│ • Extract conditions: payment, delivery │
│                                         │
│ Output: {                               │
│   parties: [{name, role}],              │
│   amount: 1000,                         │
│   deadline: "30 days"                   │
│ }                                       │
│ Progress: 40%                           │
└─────────────────────────────────────────┘
         ↓ (2 second delay)
         ↓

Phase 3: Code Generation
┌─────────────────────────────────────────┐
│ Actual Process:                         │
│ • LLM (gpt-4o-mini) given schema        │
│ • Generates Solidity code               │
│ • Mock in demo (simulated)              │
│                                         │
│ Output: Solidity contract code          │
│ Progress: 60%                           │
│                                         │
│ Preview: (textarea shows code)          │
└─────────────────────────────────────────┘
         ↓ (2 second delay)
         ↓

Phase 4: Security Audit
┌─────────────────────────────────────────┐
│ Simulated Process:                      │
│ • Analyze for reentrancy                │
│ • Check state management                │
│ • Review access control                 │
│                                         │
│ Output: {                               │
│   severity: "medium",                   │
│   issues: [                             │
│     "Reentrancy risk",                 │
│     "State mgmt"                        │
│   ]                                     │
│ }                                       │
│ Status: ⚠️ Medium Risk                  │
│ Progress: 80%                           │
└─────────────────────────────────────────┘
         ↓ (2 second delay)
         ↓

Phase 5: ABI Generation
┌─────────────────────────────────────────┐
│ Actual Process:                         │
│ • Extract function signatures           │
│ • Extract parameter types               │
│ • Extract return types                  │
│ • Mock in demo (simulated)              │
│                                         │
│ Output: JSON ABI array                  │
│ Progress: 90%                           │
│                                         │
│ Preview: (textarea shows JSON)          │
└─────────────────────────────────────────┘
         ↓ (2 second delay)
         ↓

Phase 6: MCP Server Generation
┌─────────────────────────────────────────┐
│ Actual Process:                         │
│ • Generate Python FastMCP server        │
│ • Create tools for each function        │
│ • Add .env loading logic                │
│ • Add ABI loading from file             │
│ • Add Web3.py integration               │
│ • Mock in demo (simulated)              │
│                                         │
│ Output: Python server script            │
│ Status: ✓ Complete                      │
│ Progress: 100%                          │
└─────────────────────────────────────────┘
```

### Deployment Phase: User Actions

```
Step 1: Download Files
┌─────────────────────────────────────────┐
│ React: downloadFile() function triggers │
│        browser download APIs            │
│                                         │
│ Files saved to Downloads:               │
│ • sales_contract.sol                    │
│ • sales_contract.abi.json               │
│ • sales_mcp_server.py                   │
└─────────────────────────────────────────┘
         ↓ (user action)
         ↓

Step 2: Deploy via Remix
┌─────────────────────────────────────────┐
│ User actions:                           │
│ 1. Open remix.ethereum.org              │
│ 2. New file → paste .sol                │
│ 3. Compile → check for errors           │
│ 4. Deploy → Hardhat Provider            │
│ 5. Get address from receipt             │
│                                         │
│ Result: deployed_address = "0x5C18..." │
└─────────────────────────────────────────┘
         ↓ (user copies address)
         ↓

Step 3: Configure in Demo
┌─────────────────────────────────────────┐
│ User fills form fields:                 │
│                                         │
│ RPC_URL:          "http://127.0.0.1:..." │
│ CONTRACT_ADDRESS: "0x5C18C93C..."        │
│ PRIVATE_KEY:      "555b62b19c39..."      │
│                                         │
│ Form validation: All fields filled?     │
│ Button enabled: "✓ Start MCP Server"   │
└─────────────────────────────────────────┘
         ↓ (user clicks button)
         ↓

Step 4: Start MCP Server
┌─────────────────────────────────────────┐
│ Demo simulation:                        │
│ 1. Set mcpServerRunning = true          │
│ 2. Show "✓ MCP Server Running"          │
│ 3. Enable chatbot UI                    │
│ 4. Display contract address             │
│                                         │
│ (In real scenario:                      │
│  python mcp_server.py                   │
│  Server loads .env & ABI                │
│  Waits for stdio commands)              │
└─────────────────────────────────────────┘
```

### Chatbot Interaction Phase

```
User Input: "Make a payment"
         ↓
┌─────────────────────────────────────────┐
│ Chatbot Logic:                          │
│ 1. Add message to chat history          │
│ 2. Clear input field                    │
│ 3. Set loading = true                   │
│ 4. Wait 1.5 seconds (simulate delay)    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ MCP Server (simulated):                 │
│ 1. Parse "Make a payment"               │
│ 2. Determine function: makePayment()    │
│ 3. Build transaction:                   │
│    {                                    │
│      from: "0x742d...",                 │
│      to: "0x5C18...",                   │
│      function: "makePayment()",          │
│      value: web3.to_wei(1, 'ether'),    │
│      gas: 2000000,                      │
│      gasPrice: web3.to_wei('20', 'gwei')│
│    }                                    │
│ 4. Sign with private key                │
│ 5. Send to Ganache via RPC              │
│ 6. Get tx_hash: "0x1a2b3c..."          │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Return Response:                        │
│                                         │
│ {                                       │
│   "tx_hash": "0x1a2b3c4d5e6f...",      │
│   "success": true                       │
│ }                                       │
│                                         │
│ (Or error if contract not deployed)     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Chatbot Display:                        │
│ • Randomly select response template     │
│ • Format with result data               │
│ • Add to chat history                   │
│ • Set loading = false                   │
│                                         │
│ Display:                                │
│ "Called makePayment() →                 │
│  Transaction: 0x1a2b3c4d5e6f... ✓"     │
└─────────────────────────────────────────┘
```

---

## 🔐 Security Considerations

### Data Flow Security

```
User Input
   ↓
Browser (HTTPS if deployed to web)
   ↓
Local Filesystem (.env)
   ↓
MCP Server Process
   ↓
Private Key (IN MEMORY ONLY)
   ↓
Web3.py (Local)
   ↓
RPC Connection (Local Network)
   ↓
Ganache (No real blockchain)
```

### Key Security Features

1. **Private Key Storage**
   - Stored only in local `.env` file
   - Never sent to browser or server
   - Loaded directly into MCP process memory
   - Accessible only by local user

2. **Transaction Signing**
   - Web3.py signs locally using private key
   - Signed transaction sent to Ganache
   - Ganache validates signature
   - No centralized signature server

3. **Environment Isolation**
   - Each contract has separate `.env`
   - `.env.example` provides template (safe to share)
   - No secrets in code or documentation
   - User responsible for filling `.env`

4. **Ganache Safety**
   - Runs locally (no external connections)
   - Test accounts with fake funds
   - No mainnet funds at risk
   - Transaction history isolated

---

## 💾 File Generation & Loading

### Generated Files

```
When demo.html runs Phases 1-6:
(Simulated, not actual API calls in demo)

Output would be:
├── output/Sales_1/
│   ├── TechGear_M_RetailChai.sol
│   │   ├── Contract declaration
│   │   ├── State variables
│   │   ├── Events
│   │   ├── Functions (payable, nonpayable, view)
│   │   └── Modifiers
│   │
│   ├── TechGear_M_RetailChai.abi.json
│   │   ├── Constructor ABI
│   │   ├── Function ABIs (with inputs/outputs)
│   │   ├── Event ABIs
│   │   └── Fallback function ABI
│   │
│   ├── TechGear_M_RetailChai_mcp_server.py
│   │   ├── Imports (Web3, FastMCP, dotenv)
│   │   ├── .env loading
│   │   ├── ABI loading from file
│   │   ├── Web3.py setup
│   │   ├── FastMCP instance creation
│   │   └── Tool definitions for each function
│   │
│   ├── .env (USER FILLS)
│   │   ├── RPC_URL
│   │   ├── PRIVATE_KEY
│   │   └── CONTRACT_ADDRESS
│   │
│   ├── .env.example
│   │   └── Template (safe to share)
│   │
│   ├── contract_schema.json
│   │   └── Parsed contract structure
│   │
│   ├── security_audit.json
│   │   ├── Vulnerabilities found
│   │   ├── Severity levels
│   │   └── Recommendations
│   │
│   └── README.md
│       └── Contract documentation
```

### File Usage in MCP Server

```python
# On MCP Server startup:

# 1. Load configuration
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
# Result: RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS loaded

# 2. Load ABI
abi_path = Path(__file__).parent / 'TechGear_M_RetailChai.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)
# Result: contract_abi contains all function definitions

# 3. Connect to blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)
# Result: contract object ready to call functions

# 4. Define tools for each ABI function
@mcp.tool()
def makePayment():
    """From ABI: inputs=[], name='makePayment', stateMutability='payable'"""
    # Implementation...
```

---

## 🎮 Interactive State Management

### React State Variables

```javascript
// Main workflow
const [phase, setPhase] = useState(0);              // 0-6
const [contractType, setContractType] = useState('sales');
const [currentPhaseInfo, setCurrentPhaseInfo] = useState({...});

// Generated code storage
const [generatedData, setGeneratedData] = useState({
    solidity: '',
    abi: '',
    schema: '',
    audit: '',
    mcp: ''
});

// Deployment configuration
const [contractAddress, setContractAddress] = useState('');
const [privateKey, setPrivateKey] = useState('');
const [rpcUrl, setRpcUrl] = useState('http://127.0.0.1:7545');
const [mcpServerRunning, setMcpServerRunning] = useState(false);

// Chatbot state
const [chatMessages, setChatMessages] = useState([]);
const [chatInput, setChatInput] = useState('');
const [chatLoading, setChatLoading] = useState(false);
```

### State Transitions

```
Initial: phase = 0
         contractType = 'sales'
         mcpServerRunning = false
         chatMessages = [assistant greeting]

         ↓ (click contract type)

User selects: contractType = 'investment'

         ↓ (click "Start 6-Phase Translation")

Phase 1: phase = 1
         currentPhaseInfo = {title, status, output, progress: 20}

         ↓ (2 second wait)

Phase 2: phase = 2
         currentPhaseInfo = {progress: 40}
         
         ... (repeat for phases 3-6)

Phase 6: phase = 6
         generatedData.solidity = "// SPDX-License-Identifier..."
         generatedData.abi = JSON formatted ABI
         generatedData.mcp = Python FastMCP server code

         ↓ (user downloads & deploys)

Post-Deploy: User enters config values
             contractAddress = "0x5C18..."
             privateKey = "555b62b19c39..."

         ↓ (click "Start MCP Server")

MCP Running: mcpServerRunning = true
             Chatbot UI enabled

         ↓ (user sends chat message)

Chat Active: chatMessages = [...messages]
             chatLoading = true/false
             chatInput = "" (cleared after send)
```

---

## 📦 Component Hierarchy

```
<ContractTranslatorDemo>
│
├─ Phase 0: Contract Selection UI
│  ├─ Grid of contract type buttons
│  └─ "Start 6-Phase Translation" button
│
├─ Phases 1-6: Generation Display
│  ├─ <StepIndicator />
│  │  └─ Step numbers and labels
│  ├─ Phase Animation Box
│  │  ├─ Phase icon (🎨 emoji)
│  │  └─ Phase title
│  ├─ Phase Status Card
│  │  ├─ Title and status badges
│  │  ├─ Progress description
│  │  └─ Progress bar
│  └─ Code Preview Textareas
│     ├─ Solidity code (Phase 3)
│     └─ ABI JSON (Phase 5)
│
└─ Phase 6+: Deployment & Chatbot
   ├─ Left Column: Deployment Guide
   │  ├─ Download Buttons
   │  ├─ Remix Instructions Card
   │  └─ Configuration Form
   │     ├─ RPC URL input
   │     ├─ Contract Address input
   │     ├─ Private Key input (password)
   │     └─ "Start MCP Server" button
   │
   └─ Right Column: Chatbot
      ├─ Chat Message Display Area
      │  └─ Message bubbles (user/assistant)
      ├─ Chat Input Form
      │  ├─ Text input
      │  └─ Send button
      ├─ Quick Action Buttons
      │  ├─ "💳 Make Payment"
      │  ├─ "📊 Check Status"
      │  ├─ "✓ Confirm Delivery"
      │  └─ "💰 Get Balance"
      └─ MCP Status Indicator
```

---

## 🔌 API Connections

### RPC Calls (via Web3.py in MCP Server)

```
web3.eth.get_transaction_count(address)
  → Gets nonce for transaction ordering
  → Returns: integer (e.g., 5)

web3.eth.send_raw_transaction(signed_txn.rawTransaction)
  → Sends signed transaction to Ganache
  → Returns: transaction hash (e.g., 0x1a2b3c...)

contract.functions.functionName(...).call()
  → Calls view/read-only function
  → Returns: function result (no state change)

contract.functions.functionName(...).buildTransaction(tx_dict)
  → Builds transaction (not yet signed)
  → Returns: unsigned transaction object

web3.eth.account.sign_transaction(txn, private_key)
  → Signs transaction with private key
  → Returns: signed transaction object

web3.to_wei(amount, unit)
  → Converts Ether to Wei (1 ETH = 10^18 Wei)
  → Example: web3.to_wei(1, 'ether') → 1000000000000000000

Web3.to_checksum_address(address)
  → Converts address to checksum format
  → Example: 0x5c18c93c... → 0x5C18C93C...
```

### MCP Tool Calls (via stdio)

```
Browser → MCP Server:
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "makePayment",
    "arguments": {}
  }
}

MCP Server → Browser:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"tx_hash\": \"0x1a2b3c...\"}"
      }
    ]
  }
}
```

---

## 📊 Performance Metrics

### Phase Timing
```
Phase 1: Document Processing    → ~2 seconds
Phase 2: Contract Analysis      → ~2 seconds
Phase 3: Code Generation        → ~2 seconds
Phase 4: Security Audit         → ~2 seconds
Phase 5: ABI Generation         → ~2 seconds
Phase 6: MCP Server Generation  → ~2 seconds
────────────────────────────────────────
Total Generation Time: ~12 seconds
```

### File Sizes (Typical)
```
.sol file:           8-15 KB   (Solidity source)
.abi.json:           2-5 KB    (Function interface)
_mcp_server.py:      12-20 KB  (FastMCP server)
```

### Network Usage
```
Browser → Download: .sol + .abi.json + .py ~25 KB total
MCP ↔ Ganache: Minimal (local network)
No external API calls in local setup
```

---

## 🎯 Success Indicators

You've successfully completed the demo when you see:

1. ✅ All 6 phases complete with progress bars
2. ✅ "Download .sol", ".abi", and ".py" buttons clickable
3. ✅ Contract deployed in Remix (address received)
4. ✅ Configuration form filled with real values
5. ✅ Green "✓ MCP Server Running" status
6. ✅ Chatbot responds to function calls
7. ✅ Ganache shows transactions and balance changes
8. ✅ Chat history shows multiple interactions

---

**Architecture Document Complete**  
**All components documented and interconnected**  
**Ready for production deployment with real contracts**
