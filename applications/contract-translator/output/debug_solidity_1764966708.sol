// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Unexpected trailing comma.
  --> <stdin>:55:47:
   |
55 |             name: "Capital Finance Group, LLC",
   |                                               ^

Unexpected trailing comma.
  --> <stdin>:59:46:
   |
59 |             name: "GreenTech Solutions, Inc.",
   |                                              ^

Unexpected trailing comma.
  --> <stdin>:67:39:
   |
67 |             purpose: "monthly payment",
   |                                       ^

Unexpected trailing comma.
  --> <stdin>:81:32:
   |
81 |             value: "2025-01-10",
   |                                ^

Unexpected trailing comma.
  --> <stdin>:85:32:
   |
85 |             value: "2025-02-01",
   |                                ^

Unexpected trailing comma.
  --> <stdin>:89:32:
   |
89 |             value: "2025-03-01",
   |                                ^

Unexpected trailing comma.
  --> <stdin>:93:32:
   |
93 |             value: "2030-01-10",
   |                                ^

Expected primary expression.
   --> <stdin>:106:1:
    |
106 | 
    | ^
// This contract failed to compile after 3 fix attempts

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
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
        });

        loanTerm = FinancialTerm({
            frequency: "one-time"
        });

        monthlyPaymentTerm = FinancialTerm({
            purpose: "monthly payment",
        });

        originationFeeTerm = FinancialTerm({
            purpose: "origination fee",
            frequency: "one-time"
        });

        latePaymentFeeTerm = FinancialTerm({
            purpose: "late payment fee",
            frequency: "one-time"
        });

        startDate = Date({
            value: "2025-01-10",
        });

        disbursementDate = Date({
            value: "2025-02-01",
        });

        firstPaymentDueDate = Date({
            value: "2025-03-01",
        });

        endDate = Date({
            value: "2030-01-10",
        });

        obligation = Obligation({
            description: "maintain insurance on collateral at full value"
        });

        emit LoanCreated(loanTerm.amount, loanTerm.currency);
    }

    // Getters
    function getLender() public view returns (string memory, string memory, address, string memory) {
        return (lender.name, lender.role, lender.addr, lender.entityType);