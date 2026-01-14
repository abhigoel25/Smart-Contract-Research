// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:86:1:
   |
86 | 
   | ^
// This contract failed to compile

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    
    struct Party {
        string name;
        string role;
        address entityAddress;
        string email;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate;
    }

    struct Date {
        string dateType;
        string value;
        uint256 dayOfMonth;
        uint256 frequency;
    }
    
    struct Asset {
        string assetType;
        string description;
        uint256 quantity;
        uint256 value;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Party[] public parties;
    FinancialTerm[] public financialTerms;
    Date[] public dates;
    Asset[] public assets;
    Obligation[] public obligations;
    string[] public specialTerms;
    string[] public terminationConditions;

    event InvestmentExecuted(uint256 amount, string purpose);
    
    constructor() {
        parties.push(Party("BlockChain Innovations Inc.", "company", address(0), "", "company"));
        parties.push(Party("Venture Capital Fund VII, LP", "investor", address(0), "", "company"));

        financialTerms.push(FinancialTerm(10000000, "USD", "investment", "one-time", 0));
        financialTerms.push(FinancialTerm(8, "USD", "purchase price per share", "one-time", 0));
        financialTerms.push(FinancialTerm(4000000, "USD", "product development", "one-time", 0));
        financialTerms.push(FinancialTerm(3500000, "USD", "sales and marketing", "one-time", 0));
        financialTerms.push(FinancialTerm(1500000, "USD", "operations and administration", "one-time", 0));
        financialTerms.push(FinancialTerm(1000000, "USD", "working capital reserve", "one-time", 0));

        dates.push(Date("start", "2025-01-01", 1, 0));
        dates.push(Date("redemption_trigger", "2030-01-01", 1, 0));

        assets.push(Asset("equity", "Series A Preferred Stock", 1250000, 10000000));

        obligations.push(Obligation("BlockChain Innovations Inc.", "must redeem shares if no qualified IPO by January 1, 2030", "January 1, 2031", ""));
        
        specialTerms.push("8% annual return on non-cumulative dividend");
        specialTerms.push("Investors participate pro-rata in remaining proceeds");
        specialTerms.push("1x non-participating in liquidation events");
        specialTerms.push("Weighted average anti-dilution protection in down rounds");
        specialTerms.push("Right to maintain ownership percentage in future financings");
        specialTerms.push("Mandatory participation in company sale if approved by majority holders");

        terminationConditions.push("Company must redeem shares if no qualified IPO by specified date");
    }

    // Getters
    function getParty(address partyAddress) public view returns (string memory name, string memory role, string memory email, string memory entityType) {
        for (uint i = 0; i < parties.length; i++) {
            if (parties[i].entityAddress == partyAddress) {
                return (parties[i].name, parties[i].role, parties[i].email, parties[i].entityType);