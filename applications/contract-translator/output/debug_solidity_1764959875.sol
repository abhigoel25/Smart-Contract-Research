// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got ';'
  --> <stdin>:68:30:
   |
68 |             addr: address(0),; // placeholder for missing address
   |                              ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    // Parties
    struct Party {
        string name;
        string role;
        address addr;  // Using address(0) for missing
        string entityType;
    }

    Party public company;
    Party public investor;

    // Financial Terms
    struct FinancialTerm {
        uint256 amount;  // Defaults to 0 if missing
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate;  // Defaults to 0 if missing
    }

    FinancialTerm public totalInvestment;
    FinancialTerm public purchasePrice;

    // Dates
    struct ContractDate {
        string dateType;
        string value;
        uint256 dayOfMonth; // Defaults to 0 if missing
        string frequency;
    }

    ContractDate public startDate;
    ContractDate public redemptionTriggerDate;

    // Assets
    struct Asset {
        string assetType;
        string description;
        string location; // Using "" for missing
        uint256 quantity; // Defaults to 0 if missing
        uint256 value; // Defaults to 0 if missing
    }

    Asset public seriesAStock;

    // Obligations
    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach; // Using "" for missing
    }

    Obligation public redemptionObligation;

    // Events
    event InvestmentTriggered(address indexed investor, uint256 amount);
    event SharesRedeemed(uint256 amount);

    // Constructor
    constructor() {
        company = Party({
            name: "BlockChain Innovations Inc.",
            addr: address(0),; // placeholder for missing address
        });

        investor = Party({
            name: "Venture Capital Fund VII, LP",
            addr: address(0),; // placeholder for missing address
        });

        totalInvestment = FinancialTerm({
            purpose: "total investment amount",
            frequency: "one-time",
            dueDate: 0; // placeholder for missing due date
        });

        purchasePrice = FinancialTerm({
            purpose: "purchase price per share",
            frequency: "one-time",
            dueDate: 0; // placeholder for missing due date
        });

        startDate = ContractDate({
            value: "2025-01-01",
            frequency: ""; // placeholder for missing frequency
        });

        redemptionTriggerDate = ContractDate({
            value: "2030-01-01",
            frequency: ""; // placeholder for missing frequency
        });

        seriesAStock = Asset({
            description: "Series A Preferred Stock",
            location: "",; // placeholder for missing location
            value: 0; // placeholder for missing value
        });

        redemptionObligation = Obligation({
            description: "Redeem shares if no qualified IPO by January 1, 2030",
            deadline: "12 months from redemption trigger event",
            penaltyForBreach: ""; // placeholder for missing penalty
        });
    }

    // Getters
    function getCompany() public view returns (string memory, string memory, address, string memory) {
        return (company.name, company.role, company.addr, company.entityType);