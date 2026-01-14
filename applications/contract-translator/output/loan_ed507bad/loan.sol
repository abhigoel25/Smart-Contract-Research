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
            role: "lender",
            addr: address(0), // Missing address in input
            email: "",
            entityType: "company"
        });
        
        // Borrower information
        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            addr: address(0), // Missing address in input
            email: "",
            entityType: "company"
        });

        // Financial terms initialization
        financialTerms.push(FinancialTerm({
            amount: 500000 ether,
            currency: "USD",
            purpose: "loan",
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 9934 ether,
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly",
            dueDate: "March 1, 2025"
        }));
        
        financialTerms.push(FinancialTerm({
            amount: 10000 ether,
            currency: "USD",
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: "" // Missing
        }));

        // Dates initialization
        importantDates.push(DateInfo({
            dateType: "contract date",
            value: "January 10, 2025",
            dayOfMonth: 10,
            frequency: "" // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "disbursement date",
            value: "February 1, 2025",
            dayOfMonth: 1,
            frequency: "" // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "first payment due",
            value: "March 1, 2025",
            dayOfMonth: 1,
            frequency: "" // Missing
        }));

        importantDates.push(DateInfo({
            dateType: "loan term end",
            value: "January 10, 2030",
            dayOfMonth: 0, // Missing
            frequency: "" // Missing
        }));

        // Obligations initialization
        obligations.push(Obligation({
            party: "borrower",
            description: "maintain insurance on collateral at full value",
            deadline: "", // Missing
            penaltyForBreach: "" // Missing
        }));

        obligations.push(Obligation({
            party: "borrower",
            description: "make timely loan payments as per schedule",
            deadline: "", // Missing
            penaltyForBreach: "5% late payment fee"
        }));
    }

    // Getter functions
    function getLender() public view returns (string memory, string memory, address, string memory, string memory) {
        return (lender.name, lender.role, lender.addr, lender.email, lender.entityType);
    }

    function getBorrower() public view returns (string memory, string memory, address, string memory, string memory) {
        return (borrower.name, borrower.role, borrower.addr, borrower.email, borrower.entityType);
    }

    function getFinancialTerm(uint256 index) public view returns (uint256, string memory, string memory, string memory, string memory) {
        if (index < financialTerms.length) {
            FinancialTerm memory term = financialTerms[index];
            return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
        }
        return (0, "", "", "", ""); // Return defaults if index is out of bounds
    }

    function getImportantDate(uint256 index) public view returns (string memory, string memory, uint256, string memory) {
        if (index < importantDates.length) {
            DateInfo memory date = importantDates[index];
            return (date.dateType, date.value, date.dayOfMonth, date.frequency);
        }
        return ("", "", 0, ""); // Return defaults if index is out of bounds
    }

    function getObligation(uint256 index) public view returns (string memory, string memory, string memory, string memory) {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            return (obligation.party, obligation.description, obligation.deadline, obligation.penaltyForBreach);
        }
        return ("", "", "", ""); // Return defaults if index is out of bounds
    }

    // Action function to make a payment
    function makePayment(uint256 amount, string memory purpose) public {
        if (amount > 0) {
            emit PaymentMade(amount, purpose, msg.sender);
        }
    }

    // Action for borrower to fulfill obligations
    function fulfillObligation(uint256 obligationIndex) public {
        if (obligationIndex < obligations.length) {
            // Logic for fulfilling obligation goes here
            // Simply logging for now
            emit PaymentMade(0, obligations[obligationIndex].description, msg.sender);
        }
    }
}