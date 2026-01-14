// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:80:1:
   |
80 | 
   | ^
// This contract failed to compile after 3 fix attempts

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