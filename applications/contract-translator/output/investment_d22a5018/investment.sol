// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPurchaseAgreement {
    event InvestmentMade(address investor, uint256 amount);
    event SharesRedeemed(address company, uint256 quantity);

    address public company;
    address public investor;
    uint256 public investmentAmount;
    uint256 public purchasePricePerShare;
    uint256 public sharesQuantity;
    bool public sharesRedeemed;

    constructor() {
        company = 0x1234567890123456789012345678901234567890; // BlockChain Innovations Inc.
        investor = 0x0987654321098765432109876543210987654321; // Venture Capital Fund VII, LP
        investmentAmount = 10000000; // USD
        purchasePricePerShare = 8; // USD
        sharesQuantity = 1250000; // Quantity of shares
        sharesRedeemed = false;
    }

    function makeInvestment() external {
        investmentAmount = 10000000;
        emit InvestmentMade(investor, investmentAmount);
    }

    function redeemShares() external {
        require(!sharesRedeemed, "Shares already redeemed");
        sharesRedeemed = true;
        emit SharesRedeemed(company, sharesQuantity);
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

    function areSharesRedeemed() external view returns (bool) {
        return sharesRedeemed;
    }
}