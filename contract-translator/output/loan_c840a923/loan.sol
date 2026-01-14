// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    // State variables
    address public lender;
    address public borrower;
    
    uint public loanAmount;
    uint public monthlyPaymentAmount;
    uint public originationFeeAmount;

    uint public startDate;
    uint public disbursementDate;
    uint public firstPaymentDueDate;
    uint public termEndDate;

    string public defaultTrigger;
    string public accelerationClause;
    string public defaultInterestRate;

    string[] public specialTerms;
    string[] public terminationConditions;
    
    // Events
    event LoanInitialized(
        address indexed lender,
        address indexed borrower,
        uint loanAmount,
        uint monthlyPaymentAmount,
        uint originationFeeAmount
    );

    // Constructor to initialize party information and financial terms
    constructor(
        string memory lenderName,
        string memory borrowerName,
        string memory lenderAddress,
        uint _loanAmount,
        uint _monthlyPaymentAmount,
        uint _originationFeeAmount,
        string[] memory _specialTerms,
        string[] memory _terminationConditions
    ) {
        lender = bytes(lenderAddress).length > 0 ? address(uint160(uint256(keccak256(abi.encodePacked(lenderAddress))))) : address(0);
        borrower = address(0); // Borrower address not specified, using address(0) as default
        
        loanAmount = _loanAmount > 0 ? _loanAmount : 0;
        monthlyPaymentAmount = _monthlyPaymentAmount > 0 ? _monthlyPaymentAmount : 0;
        originationFeeAmount = _originationFeeAmount > 0 ? _originationFeeAmount : 0;

        startDate = block.timestamp; // defaulting to current block time as start date
        disbursementDate = 0; // not specified
        firstPaymentDueDate = 0; // not specified
        termEndDate = 0; // not specified

        specialTerms = _specialTerms;
        terminationConditions = _terminationConditions;

        emit LoanInitialized(lender, borrower, loanAmount, monthlyPaymentAmount, originationFeeAmount);
    }

    // Getters for lender and borrower
    function getLender() public view returns (address) {
        return lender;
    }

    function getBorrower() public view returns (address) {
        return borrower;
    }

    // Getters for financial terms
    function getLoanAmount() public view returns (uint) {
        return loanAmount;
    }

    function getMonthlyPaymentAmount() public view returns (uint) {
        return monthlyPaymentAmount;
    }

    function getOriginationFeeAmount() public view returns (uint) {
        return originationFeeAmount;
    }

    // Getters for key dates
    function getStartDate() public view returns (uint) {
        return startDate;
    }

    function getDisbursementDate() public view returns (uint) {
        return disbursementDate;
    }

    function getFirstPaymentDueDate() public view returns (uint) {
        return firstPaymentDueDate;
    }

    function getTermEndDate() public view returns (uint) {
        return termEndDate;
    }

    // Obligations (Action functions)
    function maintainInsurance() public {
        // Implement maintaining insurance
        // No operation if borrower's obligations cannot be satisfied due to missing data
    }

    function prepayLoan() public {
        // Implement prepayment without penalty
        if (loanAmount > 0) {
            // Handle prepayment logic
        }
    }

    // Functions to manage conditions
    function setDefaultConditions(string memory triggers, string memory acceleration, string memory interestRate) public {
        defaultTrigger = bytes(triggers).length > 0 ? triggers : "";
        accelerationClause = bytes(acceleration).length > 0 ? acceleration : "";
        defaultInterestRate = bytes(interestRate).length > 0 ? interestRate : "";
    }

    function getDefaultConditions() public view returns (string memory, string memory, string memory) {
        return (defaultTrigger, accelerationClause, defaultInterestRate);
    }

    // Updating the disbursement and payment due dates
    function setDisbursementDate(uint _disbursementDate) public {
        disbursementDate = _disbursementDate; // Can be set by authorized roles
    }

    function setFirstPaymentDueDate(uint _firstPaymentDueDate) public {
        firstPaymentDueDate = _firstPaymentDueDate; // Can be set by authorized roles
    }

    function setTermEndDate(uint _termEndDate) public {
        termEndDate = _termEndDate; // Can be set by authorized roles
    }
}