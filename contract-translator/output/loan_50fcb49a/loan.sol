// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    struct Party {
        string name;
        address addr; // stores address(0) if missing
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount; // stores 0 if missing
        string currency;
        string purpose;
        string frequency;
        string dueDate; // empty string if missing
    }

    struct DateDetail {
        string dateType;
        string value; // empty string if missing
        uint256 dayOfMonth; // store 0 if missing
    }

    struct Obligation {
        string party;
        string description;
        string deadline; // empty string if missing
        string penaltyForBreach; // empty string if missing
    }

    struct Condition {
        string[] defaultTriggers;
        string accelerationClause; // empty string if missing
        string defaultInterestRate; // empty string if missing
    }

    Party public lender;
    Party public borrower;
    FinancialTerm[] public financialTerms;
    DateDetail[] public dates;
    Obligation[] public obligations;
    Condition public conditions;

    event LoanAgreementCreated();
    event ObligationExecuted(string description);

    constructor() {
        // Initialize Parties with address(0) if missing
        lender = Party("Capital Finance Group, LLC", address(0), "company");
        borrower = Party("GreenTech Solutions, Inc.", address(0), "company");

        // Initialize Financial Terms
        financialTerms.push(FinancialTerm(500000 * 1e18, "USD", "loan", "one-time", ""));
        financialTerms.push(FinancialTerm(9934 * 1e18, "USD", "monthly payment", "monthly", "March 1, 2025"));
        financialTerms.push(FinancialTerm(10000 * 1e18, "USD", "origination fee", "one-time", ""));

        // Initialize Dates
        dates.push(DateDetail("loan_disbursement", "February 1, 2025", 1));
        dates.push(DateDetail("first_payment_due", "March 1, 2025", 1));
        dates.push(DateDetail("term_start", "January 10, 2025", 10));
        dates.push(DateDetail("loan_term_end", "January 10, 2030", 10));

        // Initialize Obligations
        obligations.push(Obligation("Borrower", "maintain insurance on collateral at full value", "", ""));
        obligations.push(Obligation("Borrower", "make monthly payments as per schedule", "monthly on due date", "Late Payment Fee: 5% of overdue amount"));
        
        // Initialize Conditions
        conditions.defaultTriggers = ["Payment 15+ days late", "bankruptcy filing", "breach of covenants"];
        conditions.accelerationClause = "Entire remaining balance becomes immediately due";
        conditions.defaultInterestRate = "12% per annum on unpaid balance";

        emit LoanAgreementCreated();
    }

    // Getters for parties
    function getLender() external view returns (string memory, address, string memory) {
        return (lender.name, lender.addr, lender.entityType);
    }

    function getBorrower() external view returns (string memory, address, string memory) {
        return (borrower.name, borrower.addr, borrower.entityType);
    }

    // Getters for financial terms
    function getFinancialTerm(uint256 index) external view returns (uint256, string memory, string memory, string memory, string memory) {
        if (index < financialTerms.length) {
            FinancialTerm memory term = financialTerms[index];
            return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
        }
        return (0, "", "", "", ""); // return defaults if index is out of range
    }

    // Getters for dates
    function getDateDetail(uint256 index) external view returns (string memory, string memory, uint256) {
        if (index < dates.length) {
            DateDetail memory dateDetail = dates[index];
            return (dateDetail.dateType, dateDetail.value, dateDetail.dayOfMonth);
        }
        return ("", "", 0); // return defaults if index is out of range
    }

    // Functions for obligations
    function executeObligation(uint256 index) external {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            emit ObligationExecuted(obligation.description);
            // Additional logic for obligation processing can be handled here
        }
    }

    // Optional functions that could process financial actions
    function makePayment(uint256 amount) external {
        // Only proceed if the amount is greater than 0
        if (amount > 0) {
            // Implement payment logic
        }
    }
}