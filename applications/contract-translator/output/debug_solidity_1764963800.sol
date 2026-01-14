// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:76:1:
   |
76 | 
   | ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    struct Party {
        string name;
        address addr;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate;
    }

    struct Date {
        string dateType;
        uint256 value;
        uint256 dayOfMonth;
    }

    struct Obligation {
        string party;
        string description;
        uint256 deadline;
        string penaltyForBreach;
    }

    struct Conditions {
        string[] defaultTriggers;
        string acceleration;
        string defaultInterestRate;
    }

    // State Variables
    Party public lender;
    Party public borrower;

    FinancialTerm[] public financialTerms;
    Date[] public dates;
    Obligation[] public obligations;
    Conditions public conditions;

    event LoanCreated(address indexed lender, address indexed borrower, uint256 amount);
    event PaymentMade(address indexed borrower, uint256 amount);
    event ObligationFulfilled(address indexed borrower, string description);

    constructor() {
        lender = Party("Capital Finance Group, LLC", address(0)); // address(0) for missing;
        borrower = Party("GreenTech Solutions, Inc.", address(0)); // address(0) for missing;

        financialTerms.push(FinancialTerm(500000 ether, "USD", "loan", "one-time", 1735756800)); // February 1, 2025
        financialTerms.push(FinancialTerm(9934 ether, "USD", "monthly payment", "monthly", 1737830400)); // March 1, 2025
        financialTerms.push(FinancialTerm(10000 ether, "USD", "origination fee", "one-time", 0)); // missing due_date handled

        dates.push(Date("contract_date", 1736582400, 10)); // January 10, 2025
        dates.push(Date("disbursement_date", 1735756800, 1)); // February 1, 2025
        dates.push(Date("first_payment_due", 1737830400, 1)); // March 1, 2025
        dates.push(Date("term_end", 1735699200, 0)); // February 1, 2030

        obligations.push(Obligation("Borrower", "maintain insurance on collateral at full value", 0, ""));

        conditions.defaultTriggers.push("Payment 15+ days late");
        conditions.defaultTriggers.push("bankruptcy filing");
        conditions.defaultTriggers.push("breach of covenants");
        conditions.acceleration = "Entire remaining balance becomes immediately due";
        conditions.defaultInterestRate = "12% per annum on unpaid balance";
    }

    // View functions
    function getLender() public view returns (string memory, address) {
        return (lender.name, lender.addr);