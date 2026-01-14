// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    struct Party {
        string name;
        string role;
        address addr;
    }

    struct FinancialTerm {
        uint amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    struct Date {
        string dateType;
        string value;
        uint dayOfMonth;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Party public lender;
    Party public borrower;
    
    FinancialTerm[] public financialTerms;
    Date[] public importantDates;
    Obligation[] public obligations;

    event LoanCreated(string indexed title, address indexed lenderAddr, address indexed borrowerAddr);
    
    constructor() {
        // Initialize Lender
        lender.name = "Capital Finance Group, LLC";
        lender.role = "lender";
        lender.addr = 0x0000000000000000000000000000000000000000; // Address not provided
        
        // Initialize Borrower
        borrower.name = "GreenTech Solutions, Inc.";
        borrower.role = "borrower";
        borrower.addr = 0x0000000000000000000000000000000000000000; // Address not provided

        // Define Financial Terms
        financialTerms.push(FinancialTerm(500000 * 1e18, "USD", "loan", "one-time", "February 1, 2025"));
        financialTerms.push(FinancialTerm(9934 * 1e18, "USD", "monthly payment", "monthly", "March 1, 2025"));
        financialTerms.push(FinancialTerm(10000 * 1e18, "USD", "origination fee", "one-time", ""));
        
        // Define Important Dates
        importantDates.push(Date("loan agreement date", "January 10, 2025", 10));
        importantDates.push(Date("disbursement date", "February 1, 2025", 1));
        importantDates.push(Date("first payment due", "March 1, 2025", 1));
        importantDates.push(Date("loan term end", "January 10, 2030", 10));

        // Define Obligations
        obligations.push(Obligation("Borrower", "Maintain insurance on collateral at full value", "", ""));
        obligations.push(Obligation("Lender", "Hold first security interest in equipment", "", ""));
        
        emit LoanCreated("Promissory Note and Loan Agreement", lender.addr, borrower.addr);
    }

    // View Functions
    function getLender() public view returns (string memory, string memory, address) {
        return (lender.name, lender.role, lender.addr);
    }
    
    function getBorrower() public view returns (string memory, string memory, address) {
        return (borrower.name, borrower.role, borrower.addr);
    }

    function getFinancialTerm(uint index) public view returns (uint, string memory, string memory, string memory, string memory) {
        if (index < financialTerms.length) {
            FinancialTerm memory term = financialTerms[index];
            return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
        } else {
            return (0, "", "", "", ""); // Default returns
        }
    }

    function getImportantDate(uint index) public view returns (string memory, string memory, uint) {
        if (index < importantDates.length) {
            Date memory dateInfo = importantDates[index];
            return (dateInfo.dateType, dateInfo.value, dateInfo.dayOfMonth);
        } else {
            return ("", "", 0); // Default returns
        }
    }

    function getObligation(uint index) public view returns (string memory, string memory, string memory, string memory) {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            return (obligation.party, obligation.description, obligation.deadline, obligation.penaltyForBreach);
        } else {
            return ("", "", "", ""); // Default returns
        }
    }

    // Action Functions
    function maintainInsuranceOnCollateral() public {
        if (keccak256(abi.encodePacked(obligations[0].description)) != keccak256(abi.encodePacked(""))) {
            // Logic for maintaining insurance on collateral
        }
    }

    function holdFirstSecurityInterest() public {
        if (keccak256(abi.encodePacked(obligations[1].description)) != keccak256(abi.encodePacked(""))) {
            // Logic for holding security interest
        }
    }

    function prepayLoan(uint amount) public {
        if (amount > 0) {
            // Logic for prepayment
        }
    }

    // Add more action functions as per obligations if needed
    // Ensure they safely handle missing data
}