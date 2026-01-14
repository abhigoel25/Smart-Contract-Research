// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ServiceAgreement {
    address public serviceProvider;
    address public client;

    struct FinancialTerm {
        uint256 amount; // in USD with 2 decimal points (e.g., 15000 means $150.00)
        string currency;
        string purpose; // e.g., monthly fee, setup fee
    }

    struct Obligation {
        string description;
        string penaltyForBreach;
    }

    struct Term {
        uint256 startDate;
        uint256 endDate;
    }

    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;
    Term public term;

    event PaymentMade(address indexed payer, uint256 amount, string purpose);
    event ObligationFulfilled(address indexed party, string description);
    event AgreementTerminated(address indexed party, string reason);

    constructor() {
        serviceProvider = msg.sender; // Set the deployer as the service provider
        client = 0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48; // Example client address, to be changed
        term.startDate = 1735689600; // March 1, 2025
        term.endDate = 1748271600;   // March 1, 2026

        financialTerms.push(FinancialTerm(15000 * 1e18, "USD", "monthly fee")); // using 18 decimals for compatibility
        financialTerms.push(FinancialTerm(5000 * 1e18, "USD", "setup fee"));
        financialTerms.push(FinancialTerm(3, "percent", "annual increase for renewals"));
        
        obligations.push(Obligation("Provide 24/7 Monitoring, Technical Support, and Monthly Optimization", "10% monthly credit for each hour below 99.95% uptime guarantee"));
        obligations.push(Obligation("Pay agreed fees on time as specified", "1.5% per month on overdue amounts"));
    }

    modifier onlyClient() {
        require(msg.sender == client, "Only client can call this function");
        _;
    }

    modifier onlyServiceProvider() {
        require(msg.sender == serviceProvider, "Only service provider can call this function");
        _;
    }

    function paySetupFee() external payable onlyClient {
        require(msg.value == financialTerms[1].amount, "Incorrect setup fee amount");
        emit PaymentMade(msg.sender, msg.value, financialTerms[1].purpose);
    }

    function payMonthlyFee() external payable onlyClient {
        require(block.timestamp % 30 days < 1 days, "Fees can only be paid on due date");
        require(msg.value == financialTerms[0].amount, "Incorrect monthly fee amount");
        emit PaymentMade(msg.sender, msg.value, financialTerms[0].purpose);
    }

    function fulfillObligation(uint256 obligationIndex) external {
        require(obligationIndex < obligations.length, "Invalid obligation index");
        emit ObligationFulfilled(msg.sender, obligations[obligationIndex].description);
    }

    function terminateAgreement(string memory reason) external {
        require(msg.sender == serviceProvider || msg.sender == client, "Only involved parties can terminate");
        emit AgreementTerminated(msg.sender, reason);
    }

    function getFinancialTerms() external view returns (FinancialTerm[] memory) {
        return financialTerms;
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function getTerm() external view returns (Term memory) {
        return term;
    }
}