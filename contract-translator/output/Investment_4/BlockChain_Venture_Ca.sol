// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    address public company;
    address public investor;

    uint256 public constant PURCHASE_PRICE_PER_SHARE = 8000000 ether; // 8 million USD in wei equivalent
    uint256 public constant TOTAL_INVESTMENT_AMOUNT = 10000000 ether; // 10 million USD in wei equivalent

    uint256 public investmentTimestamp;
    uint256 public redemptionEventTimestamp;
    bool public sharesRedeemed;

    event InvestmentMade(address indexed investor, uint256 amount);
    event SharesRedeemed(uint256 redemptionAmount);
    event BoardSeatGranted(address indexed investor);
    event DividendPaid(address indexed investor, uint256 amount);

    modifier onlyCompany() {
        require(msg.sender == company, "Only company can call this function");
        _;
    }

    modifier onlyInvestor() {
        require(msg.sender == investor, "Only investor can call this function");
        _;
    }

    modifier investmentActive() {
        require(investmentTimestamp != 0, "Investment must be active");
        _;
    }

    modifier beforeRedemptionEvent() {
        require(block.timestamp < redemptionEventTimestamp, "Redemption event has passed");
        _;
    }

    constructor() {
        company = msg.sender;
        investor = address(0); // to be set when investor commits
        sharesRedeemed = false;
    }

    function setInvestor(address _investor) external onlyCompany {
        require(investor == address(0), "Investor has already been set");
        investor = _investor;
    }

    function makeInvestment() external payable onlyInvestor {
        require(msg.value == TOTAL_INVESTMENT_AMOUNT, "Incorrect investment amount");
        investmentTimestamp = block.timestamp;

        emit InvestmentMade(investor, msg.value);
    }

    function setRedemptionEvent(uint256 _timestamp) external onlyCompany {
        redemptionEventTimestamp = _timestamp;
    }

    function redeemShares() external onlyCompany investmentActive {
        require(block.timestamp >= redemptionEventTimestamp, "Redemption event not triggered");
        require(!sharesRedeemed, "Shares already redeemed");
        
        sharesRedeemed = true;

        // Here you would include logic to handle the redemption funds transfer
        emit SharesRedeemed(TOTAL_INVESTMENT_AMOUNT);
    }

    function distributeDividends(uint256 amount) external onlyCompany investmentActive {
        // Ensure proper handling of dividends distribution
        emit DividendPaid(investor, amount);
    }

    function grantBoardSeat() external onlyCompany {
        emit BoardSeatGranted(investor);
    }

    function getStatus() external view returns (string memory) {
        if (sharesRedeemed) {
            return "Shares have been redeemed.";
        } else {
            return "Investment is active.";
        }
    }

    // Additional functions for obligations and penalties could be added here
}