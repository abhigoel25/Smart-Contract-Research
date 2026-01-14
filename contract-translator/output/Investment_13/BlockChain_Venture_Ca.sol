// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    // State variables
    address public companyAddress;
    address public investorAddress;
    uint256 public purchasePricePerShare;
    uint256 public totalInvestmentAmount;
    uint256 public productDevelopmentAmount;
    uint256 public salesAndMarketingAmount;
    uint256 public operationsAndAdministrationAmount;
    uint256 public workingCapitalReserveAmount;
    uint256 public startDate;
    uint256 public redemptionTriggerDate;

    // Obligations
    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }
    Obligation public obligation;

    // Special terms
    string[] public specialTerms;
    string public antiDilutionCondition;

    // Events
    event InvestmentProcessed(string indexed purpose, uint256 amount);
    event SharesRedeemed(string indexed party, uint256 amount);

    constructor() {
        // Parties
        companyAddress = address(0); // default when missing
        investorAddress = address(0); // default when missing

        // Financial terms (use 0 for missing values)
        purchasePricePerShare = 8000000 * 10 ** 18; // Storing in wei
        totalInvestmentAmount = 10000000 * 10 ** 18; // Storing in wei
        productDevelopmentAmount = 4000000 * 10 ** 18; // Storing in wei
        salesAndMarketingAmount = 3500000 * 10 ** 18; // Storing in wei
        operationsAndAdministrationAmount = 1500000 * 10 ** 18; // Storing in wei
        workingCapitalReserveAmount = 1000000 * 10 ** 18; // Storing in wei
        
        // Dates (initialize to 0 if not provided)
        startDate = 1735689600; // UNIX timestamp for 2025-01-01
        redemptionTriggerDate = 1735689600; // UNIX timestamp for 2030-01-01

        // Set up obligations
        obligation = Obligation({
            party: "BlockChain Innovations Inc.",
            description: "Company must redeem shares if no qualified IPO by January 1, 2030",
            deadline: "12 months from redemption trigger event",
            penaltyForBreach: "Original purchase price plus accrued but unpaid dividends"
        });

        // Special terms and conditions
        specialTerms.push("One designated board observer seat for investor");
        specialTerms.push("Quarterly and annual financial statement rights");
        specialTerms.push("Pro-rata rights for future financings");
        specialTerms.push("Participation in company sale with majority approval");
        specialTerms.push("8% annual return non-cumulative dividend");
        specialTerms.push("Participating preferred investors participate pro-rata in remaining proceeds");

        antiDilutionCondition = "Weighted average anti-dilution protection in down rounds";
    }

    // Getters
    function getCompanyAddress() external view returns (address) {
        return companyAddress == address(0) ? address(0) : companyAddress;
    }

    function getInvestorAddress() external view returns (address) {
        return investorAddress == address(0) ? address(0) : investorAddress;
    }

    function getPurchasePricePerShare() external view returns (uint256) {
        return purchasePricePerShare > 0 ? purchasePricePerShare : 0;
    }

    function getTotalInvestmentAmount() external view returns (uint256) {
        return totalInvestmentAmount > 0 ? totalInvestmentAmount : 0;
    }

    function getProductDevelopmentAmount() external view returns (uint256) {
        return productDevelopmentAmount > 0 ? productDevelopmentAmount : 0;
    }

    function getSalesAndMarketingAmount() external view returns (uint256) {
        return salesAndMarketingAmount > 0 ? salesAndMarketingAmount : 0;
    }

    function getOperationsAndAdministrationAmount() external view returns (uint256) {
        return operationsAndAdministrationAmount > 0 ? operationsAndAdministrationAmount : 0;
    }

    function getWorkingCapitalReserveAmount() external view returns (uint256) {
        return workingCapitalReserveAmount > 0 ? workingCapitalReserveAmount : 0;
    }

    function getStartDate() external view returns (uint256) {
        return startDate == 0 ? 0 : startDate;
    }

    function getRedemptionTriggerDate() external view returns (uint256) {
        return redemptionTriggerDate == 0 ? 0 : redemptionTriggerDate;
    }

    function getObligation() external view returns (Obligation memory) {
        return obligation;
    }

    function getSpecialTerms() external view returns (string[] memory) {
        return specialTerms;
    }

    function getAntiDilutionCondition() external view returns (string memory) {
        return bytes(antiDilutionCondition).length > 0 ? antiDilutionCondition : "";
    }

    // Action Functions
    function processInvestment(string calldata purpose, uint256 amount) external {
        if (amount > 0) {
            emit InvestmentProcessed(purpose, amount);
        }
    }

    function redeemShares() external {
        // Using obligation data for redemption process
        if (keccak256(bytes(obligation.party)) != keccak256(bytes(""))) {
            emit SharesRedeemed(obligation.party, purchasePricePerShare);
        }
    }
}