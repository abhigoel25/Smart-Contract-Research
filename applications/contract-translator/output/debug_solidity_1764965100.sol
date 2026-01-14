// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:71:1:
   |
71 | 
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
        string due_date;
    }

    struct Date {
        string date_type;
        string value;
        uint256 day_of_month;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penalty_for_breach;
    }

    Party public lender;
    Party public borrower;

    FinancialTerm[] public financialTerms;

    Date[] public dates;

    Obligation[] public obligations;

    event LoanCreated(address lender, address borrower, uint256 loanAmount);
    event PaymentMade(address borrower, uint256 amount);

    constructor() {
        lender = Party("Capital Finance Group, LLC", 0x5555555555555555555555555555555555555555); // Placeholder address, use accurate one;
        borrower = Party("GreenTech Solutions, Inc.", address(0)); // address(0) since missing;

        // Initialize financial terms
        financialTerms.push(FinancialTerm(500000, "USD", "loan", "one-time", "February 1, 2025"));
        financialTerms.push(FinancialTerm(9934, "USD", "monthly payment", "monthly", "March 1, 2025"));
        financialTerms.push(FinancialTerm(10000, "USD", "origination fee", "one-time", ""));
        financialTerms.push(FinancialTerm(0, "USD", "late payment fee", "per occurrence", ""));

        // Initialize dates
        dates.push(Date("loan_disbursement", "February 1, 2025", 1, ""));
        dates.push(Date("first_payment_due", "March 1, 2025", 1, "monthly"));
        dates.push(Date("contract_start", "January 10, 2025", 10, ""));

        // Initialize obligations
        obligations.push(Obligation("borrower", "maintain insurance on collateral at full value", "", ""));
        obligations.push(Obligation("borrower", "payments due monthly as per repayment schedule", "monthly starting March 1, 2025", "5% late payment fee on overdue amount"));
        obligations.push(Obligation("lender", "provide loan amount on disbursement date", "February 1, 2025", ""));

        emit LoanCreated(lender.addr, borrower.addr, financialTerms[0].amount);
    }

    // Getters for Parties
    function getLender() public view returns (string memory name, address addr) {
        return (lender.name, lender.addr);