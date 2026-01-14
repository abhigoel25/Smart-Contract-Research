// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {

    // Parties Involved
    address public company;
    address public investor;

    // Financial Terms
    uint256 public totalInvestmentAmount;
    uint256 public purchasePricePerShare;

    // Dates
    uint256 public investmentStartDate;
    uint256 public investmentEndDate;

    // Assets
    uint256 public shareQuantity;
    uint256 public assetValue;

    // Obligations
    struct Obligation {
        string description;
        uint256 deadline;  // Timestamp
    }

    mapping(address => Obligation) public obligations;

    // Special Terms & Conditions
    string[] public specialTerms;
    string public redemptionCondition;
    string public preferredStockCondition;

    // Event Declarations
    event InvestmentMade(address indexed investor, uint256 amount);
    event SharesRedeemed(address indexed company, uint256 amount);
    event ObligationMet(address indexed party);

    // Modifiers
    modifier onlyCompany() {
        require(msg.sender == company, "Not authorized: Only company can execute this.");
        _;
    }

    modifier onlyInvestor() {
        require(msg.sender == investor, "Not authorized: Only investor can execute this.");
        _;
    }

    constructor(
        address _company,
        address _investor,
        uint256 _totalInvestmentAmount,
        uint256 _purchasePricePerShare,
        uint256 _investmentStartDate,
        uint256 _investmentEndDate,
        uint256 _shareQuantity,
        uint256 _assetValue,
        string[] memory _specialTerms,
        string memory _redemptionCondition,
        string memory _preferredStockCondition
    ) {
        company = _company;
        investor = _investor;
        totalInvestmentAmount = _totalInvestmentAmount;
        purchasePricePerShare = _purchasePricePerShare;
        investmentStartDate = _investmentStartDate;
        investmentEndDate = _investmentEndDate;
        shareQuantity = _shareQuantity;
        assetValue = _assetValue;
        specialTerms = _specialTerms;
        redemptionCondition = _redemptionCondition;
        preferredStockCondition = _preferredStockCondition;
    }

    // Function to make investment
    function invest() external payable onlyInvestor {
        require(msg.value == totalInvestmentAmount, "Incorrect investment amount sent.");
        emit InvestmentMade(msg.sender, msg.value);
    }

    // Function for company to redeem shares
    function redeemShares() external onlyCompany {
        require(block.timestamp > investmentEndDate, "Cannot redeem shares before end date.");
        // Logic for redemption
        emit SharesRedeemed(company, shareQuantity);
    }

    // Function to set obligations
    function setObligation(address party, string memory description, uint256 deadline) external {
        if (party == company) {
            require(msg.sender == company, "Only company can set obligations.");
        } else if (party == investor) {
            require(msg.sender == investor, "Only investor can set obligations.");
        }
        obligations[party] = Obligation(description, deadline);
    }

    // Function for obligation management
    function meetObligation(address party) external {
        require(block.timestamp <= obligations[party].deadline, "Obligation deadline has passed.");
        emit ObligationMet(party);
        delete obligations[party];  // Remove obligation after met
    }

    // View functions for asset management
    function getSpecialTerms() external view returns (string[] memory) {
        return specialTerms;
    }
    
    function getObligationDetails(address party) external view returns (Obligation memory) {
        return obligations[party];
    }
}