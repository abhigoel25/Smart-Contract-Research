// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    event InvestmentMade(address indexed investor, uint256 amount);
    event SharesRedeemed(address indexed company, uint256 amount);
    
    address public company;
    address public investor;
    
    uint256 public totalInvestment;
    uint256 public sharePrice;
    
    mapping(address => bool) public obligationsMet;

    constructor(address _company, address _investor, uint256 _totalInvestment, uint256 _sharePrice) {
        company = _company;
        investor = _investor;
        totalInvestment = _totalInvestment;
        sharePrice = _sharePrice;
    }

    function makeInvestment() external returns (bool) {
        require(msg.sender == investor, "Only investor can make an investment");
        emit InvestmentMade(investor, totalInvestment);
        return true;
    }
    
    function redeemShares() external returns (bool) {
        require(msg.sender == company, "Only company can redeem shares");
        obligationsMet[company] = true;
        emit SharesRedeemed(company, totalInvestment);
        return true;
    }

    function getTotalInvestment() external view returns (uint256) {
        return totalInvestment;
    }

    function getSharePrice() external view returns (uint256) {
        return sharePrice;
    }
}