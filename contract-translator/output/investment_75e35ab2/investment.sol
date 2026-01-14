// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchase {
    // State variables
    address public companyAddress;
    address public investorAddress;
    uint256 public investmentAmount;
    uint256 public purchasePricePerShare;
    uint256 public startDate;
    uint256 public redemptionTriggerDate;

    // Obligations
    string public companyObligation;
    string public investorObligation;

    event InvestmentMade(address indexed investor, uint256 amount);
    event ObligationFulfilled(string obligation);

    // Constructor
    constructor() {
        // Company details
        companyAddress = address(0); // Missing address defaults to address(0)
        investorAddress = address(0); // Missing address defaults to address(0)

        // Financial Terms
        investmentAmount = 0; // Missing amount defaults to 0
        purchasePricePerShare = 0; // Missing amount defaults to 0

        // Dates
        startDate = 0; // Missing date defaults to 0
        redemptionTriggerDate = 0; // Missing date defaults to 0

        // Obligations
        companyObligation = "redeem shares if no qualified IPO by 2030"; // Default obligation
        investorObligation = "participate in company sale if approved by majority holders (drag-along rights)"; // Default obligation
    }

    // Getter functions
    function getCompanyAddress() external view returns (address) {
        return companyAddress;
    }

    function getInvestorAddress() external view returns (address) {
        return investorAddress;
    }

    function getInvestmentAmount() external view returns (uint256) {
        return investmentAmount;
    }

    function getPurchasePricePerShare() external view returns (uint256) {
        return purchasePricePerShare;
    }

    function getStartDate() external view returns (uint256) {
        return startDate;
    }

    function getRedemptionTriggerDate() external view returns (uint256) {
        return redemptionTriggerDate;
    }

    function getCompanyObligation() external view returns (string memory) {
        return companyObligation;
    }

    function getInvestorObligation() external view returns (string memory) {
        return investorObligation;
    }

    // Action functions
    function makeInvestment(uint256 amount) external {
        if (amount > 0) {
            investmentAmount += amount;
            emit InvestmentMade(msg.sender, amount);
        }
        // Gracefully handle no investment - no revert
    }

    function fulfillCompanyObligation() external {
        // This function could determine if the obligation is fulfilled
        emit ObligationFulfilled(companyObligation);
        // No requirement; proceeds even if the obligation status is unclear
    }

    function fulfillInvestorObligation() external {
        // This function could determine if the obligation is fulfilled
        emit ObligationFulfilled(investorObligation);
        // No requirement; proceeds even if the obligation status is unclear
    }

    // Function to set company and investor addresses (could be accessed by admin)
    function setAddresses(address _companyAddress, address _investorAddress) external {
        companyAddress = _companyAddress == address(0) ? address(0) : _companyAddress;
        investorAddress = _investorAddress == address(0) ? address(0) : _investorAddress;
    }

    // Function to set financial terms
    function setFinancialTerms(uint256 _investmentAmount, uint256 _purchasePricePerShare) external {
        investmentAmount = _investmentAmount > 0 ? _investmentAmount : 0;
        purchasePricePerShare = _purchasePricePerShare > 0 ? _purchasePricePerShare : 0;
    }

    // Function to set dates
    function setDates(uint256 _startDate, uint256 _redemptionTriggerDate) external {
        startDate = _startDate > 0 ? _startDate : 0;
        redemptionTriggerDate = _redemptionTriggerDate > 0 ? _redemptionTriggerDate : 0;
    }
}