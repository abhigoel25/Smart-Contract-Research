// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:82:1:
   |
82 | 
   | ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    struct Party {
        string name;
        address wallet;
        string role;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    struct DateTerm {
        string dateType;
        string value;
        uint256 dayOfMonth;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    struct Condition {
        string[] defaultTriggers;
        string acceleration;
        string defaultInterestRate;
    }

    Party public lender;
    Party public borrower;

    FinancialTerm[] public financialTerms;
    DateTerm[] public dates;
    Obligation[] public obligations;
    Condition public conditions;

    event LoanCreated(address lender, address borrower);
    event PaymentProcessed(uint256 amount);

    constructor() {
        // Parties
        lender = Party("Capital Finance Group, LLC", address(0), "lender");
        borrower = Party("GreenTech Solutions, Inc.", address(0), "borrower");

        // Financial Terms
        financialTerms.push(FinancialTerm(500000 ether, "USD", "loan", "one-time", "February 1, 2025"));
        financialTerms.push(FinancialTerm(9934 ether, "USD", "monthly payment", "monthly", "March 1, 2025"));
        financialTerms.push(FinancialTerm(10000 ether, "USD", "origination fee", "one-time", ""));
        financialTerms.push(FinancialTerm(0, "USD", "late payment fee", "one-time", ""));
        financialTerms.push(FinancialTerm(0, "USD", "default interest", "annual", ""));

        // Dates
        dates.push(DateTerm("contract_date", "January 10, 2025", 10, ""));
        dates.push(DateTerm("disbursement_date", "February 1, 2025", 1, ""));
        dates.push(DateTerm("first_payment_due", "March 1, 2025", 1, ""));
        dates.push(DateTerm("loan_term_end", "January 10, 2030", 10, ""));

        // Obligations
        obligations.push(Obligation("borrower", "maintain insurance on collateral at full value", "", ""));

        // Conditions
        conditions.defaultTriggers = ["Payment 15+ days late", "bankruptcy filing", "breach of covenants"];
        conditions.acceleration = "Entire remaining balance becomes immediately due";
        conditions.defaultInterestRate = "12% per annum on unpaid balance";

        emit LoanCreated(lender.wallet, borrower.wallet);
    }

    // Getters for parties
    function getLender() public view returns (string memory, address) {
        return (lender.name, lender.wallet);