// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    address public constant COMPANY = 0x1234567890abcdef1234567890abcdef12345678;  // Replace with actual company address
    address public constant INVESTOR = 0xabcdef1234567890abcdef1234567890abcdef12; // Replace with actual investor address

    uint256 public constant TOTAL_INVESTMENT_AMOUNT = 10_000_000 ether; // Total investment amount
    uint256 public constant PURCHASE_PRICE_PER_SHARE = 8 ether; // Price per share
    uint256 public constant TOTAL_SHARES = 1_250_000; // Total shares to be issued
    uint256 public constant PRE_MONEY_VALUATION = 30_000_000 ether; // Pre-money valuation
    uint256 public constant POST_MONEY_VALUATION = 40_000_000 ether; // Post-money valuation

    enum Obligation {
        Investor,
        Company
    }

    event InvestmentReceived(address indexed investor, uint256 amount);
    event SharesRedeemed(uint256 sharesRedeemed, uint256 totalAmount);
    event ObligationMet(Obligation obligation);
    event ContractTerminated();

    bool public isContractTerminated;

    modifier onlyCompany() {
        require(msg.sender == COMPANY, "Only company can call this.");
        _;
    }

    modifier onlyInvestor() {
        require(msg.sender == INVESTOR, "Only investor can call this.");
        _;
    }

    constructor() {
        isContractTerminated = false;
    }

    function invest() external payable onlyInvestor {
        require(msg.value == TOTAL_INVESTMENT_AMOUNT, "Incorrect investment amount.");
        // Logic to handle investment allocation
        emit InvestmentReceived(msg.sender, msg.value);
    }

    function companyRedeemShares() external onlyCompany {
        require(block.timestamp >= 1735680000, "Not eligible for redemption."); // January 1, 2030, in UNIX timestamp
        uint256 sharesRedeemed = TOTAL_SHARES; // Redeem all shares
        // Logic to handle shares redemption
        emit SharesRedeemed(sharesRedeemed, TOTAL_INVESTMENT_AMOUNT);
    }

    function meetObligation(Obligation obligation) external {
        if (obligation == Obligation.Investor) {
            // Logic for the investor's obligation
            emit ObligationMet(obligation);
        } else if (obligation == Obligation.Company) {
            // Logic for the company's obligation
            emit ObligationMet(obligation);
        }
    }

    function terminateContract() external onlyInvestor {
        isContractTerminated = true;
        emit ContractTerminated();
    }

    function isContractActive() external view returns (bool) {
        return !isContractTerminated;
    }
}