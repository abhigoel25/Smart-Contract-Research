// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got ';'
  --> <stdin>:48:30:
   |
48 |             addr: address(0),; // Missing address in input
   |                              ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    struct Party {
        string name;
        string role;
        address addr; // Using address(0) for missing
        string email;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount; // Use 0 for missing
        string currency;
        string purpose;
        string frequency; // Return "" if missing
        string dueDate; // Return "" if missing
    }

    struct DateInfo {
        string dateType;
        string value; // Return "" if missing
        uint256 dayOfMonth; // Use 0 for missing
        string frequency; // Return "" if missing
    }

    struct Obligation {
        string party; // 'borrower' or 'lender'
        string description;
        string deadline; // Return "" if missing
        string penaltyForBreach; // Return "" if missing or use "" if not applicable
    }

    Party public lender;
    Party public borrower;

    FinancialTerm[] public financialTerms; // Dynamic array to store multiple financial terms
    DateInfo[] public importantDates; // Dynamic array to store important dates
    Obligation[] public obligations; // Dynamic array to store obligations

    event PaymentMade(uint256 amount, string purpose, address payer);

    constructor() {
        // Lender information
        lender = Party({
            name: "Capital Finance Group, LLC",
            addr: address(0),; // Missing address in input
        });

        // Borrower information
        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            addr: address(0),; // Missing address in input
        });

        // Financial terms initialization
        financialTerms.push(FinancialTerm({
            amount: 500000 ether,
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 9934 ether,
            purpose: "monthly payment",
            dueDate: "March 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 10000 ether,
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: ""; // Missing
        }));

        // Dates initialization
        importantDates.push(DateInfo({
            dateType: "contract date",
            value: "January 10, 2025",
            frequency: ""; // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "disbursement date",
            value: "February 1, 2025",
            frequency: ""; // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "first payment due",
            value: "March 1, 2025",
            frequency: ""; // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "loan term end",
            value: "January 10, 2030",
            dayOfMonth: 0,; // Missing
            frequency: ""; // Missing
        }));

        // Obligations initialization
        obligations.push(Obligation({
            description: "maintain insurance on collateral at full value",
            deadline: "",; // Missing
            penaltyForBreach: ""; // Missing
        }));

        obligations.push(Obligation({
            description: "make timely loan payments as per schedule",
            deadline: "",; // Missing
            penaltyForBreach: "5% late payment fee"
        }));
    }

    // Getter functions
    function getLender() public view returns (string memory, string memory, address, string memory, string memory) {
        return (lender.name, lender.role, lender.addr, lender.email, lender.entityType);