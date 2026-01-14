// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got ';'
  --> <stdin>:65:38:
   |
65 |             partyAddress: address(0),; // Missing address
   |                                      ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // State variables for parties
    struct Party {
        string name;
        string role;
        address partyAddress;
        string email;
        string entityType;
    }

    Party public lender;
    Party public borrower;

    // Financial terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    FinancialTerm[] public financialTerms;

    // Dates
    struct Date {
        string dateType;
        string value;
        uint256 dayOfMonth;
        string frequency;
    }

    Date[] public importantDates;

    // Obligations
    struct Obligation {
        string party; // "borrower" or "lender"
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Obligation[] public obligations;

    // Conditions
    struct Conditions {
        string[] defaultTriggers;
        string acceleration;
        string defaultInterestRate;
    }

    Conditions public conditions;

    // Events
    event LoanCreated(address indexed lender, address indexed borrower, uint256 amount);
    event ObligationFulfilled(string description);

    // Constructor to initialize the contract
    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            partyAddress: address(0),; // Missing address
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            partyAddress: address(0),; // Missing address
        });

        // Initializing financial terms with defaults for missing fields
        financialTerms.push(FinancialTerm({
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            purpose: "monthly payment",
            dueDate: "March 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            purpose: "origination fee",
            frequency: "one-time",
        }));

        importantDates.push(Date({
            value: "February 1, 2025",
        }));

        importantDates.push(Date({
            value: "March 1, 2025",
        }));

        obligations.push(Obligation({
            description: "maintain insurance on collateral at full value",
        }));

        conditions = Conditions({
            defaultTriggers: new string[](3),
            acceleration: "Entire remaining balance becomes immediately due",
            defaultInterestRate: "12% per annum on unpaid balance"
        });

        conditions.defaultTriggers[0] = "Payment 15+ days late";
        conditions.defaultTriggers[1] = "bankruptcy filing";
        conditions.defaultTriggers[2] = "breach of covenants";

        emit LoanCreated(lender.partyAddress, borrower.partyAddress, 500000);
    }

    // Getter functions
    function getLender() public view returns (string memory, string memory, address, string memory, string memory) {
        return (lender.name, lender.role, lender.partyAddress, lender.email, lender.entityType);