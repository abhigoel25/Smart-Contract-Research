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
            }
        }
        return ("", "", "", "");  // Default return if not found
    }

    function getFinancialTerm(uint256 index) public view returns (uint256 amount, string memory currency, string memory purpose) {
        if (index < financialTerms.length) {
            return (financialTerms[index].amount, financialTerms[index].currency, financialTerms[index].purpose);
        }
        return (0, "", "");  // Default return if index out of range
    }

    function getDate(uint256 index) public view returns (string memory dateType, string memory value) {
        if (index < dates.length) {
            return (dates[index].dateType, dates[index].value);
        }
        return ("", ""); // Default return if index out of range
    }

    function getAsset(uint256 index) public view returns (string memory assetType, string memory description, uint256 quantity, uint256 value) {
        if (index < assets.length) {
            return (assets[index].assetType, assets[index].description, assets[index].quantity, assets[index].value);
        }
        return ("", "", 0, 0); // Default return if index out of range
    }

    function getObligation(uint256 index) public view returns (string memory party, string memory description, string memory deadline) {
        if (index < obligations.length) {
            return (obligations[index].party, obligations[index].description, obligations[index].deadline);
        }
        return ("", "", ""); // Default return if index out of range
    }

    function executeInvestment(uint256 index) public {
        if (index < financialTerms.length && financialTerms[index].amount > 0) {
            emit InvestmentExecuted(financialTerms[index].amount, financialTerms[index].purpose);
        }
    }

    function fulfillObligation(uint256 index) public {
        if (index < obligations.length) {
            // Logic can be added here to fulfill obligation
        }
    }
}