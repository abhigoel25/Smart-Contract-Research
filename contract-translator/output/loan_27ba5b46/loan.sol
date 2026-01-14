// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // Structs for parties, financial terms, and obligations
    struct Party {
        string name;
        string role;
        address addr;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
    }

    struct Date {
        string dateType;
        string value;
        uint256 dayOfMonth;
    }

    struct Obligation {
        string party;
        string description;
    }

    // State variables for the contract
    Party public lender;
    Party public borrower;

    FinancialTerm public loanTerm;
    FinancialTerm public monthlyPaymentTerm;
    FinancialTerm public originationFeeTerm;
    FinancialTerm public latePaymentFeeTerm;

    Date public startDate;
    Date public disbursementDate;
    Date public firstPaymentDueDate;
    Date public endDate;

    Obligation public obligation;

    // Events for tracking
    event LoanCreated(uint256 amount, string currency);
    event PaymentMade(uint256 amount);
    event ObligationFulfilled(string description);

    // Constructor to initialize contract
    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            role: "lender",
            addr: 0x0000000000000000000000000000000000000000,
            entityType: "company"
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            addr: 0x0000000000000000000000000000000000000000,
            entityType: "company"
        });

        loanTerm = FinancialTerm({
            amount: 500000,
            currency: "USD",
            purpose: "loan",
            frequency: "one-time"
        });

        monthlyPaymentTerm = FinancialTerm({
            amount: 9934,
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly"
        });

        originationFeeTerm = FinancialTerm({
            amount: 10000,
            currency: "USD",
            purpose: "origination fee",
            frequency: "one-time"
        });

        latePaymentFeeTerm = FinancialTerm({
            amount: 0,
            currency: "USD",
            purpose: "late payment fee",
            frequency: "one-time"
        });

        startDate = Date({
            dateType: "start",
            value: "2025-01-10",
            dayOfMonth: 10
        });

        disbursementDate = Date({
            dateType: "disbursement",
            value: "2025-02-01",
            dayOfMonth: 1
        });

        firstPaymentDueDate = Date({
            dateType: "first_payment_due",
            value: "2025-03-01",
            dayOfMonth: 1
        });

        endDate = Date({
            dateType: "end",
            value: "2030-01-10",
            dayOfMonth: 10
        });

        obligation = Obligation({
            party: "borrower",
            description: "maintain insurance on collateral at full value"
        });

        emit LoanCreated(loanTerm.amount, loanTerm.currency);
    }

    // Getters
    function getLender() public view returns (string memory, string memory, address, string memory) {
        return (lender.name, lender.role, lender.addr, lender.entityType);
    }

    function getBorrower() public view returns (string memory, string memory, address, string memory) {
        return (borrower.name, borrower.role, borrower.addr, borrower.entityType);
    }

    function getLoanTerm() public view returns (uint256, string memory, string memory, string memory) {
        return (loanTerm.amount, loanTerm.currency, loanTerm.purpose, loanTerm.frequency);
    }

    function getMonthlyPaymentTerm() public view returns (uint256, string memory, string memory, string memory) {
        return (monthlyPaymentTerm.amount, monthlyPaymentTerm.currency, monthlyPaymentTerm.purpose, monthlyPaymentTerm.frequency);
    }

    function getOriginationFeeTerm() public view returns (uint256, string memory, string memory, string memory) {
        return (originationFeeTerm.amount, originationFeeTerm.currency, originationFeeTerm.purpose, originationFeeTerm.frequency);
    }

    function getLatePaymentFeeTerm() public view returns (uint256, string memory, string memory, string memory) {
        return (latePaymentFeeTerm.amount, latePaymentFeeTerm.currency, latePaymentFeeTerm.purpose, latePaymentFeeTerm.frequency);
    }

    function getStartDate() public view returns (string memory, uint256) {
        return (startDate.value, startDate.dayOfMonth);
    }

    function getDisbursementDate() public view returns (string memory, uint256) {
        return (disbursementDate.value, disbursementDate.dayOfMonth);
    }

    function getFirstPaymentDueDate() public view returns (string memory, uint256) {
        return (firstPaymentDueDate.value, firstPaymentDueDate.dayOfMonth);
    }

    function getEndDate() public view returns (string memory, uint256) {
        return (endDate.value, endDate.dayOfMonth);
    }

    function getObligation() public view returns (string memory, string memory) {
        return (obligation.party, obligation.description);
    }

    // Function to make a payment
    function makePayment(uint256 amount) public {
        if (amount > 0) {
            // Logic for processing payment
            emit PaymentMade(amount);
        }
    }

    // Function to fulfill an obligation
    function fulfillObligation() public {
        // Logic to enforce obligation
        emit ObligationFulfilled(obligation.description);
    }
}