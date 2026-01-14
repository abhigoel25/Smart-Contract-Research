// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected ',' but got ';'
  --> <stdin>:53:61:
   |
53 |             addr: 0x0000000000000000000000000000000000000000; // Use address(0) for missing address
   |                                                             ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    struct Party {
        string name;
        string role;
        address addr; // Use 0 address if not provided
    }

    struct FinancialTerm {
        uint256 amount; // Use 0 if not provided
        string currency;
        string purpose;
        string frequency;
        string dueDate; // Use "" if not provided
    }

    struct DateInfo {
        string dateType;
        string value; // Use "" if not provided
        uint256 dayOfMonth; // Use 0 if not provided
        string frequency; // Use "" if not provided
    }

    struct Obligation {
        string party; // Represented by "borrower" or "lender"
        string description;
        string deadline;
        string penaltyForBreach; // Use "" if not provided
    }

    struct Condition {
        string[] defaultTriggers; // Use empty array if not provided
        string defaultInterestRate; // Use "" if not provided
    }

    Party public lender;
    Party public borrower;
    FinancialTerm[] public financialTerms;
    DateInfo[] public dates;
    Obligation[] public obligations;
    Condition public conditions;

    event LoanCreated(address indexed lender, address indexed borrower);
    event PaymentMade(uint256 amount);
    event ObligationFulfilled(string obligationDescription);

    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            addr: 0x0000000000000000000000000000000000000000; // Use address(0) for missing address
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            addr: 0x0000000000000000000000000000000000000000; // Use address(0) for missing address
        });

        // Financial terms
        financialTerms.push(FinancialTerm({
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: "at loan disbursement"
        }));

        financialTerms.push(FinancialTerm({
            purpose: "monthly payment",
            dueDate: "March 1, 2025"
        }));

        // Dates
        dates.push(DateInfo({
            value: "January 10, 2025",
            frequency: ""; // Use empty if not provided
        }));

        dates.push(DateInfo({
            value: "February 1, 2025",
            frequency: ""; // Use empty if not provided
        }));

        dates.push(DateInfo({
            value: "March 1, 2025",
        }));

        dates.push(DateInfo({
            value: "January 10, 2030",
        }));

        // Obligations
        obligations.push(Obligation({
            description: "repay the loan amount including interest",
            deadline: "monthly for 5 years",
            penaltyForBreach: "5% late payment fee; acceleration of entire remaining balance"
        }));

        obligations.push(Obligation({
            description: "maintain insurance on collateral at full value",
            penaltyForBreach: ""; // Use empty if not provided
        }));

        // Conditions
        conditions = Condition({
            defaultTriggers: new string[](0),; // Empty array as a default
            defaultInterestRate: "12% per annum on unpaid balance"
        });

        emit LoanCreated(lender.addr, borrower.addr);
    }

    // Getters
    function getLender() public view returns (string memory, string memory, address) {
        return (lender.name, lender.role, lender.addr);