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
            role: "company",
            addr: address(0), // placeholder for missing address
            entityType: "company"
        });

        investor = Party({
            name: "Venture Capital Fund VII, LP",
            role: "investor",
            addr: address(0), // placeholder for missing address
            entityType: "company"
        });

        totalInvestment = FinancialTerm({
            amount: 10000000,
            currency: "USD",
            purpose: "total investment amount",
            frequency: "one-time",
            dueDate: 0 // placeholder for missing due date
        });

        purchasePrice = FinancialTerm({
            amount: 8,
            currency: "USD",
            purpose: "purchase price per share",
            frequency: "one-time",
            dueDate: 0 // placeholder for missing due date
        });

        startDate = ContractDate({
            dateType: "start",
            value: "2025-01-01",
            dayOfMonth: 1,
            frequency: "" // placeholder for missing frequency
        });

        redemptionTriggerDate = ContractDate({
            dateType: "redemption_trigger",
            value: "2030-01-01",
            dayOfMonth: 1,
            frequency: "" // placeholder for missing frequency
        });

        seriesAStock = Asset({
            assetType: "shares",
            description: "Series A Preferred Stock",
            location: "", // placeholder for missing location
            quantity: 1250000,
            value: 0 // placeholder for missing value
        });

        redemptionObligation = Obligation({
            party: "Company",
            description: "Redeem shares if no qualified IPO by January 1, 2030",
            deadline: "12 months from redemption trigger event",
            penaltyForBreach: "" // placeholder for missing penalty
        });
    }

    // Getters
    function getCompany() public view returns (string memory, string memory, address, string memory) {
        return (company.name, company.role, company.addr, company.entityType);
    }

    function getInvestor() public view returns (string memory, string memory, address, string memory) {
        return (investor.name, investor.role, investor.addr, investor.entityType);
    }

    function getTotalInvestment() public view returns (uint256, string memory, string memory, string memory, uint256) {
        return (totalInvestment.amount, totalInvestment.currency, totalInvestment.purpose, totalInvestment.frequency, totalInvestment.dueDate);
    }

    function getPurchasePrice() public view returns (uint256, string memory, string memory, string memory, uint256) {
        return (purchasePrice.amount, purchasePrice.currency, purchasePrice.purpose, purchasePrice.frequency, purchasePrice.dueDate);
    }

    function getStartDate() public view returns (string memory, string memory, uint256, string memory) {
        return (startDate.dateType, startDate.value, startDate.dayOfMonth, startDate.frequency);
    }

    function getRedemptionTriggerDate() public view returns (string memory, string memory, uint256, string memory) {
        return (redemptionTriggerDate.dateType, redemptionTriggerDate.value, redemptionTriggerDate.dayOfMonth, redemptionTriggerDate.frequency);
    }

    function getSeriesAStock() public view returns (string memory, string memory, string memory, uint256, uint256) {
        return (seriesAStock.assetType, seriesAStock.description, seriesAStock.location, seriesAStock.quantity, seriesAStock.value);
    }

    function getRedemptionObligation() public view returns (string memory, string memory, string memory, string memory) {
        return (redemptionObligation.party, redemptionObligation.description, redemptionObligation.deadline, redemptionObligation.penaltyForBreach);
    }

    // Action functions
    function triggerInvestment() public {
        if (totalInvestment.amount > 0) {
            emit InvestmentTriggered(investor.addr, totalInvestment.amount);
        }
    }

    function redeemShares() public {
        if (block.timestamp >= parseDate(redemptionTriggerDate.value)) {
            emit SharesRedeemed(seriesAStock.quantity);
        }
    }

    // Helper function to parse date strings to timestamps (stub)
    function parseDate(string memory dateValue) internal pure returns (uint256) {
        // In a real implementation, this would convert date strings to timestamps.
        return 0; // Default for the stub
    }
}