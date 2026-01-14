// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:70:1:
   |
70 | 
   | ^
// This contract failed to compile

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    
    // State Variables
    struct Party {
        string name;
        string role;
        address addr;
        string email;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate; // Unix timestamp for the due date
    }
    
    struct DateInfo {
        string dateType;
        string value; // Date as string (ISO format)
        uint256 dayOfMonth;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Party[2] public parties; // 0: Company, 1: Investor
    FinancialTerm[2] public financialTerms;
    DateInfo[2] public dates;
    Obligation[2] public obligations;

    // Events
    event InvestmentExecuted(uint256 investmentAmount);
    event ObligationFulfilled(string party, string description);

    // Constructor to initialize the contract
    constructor() {
        // Initializing parties with default values
        parties[0] = Party("BlockChain Innovations Inc.", "Company", address(0), "", "company");
        parties[1] = Party("Venture Capital Fund VII, LP", "Investor", address(0), "", "company");

        // Initializing financial terms with provided values
        financialTerms[0] = FinancialTerm(8000000, "USD", "purchase price per share", "one-time", 0);
        financialTerms[1] = FinancialTerm(10000000, "USD", "total investment amount", "one-time", 0);

        // Initializing dates with provided values
        dates[0] = DateInfo("start", "2025-01-01", 1, "");
        dates[1] = DateInfo("redemption_trigger", "2030-01-01", 1, "");

        // Initializing obligations
        obligations[0] = Obligation("Company", "Redeem shares if no qualified IPO by redemption trigger date.", "12 months from redemption trigger event", "");
        obligations[1] = Obligation("Investor", "Must participate in company sale if approved by majority holders.", "upon company sale event", "");
    }

    // Getters
    function getParty(uint8 index) public view returns (string memory name, string memory role, address addr, string memory email, string memory entityType) {
        if (index < 2) {
            Party memory party = parties[index];
            return (party.name, party.role, party.addr, party.email, party.entityType);