// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // Events
    event LoanCreated(uint amount, string currency, address borrower, address lender);
    event PaymentMade(uint amount, address payer);
    event ObligationFulfilled(address party);

    // Parties
    address public lender;
    address public borrower;

    // Financial terms
    uint public loanAmount;
    uint public monthlyPayment;
    uint public originationFee;
    uint public latePaymentFee;

    // Dates
    uint public loanStartDate;
    uint public disbursementDate;
    uint public firstPaymentDate;

    // Obligations
    string public borrowerObligation;
    
    // Conditions
    string[] public defaultTriggers;
    string public accelerationTerm;
    string public defaultInterestRate;

    constructor(
        address _lender, 
        address _borrower,
        uint _loanAmount,
        uint _monthlyPayment,
        uint _originationFee,
        uint _latePaymentFee,
        uint _loanStartDate,
        uint _disbursementDate,
        uint _firstPaymentDate,
        string memory _borrowerObligation,
        string[] memory _defaultTriggers,
        string memory _accelerationTerm,
        string memory _defaultInterestRate
    ) {
        lender = _lender != address(0) ? _lender : address(0);
        borrower = _borrower != address(0) ? _borrower : address(0);

        loanAmount = _loanAmount;
        monthlyPayment = _monthlyPayment;
        originationFee = _originationFee;
        latePaymentFee = _latePaymentFee;

        loanStartDate = _loanStartDate;
        disbursementDate = _disbursementDate;
        firstPaymentDate = _firstPaymentDate;

        borrowerObligation = bytes(_borrowerObligation).length > 0 ? _borrowerObligation : "";

        // Store default triggers safely
        for (uint i = 0; i < _defaultTriggers.length; i++) {
            defaultTriggers.push(_defaultTriggers[i]);
        }

        accelerationTerm = bytes(_accelerationTerm).length > 0 ? _accelerationTerm : "";
        defaultInterestRate = bytes(_defaultInterestRate).length > 0 ? _defaultInterestRate : "";

        emit LoanCreated(_loanAmount, "USD", _borrower, _lender);
    }

    // Getters
    function getLender() public view returns (address) {
        return lender != address(0) ? lender : address(0);
    }

    function getBorrower() public view returns (address) {
        return borrower != address(0) ? borrower : address(0);
    }

    function getLoanAmount() public view returns (uint) {
        return loanAmount > 0 ? loanAmount : 0;
    }

    function getMonthlyPayment() public view returns (uint) {
        return monthlyPayment > 0 ? monthlyPayment : 0;
    }

    function getOriginationFee() public view returns (uint) {
        return originationFee > 0 ? originationFee : 0;
    }

    function getLatePaymentFee() public view returns (uint) {
        return latePaymentFee > 0 ? latePaymentFee : 0;
    }

    function getLoanStartDate() public view returns (uint) {
        return loanStartDate > 0 ? loanStartDate : 0;
    }

    function getDisbursementDate() public view returns (uint) {
        return disbursementDate > 0 ? disbursementDate : 0;
    }

    function getFirstPaymentDate() public view returns (uint) {
        return firstPaymentDate > 0 ? firstPaymentDate : 0;
    }

    function getBorrowerObligation() public view returns (string memory) {
        return bytes(borrowerObligation).length > 0 ? borrowerObligation : "";
    }

    function getDefaultTriggers() public view returns (string[] memory) {
        return defaultTriggers;
    }

    function getAccelerationTerm() public view returns (string memory) {
        return bytes(accelerationTerm).length > 0 ? accelerationTerm : "";
    }

    function getDefaultInterestRate() public view returns (string memory) {
        return bytes(defaultInterestRate).length > 0 ? defaultInterestRate : "";
    }

    // Action functions
    function makePayment(uint amount) public {
        if (amount > 0) {
            emit PaymentMade(amount, msg.sender);
            // Additional logic for payment processing can go here
        }
    }

    function fulfillObligation() public {
        emit ObligationFulfilled(msg.sender);
        // Additional logic for obligation fulfillment can go here
    }
}