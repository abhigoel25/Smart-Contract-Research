// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
   --> <stdin>:100:1:
    |
100 | 
    | ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    // Parties
    struct Party {
        string name;
        address partyAddress;
        string entityType;
    }

    Party public company;
    Party public investor;

    // Financial Terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate;
    }

    FinancialTerm public purchasePrice;
    FinancialTerm public totalInvestment;

    // Dates
    struct InvestmentDate {
        string dateType;
        string value;
        uint256 dayOfMonth;
    }

    InvestmentDate public startDate;
    InvestmentDate public redemptionTriggerDate;

    // Obligations
    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Obligation public companyObligation;

    // Special Terms
    string[] public specialTerms;

    // Conditions
    struct Conditions {
        string antiDilution;
        string dividend;
    }

    Conditions public conditions;

    // Termination Conditions
    string[] public terminationConditions;

    // Events
    event InvestmentCreated();
    event ObligationFulfilled(string obligationDescription);

    constructor() {
        // Initialize parties with sensible defaults
        company = Party("BlockChain Innovations Inc.", address(0), "company");
        investor = Party("Venture Capital Fund VII, LP", address(0), "company");

        // Initialize financial terms
        purchasePrice = FinancialTerm(8000000 ether, "USD", "purchase price per share", "one-time", 0);
        totalInvestment = FinancialTerm(10000000 ether, "USD", "total investment amount", "one-time", 0);

        // Initialize dates
        startDate = InvestmentDate("start", "2025-01-01", 1);
        redemptionTriggerDate = InvestmentDate("redemption_trigger", "2030-01-01", 1);

        // Initialize obligations
        companyObligation = Obligation("company", "redeem shares if no qualified IPO by January 1, 2030", 
                                        "12 months from redemption trigger event", "");

        // Initialize special terms
        specialTerms.push("One designated board observer seat for the investor");
        specialTerms.push("Quarterly unaudited and annual audited financial statements provided to the investor");
        specialTerms.push("Right to maintain ownership percentage in future financings");
        specialTerms.push("Must participate in company sale if approved by majority holders");

        // Initialize conditions
        conditions = Conditions("weighted average anti-dilution protection in down rounds", "8% annual return (non-cumulative)");

        // Initialize termination conditions
        terminationConditions.push("If a qualified IPO does not occur by January 1, 2030");

        emit InvestmentCreated();
    }

    // Getters for parties
    function getCompany() public view returns (string memory, address, string memory) {
        return (company.name, company.partyAddress, company.entityType);