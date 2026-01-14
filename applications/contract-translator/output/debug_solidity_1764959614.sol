// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
   --> <stdin>:102:1:
    |
102 | 
    | ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferenceStockPurchaseAgreement {

    // Parties
    struct Party {
        string name;
        string role;
        address addr;
        string email;
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

    FinancialTerm public investmentTerm;
    FinancialTerm public purchasePriceTerm;

    // Dates
    struct Dates {
        string dateType;
        string value;
        uint256 dayOfMonth;
        string frequency;
    }

    Dates public startDate;
    Dates public redemptionTriggerDate;

    // Assets
    struct Asset {
        string assetType;
        string description;
        string location;
        uint256 quantity;
        uint256 value;
    }

    Asset public asset;

    // Obligations
    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Obligation public obligation;

    // Special Terms
    string[] public specialTerms;

    // Events
    event InvestmentReceived(uint256 amount);
    event SharesRedeemed(uint256 quantity);

    constructor() {
        // Parties
        company = Party("BlockChain Innovations Inc.", "company", address(0), "", "company");
        investor = Party("Venture Capital Fund VII, LP", "investor", address(0), "", "company");

        // Financial Terms
        investmentTerm = FinancialTerm(10000000 * 1 ether, "USD", "investment", "one-time", 0);
        purchasePriceTerm = FinancialTerm(8 * 1 ether, "USD", "purchase price per share", "one-time", 0);

        // Dates
        startDate = Dates("start", "2025-01-01", 1, "");
        redemptionTriggerDate = Dates("redemption_trigger", "2030-01-01", 1, "");

        // Assets
        asset = Asset("equity", "Series A Preferred Stock", "", 1250000, 10000000 * 1 ether);

        // Obligations
        obligation = Obligation("BlockChain Innovations Inc.", "Redeem shares if no qualified IPO by January 1, 2030", "12 months from redemption trigger event", "");

        // Special Terms
        specialTerms.push("One designated board observer seat for the investor");
        specialTerms.push("Quarterly unaudited and annual audited financial statements provided to investor");
        specialTerms.push("Right to maintain ownership percentage in future financings");
        specialTerms.push("Investors must participate in company sale if approved by majority holders");
        specialTerms.push("8% annual return on a non-cumulative dividend");
        specialTerms.push("Investors participate pro-rata in remaining proceeds");
        specialTerms.push("1x preference multiple in liquidation events");
        specialTerms.push("Weighted average anti-dilution protection in down rounds");
    }

    // Getters
    function getCompany() public view returns (string memory, string memory, address, string memory, string memory) {
        return (company.name, company.role, company.addr, company.email, company.entityType);