# IBM Agentics Contract Translator - Complete Demo Guide

## 📋 Overview

The `demo.html` file provides a complete end-to-end demonstration of the IBM Agentics smart contract translation and deployment workflow. It integrates:

1. **6-Phase Contract Translation** - Automated AI-powered contract to Solidity conversion
2. **Remix IDE Integration** - Manual deployment step using Remix
3. **Local Environment Configuration** - Setting up `.env` files per contract
4. **MCP Server Deployment** - Automatic FastMCP server startup
5. **AI Chatbot Interface** - Natural language interaction with deployed contracts

## 🎯 How It Works (Complete Workflow)

### Phase 0: Contract Type Selection
- Choose from 6 contract types: Sales, Employment, Investment, NDA, Rental, Loan
- Each type represents a different business agreement template
- Selection determines the Solidity contract structure and ABI functions

### Phases 1-6: Automated Translation

#### Phase 1: Document Processing 📄
- **Input**: PDF or text document containing natural language contract
- **Process**: Extracts contract text and metadata
- **Output**: Raw contract text (1,000+ characters typically)
- **Time**: ~2 seconds simulation

#### Phase 2: Contract Analysis 🔍
- **Input**: Extracted contract text
- **Process**: IBM Agentics parses parties, financial terms, conditions
- **Output**: Structured contract schema (parties, amount, dates, etc.)
- **Time**: ~2 seconds simulation

#### Phase 3: Code Generation ⚙️
- **Input**: Contract schema from Phase 2
- **Process**: LLM (gpt-4o-mini) generates Solidity smart contract
- **Output**: Complete, compilable Solidity code (~100-200 lines)
- **Time**: ~2 seconds simulation
- **Features**: Functions, events, modifiers, state variables

#### Phase 4: Security Audit 🔐
- **Input**: Generated Solidity contract
- **Process**: Analyzes for vulnerabilities (reentrancy, state issues, etc.)
- **Output**: Security report with severity level (Low/Medium/High)
- **Time**: ~2 seconds simulation
- **Action**: Allows user to review risks before proceeding

#### Phase 5: ABI Generation 📋
- **Input**: Solidity contract code
- **Process**: Extracts Application Binary Interface (ABI)
- **Output**: JSON ABI file with function signatures and types
- **Time**: ~2 seconds simulation
- **Used By**: MCP server for function calls, Remix for deployment

#### Phase 6: MCP Server Generation 🤖
- **Input**: ABI and contract schema
- **Process**: Generates FastMCP Python server with tools for each function
- **Output**: Standalone Python MCP server script
- **Time**: ~2 seconds simulation
- **Features**: 
  - Loads local `.env` file (RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS)
  - Loads ABI from `.abi.json` file
  - Creates @mcp.tool() decorated functions for each contract function
  - Handles payable, non-payable, and view functions
  - Error handling and transaction signing

### Post-Generation: Deployment Phase

#### Step 1: Manual Deployment via Remix 🔗

**Why Manual?**
- Cannot deploy directly from browser to Ganache without backend
- Remix provides safe, user-controlled deployment environment
- Lets you verify code and customize constructor parameters

**Steps:**
1. Click "Download .sol File" button
2. Go to [remix.ethereum.org](https://remix.ethereum.org)
3. Create new file (e.g., `SalesAgreement.sol`)
4. Paste downloaded Solidity code
5. Compile code (Compiler → Compile)
6. Deploy contract:
   - Go to "Deploy & Run Transactions" tab
   - Select environment: **"Hardhat Provider"** or **"Injected Web3"** (MetaMask)
   - For Ganache, use Hardhat with `http://127.0.0.1:7545` RPC endpoint
   - Click "Deploy"
7. Copy deployed contract address from deployment receipt

#### Step 2: Configure Environment Variables

**What Each Variable Does:**

1. **RPC_URL** (e.g., `http://127.0.0.1:7545`)
   - Connection endpoint to blockchain node
   - Default: Ganache on port 7545
   - Alternative: Ethereum testnet (Sepolia), mainnet, or other networks
   - Used by Web3.py to read blockchain state and send transactions

2. **Contract Address** (e.g., `0x1a2b3c...`)
   - Address where contract was deployed
   - From Remix deployment receipt
   - Used to identify which contract instance to interact with
   - Should be in checksum format (mixed case) or checksummed by Web3.py

3. **Private Key** (64 hex characters, no `0x` prefix)
   - From Ganache account details (not the display address)
   - Used to sign transactions (making payments, calling functions, etc.)
   - **NEVER share this in production**
   - In demo: Safe since Ganache is local and accounts are fake
   - Example format: `555b62b19c392d8f005e0195ba31e4c2eca6d7cbc4c75014d9025614380b10e4`

#### Step 3: Start MCP Server

**What Happens:**
1. MCP server loads local `.env` file from same directory
2. Reads RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS
3. Connects to blockchain at RPC_URL
4. Loads ABI from local `.abi.json` file
5. Initializes Web3.py with account derived from private key
6. Creates FastMCP instance with tools for each contract function
7. Server runs on `stdio` (communicates via standard input/output)
8. Chatbot connects to server via stdio

**Status Indicator:**
- Green "✓ MCP Server Running" appears when ready
- Shows truncated contract address for verification

#### Step 4: Use Chatbot to Invoke Functions

**Chatbot Features:**
- Natural language processing (LLM-powered)
- Understands requests like "make a payment", "check balance", "confirm delivery"
- Converts natural language → specific function calls
- Executes functions via MCP server
- Returns transaction hashes or results
- Simulates network delays and realistic responses

**Quick Action Buttons:**
- 💳 Make Payment - Calls `makePayment()` payable function
- 📊 Check Status - Calls `getStatus()` view function
- ✓ Confirm Delivery - Calls `confirmDelivery()` state-changing function
- 💰 Get Balance - Checks account ETH balance

**What Happens Behind the Scenes:**
1. Chatbot receives user request
2. LLM determines which function to call
3. MCP server builds transaction with:
   - Function parameters
   - From address (from private key)
   - Gas (2,000,000 wei default)
   - Gas price (20 gwei)
   - Value (if payable function)
4. Web3.py signs transaction with private key
5. Sends raw transaction to Ganache via RPC
6. Ganache executes transaction (state change or read)
7. Returns transaction hash (for state changes) or result (for view functions)
8. Chatbot displays response with ✓ or error message

**Real-World Testing:**
- Open Ganache GUI alongside browser
- See account balances change as you make payments
- Verify transaction history in Ganache
- Check contract state variables in Remix (call view functions)

## 📁 Files Generated/Used

### From Phase 6:

```
output/
├── ContractType_1/
│   ├── ContractName.sol                 # Solidity source code
│   ├── ContractName.abi.json            # Function signatures (JSON)
│   ├── ContractName_mcp_server.py       # FastMCP server
│   ├── .env                             # Configuration (LOCAL per contract)
│   ├── .env.example                     # Template (reference)
│   ├── contract_schema.json             # Parsed contract structure
│   ├── security_audit.json              # Security findings
│   └── README.md                        # Contract documentation
```

### Key Files Explained:

**ContractName.sol**
- Compiled Solidity smart contract
- Pastes directly into Remix
- Executable on any EVM blockchain
- Contains all business logic

**ContractName.abi.json**
- JSON Application Binary Interface
- Describes all functions, parameters, return types
- Used by Web3.py, Remix, and other tools
- Auto-loaded by MCP server from same directory

**ContractName_mcp_server.py**
- Standalone Python server
- Wraps contract functions as MCP tools
- Loads local `.env` file (critical!)
- Can run: `python ContractName_mcp_server.py`
- Implements all 6 Web3.py best practices from prompt

**.env (LOCAL)**
- Per-contract configuration
- **NEW FEATURE**: Each contract has its own `.env`
- Must be filled manually with:
  - RPC_URL (Ganache endpoint)
  - PRIVATE_KEY (from Ganache)
  - CONTRACT_ADDRESS (from Remix after deployment)
- Located in same directory as MCP server
- Loaded automatically by MCP server

**.env.example**
- Reference template
- Shows required variables and format
- Safe to share (no secrets)

## 🔄 Complete Workflow Example

### Scenario: Sales Agreement

1. **Select Contract Type**: Click "🛒 Sales Agreement"
2. **Start Translation**: Click "Start 6-Phase Translation"
3. **Watch Progress**: See all 6 phases complete with animations
4. **Download Files**: After Phase 6, buttons appear to download:
   - `sales_contract.sol`
   - `sales_contract.abi.json`
   - `sales_mcp_server.py`

5. **Deploy to Ganache**:
   - Open Remix IDE
   - Paste `.sol` file
   - Compile
   - Deploy to Ganache (Hardhat Provider)
   - Copy address: `0x5C18C93C477f05496cCb8De3D2d8B1F1e82E2c08`

6. **Configure Demo**:
   - RPC URL: `http://127.0.0.1:7545`
   - Contract Address: `0x5C18C93C477f05496cCb8De3D2d8B1F1e82E2c08`
   - Private Key: `555b62b19c392d8f005e0195ba31e4c2eca6d7cbc4c75014d9025614380b10e4`

7. **Start MCP Server**: Click "✓ Start MCP Server"

8. **Use Chatbot**:
   - Type: "Make a payment"
   - Chatbot calls `makePayment()` function
   - Transaction executes on Ganache
   - See transaction hash in chat
   - Watch Ganache account balance decrease by 1 ETH

9. **Verify in Ganache**:
   - Open Ganache
   - See new transaction in history
   - Contract state variables updated
   - Account balances reflect payment

## 🛠️ Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────┐
│         Browser (demo.html - React)             │
│  • Contract type selection                      │
│  • 6-phase visualization                        │
│  • File download buttons                        │
│  • Chatbot UI                                   │
└───────────┬─────────────────────────────────────┘
            │
            │ Downloads files
            ↓
┌─────────────────────────────────────────────────┐
│    User's Filesystem (Local Directory)          │
│  • contract.sol (to Remix)                      │
│  • contract.abi.json                            │
│  • mcp_server.py (Python)                       │
│  • .env (user configures)                       │
└───────────┬─────────────────────────────────────┘
            │
            │ User deploys via Remix
            ↓
┌─────────────────────────────────────────────────┐
│      Remix IDE (remix.ethereum.org)             │
│  • Compile .sol                                 │
│  • Deploy to Ganache                            │
│  • Get contract address                         │
└───────────┬─────────────────────────────────────┘
            │
            │ User updates .env with address
            ↓
┌─────────────────────────────────────────────────┐
│   MCP Server (mcp_server.py - Python)           │
│  • Loads local .env                             │
│  • Loads .abi.json                              │
│  • Creates Web3.py contract instance            │
│  • Exposes functions as MCP tools               │
└───────────┬─────────────────────────────────────┘
            │ stdio
            ↓
┌─────────────────────────────────────────────────┐
│  Chatbot (demo.html JavaScript)                 │
│  • Sends natural language requests              │
│  • Receives function results                    │
│  • Displays responses                           │
└─────────────────────────────────────────────────┘
```

## 🚀 Advanced Features

### 1. Smart Function Detection
The MCP server automatically:
- Identifies payable functions (require ETH value)
- Identifies view functions (read-only, no gas)
- Identifies state-changing functions (require signing)
- Creates appropriate transaction structures for each type

### 2. Gas Management
```python
'gas': 2000000,                    # Max gas units
'gasPrice': web3.to_wei('20', 'gwei')  # Per unit
```
Auto-calculated to reasonable defaults for local Ganache

### 3. Nonce Management
```python
'nonce': web3.eth.get_transaction_count(account.address)
```
Fetched from blockchain to prevent replay attacks

### 4. Transaction Signing
```python
signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
```
All transactions cryptographically signed with private key

### 5. Error Handling
All MCP tools wrapped in try/except:
```python
try:
    # Call contract function
    result = contract.functions.functionName().call()
    return {"result": result}
except Exception as e:
    return {"error": str(e)}
```

## 📊 What You Can Learn

This demo teaches:

1. **Contract Translation**: How natural language becomes smart contracts
2. **Security Analysis**: Identifying blockchain vulnerabilities
3. **ABI Interface**: Understanding function signatures
4. **Web3.py**: Blockchain interaction in Python
5. **MCP Servers**: Exposing blockchain as tools
6. **Local Development**: Ganache for testing
7. **Remix IDE**: Compiling and deploying contracts
8. **AI Integration**: Using LLMs for contract generation

## 🔧 Customization

### Adding New Contract Types

Edit `demo.html` line ~90:

```javascript
const contractTypes = [
    { id: 'sales', name: 'Sales Agreement', icon: '🛒' },
    { id: 'employment', name: 'Employment Contract', icon: '💼' },
    { id: 'investment', name: 'Investment Agreement', icon: '💰' },
    { id: 'nda', name: 'NDA', icon: '🔒' },
    { id: 'rental', name: 'Rental Agreement', icon: '🏠' },
    { id: 'loan', name: 'Loan Agreement', icon: '🏦' },
    // ADD NEW TYPE HERE:
    { id: 'partnership', name: 'Partnership Agreement', icon: '🤝' },
];
```

### Changing Simulation Times

Edit phase generation loop (~line 200):

```javascript
await new Promise(res => setTimeout(res, 2000));  // 2 seconds per phase
```

### Customizing Solidity Templates

Edit `generateMockSolidity()` function (~line 250):

```javascript
const templates = {
    sales: `// Your Solidity code here`,
    custom: `// New contract type`,
};
```

## ⚠️ Important Notes

### For Local Development Only
- Ganache runs on local machine
- Private keys are fake test accounts
- No real funds or assets involved
- Perfect for learning and testing

### Production Considerations
- Never hardcode private keys
- Use environment files with restricted permissions
- Deploy to testnet first (Sepolia, Goerli)
- Conduct thorough security audits
- Use multi-sig wallets for large amounts
- Test with small amounts first

### Known Limitations
- Chatbot is simulated (not real LLM in browser)
- File downloads work only in modern browsers
- Ganache must be running on `127.0.0.1:7545`
- MetaMask required for "Injected Web3" option
- Constructor parameters currently not customizable in UI

## 📚 Next Steps

1. **Generate First Contract**: Select a contract type and run the demo
2. **Deploy on Ganache**: Follow the Remix steps
3. **Customize Configuration**: Update `.env` values
4. **Run MCP Server**: Execute the generated Python script
5. **Test Functions**: Use chatbot to invoke contract functions
6. **Verify Results**: Check Ganache for state changes
7. **Iterate**: Generate more contracts, test different types
8. **Deploy to Testnet**: When ready, use Sepolia or other testnets

## 🆘 Troubleshooting

### "Could not transact with/call contract function"
**Cause**: Contract not deployed or address incorrect  
**Solution**: Verify address in Remix, update `.env`

### "RPC endpoint not reachable"
**Cause**: Ganache not running  
**Solution**: Start Ganache on port 7545

### "Invalid private key"
**Cause**: Wrong format (address vs. private key)  
**Solution**: Get 64-char private key from Ganache account details

### "Transaction out of gas"
**Cause**: Gas limit too low  
**Solution**: Increase `'gas': 3000000` in MCP server

### File download doesn't work
**Cause**: Browser security restrictions  
**Solution**: Use modern browser (Chrome, Firefox, Safari, Edge)

---

**Demo Version**: 2.0  
**Last Updated**: December 2024  
**Compatibility**: All modern browsers, Python 3.8+, Ganache CLI or Desktop
