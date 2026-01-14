// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    event InvestmentMade(uint256 amount, address investor);
    event SharesRedeemed(address company);
    
    address public company;
    address public investor;
    uint256 public investmentAmount;
    uint256 public purchasePricePerShare;
    bool public sharesRedeemed;

    constructor(address _company, address _investor, uint256 _investmentAmount, uint256 _purchasePrice) {
        company = _company;
        investor = _investor;
        investmentAmount = _investmentAmount;
        purchasePricePerShare = _purchasePrice;
        sharesRedeemed = false;
    }

    function makeInvestment() public {
        require(msg.sender == investor, "Only the investor can make the investment.");
        emit InvestmentMade(investmentAmount, investor);
    }

    function redeemShares() public {
        require(msg.sender == company, "Only the company can redeem shares.");
        sharesRedeemed = true;
        emit SharesRedeemed(company);
    }

    function isSharesRedeemed() public view returns (bool) {
        return sharesRedeemed;
    }

    function getInvestmentDetails() public view returns (uint256, uint256) {
        return (investmentAmount, purchasePricePerShare);
    }
}