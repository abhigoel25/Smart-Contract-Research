// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:35:1:
   |
35 | 
   | ^
// This contract failed to compile

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    event InvestmentMade(address indexed investor, uint256 amount);
    event SharesRedeemed(address indexed company, uint256 shares);
    
    address public companyAddress;
    address public investorAddress;
    uint256 public totalInvestment;
    uint256 public purchasePricePerShare;
    uint256 public totalShares;
    uint256 public redemptionDeadline;
    
    constructor(address _companyAddress, address _investorAddress, uint256 _totalInvestment, uint256 _purchasePricePerShare, uint256 _totalShares, uint256 _redemptionDeadline) {
        companyAddress = _companyAddress;
        investorAddress = _investorAddress;
        totalInvestment = _totalInvestment;
        purchasePricePerShare = _purchasePricePerShare;
        totalShares = _totalShares;
        redemptionDeadline = _redemptionDeadline;
    }

    function makeInvestment() public {
        emit InvestmentMade(investorAddress, totalInvestment);
    }
    
    function redeemShares() public {
        require(block.timestamp >= redemptionDeadline, "Redemption deadline not reached");
        emit SharesRedeemed(companyAddress, totalShares);
    }

    function getInvestmentDetails() public view returns (address, address, uint256, uint256, uint256, uint256) {
        return (companyAddress, investorAddress, totalInvestment, purchasePricePerShare, totalShares, redemptionDeadline);