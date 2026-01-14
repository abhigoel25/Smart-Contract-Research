// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    
    // Events
    event InvestmentMade(address indexed investor, uint256 amount);
    event SharesRedeemed(address indexed company, uint256 quantity);

    // State variables
    address public company;
    address public investor;
    uint256 public investmentAmount;
    uint256 public purchasePricePerShare;
    uint256 public sharesQuantity;
    bool public sharesRedeemed;

    // Constructor
    constructor(address _company, address _investor, uint256 _investmentAmount, uint256 _purchasePricePerShare) {
        company = _company;
        investor = _investor;
        investmentAmount = _investmentAmount;
        purchasePricePerShare = _purchasePricePerShare;
        sharesQuantity = 1250000; // Fixed quantity as per contract schema
        sharesRedeemed = false;
    }

    // Function to make an investment
    function makeInvestment() external {
        require(msg.sender == investor, "Only the investor can make the investment");
        emit InvestmentMade(investor, investmentAmount);
    }

    // Function to redeem shares
    function redeemShares(uint256 quantity) external {
        require(msg.sender == company, "Only the company can redeem shares");
        require(!sharesRedeemed, "Shares already redeemed");
        sharesRedeemed = true;
        emit SharesRedeemed(company, quantity);
    }

    // Getters
    function getCompany() external view returns (address) {
        return company;
    }

    function getInvestor() external view returns (address) {
        return investor;
    }

    function getInvestmentAmount() external view returns (uint256) {
        return investmentAmount;
    }

    function getPurchasePricePerShare() external view returns (uint256) {
        return purchasePricePerShare;
    }

    function getSharesQuantity() external view returns (uint256) {
        return sharesQuantity;
    }

    function isSharesRedeemed() external view returns (bool) {
        return sharesRedeemed;
    }
}