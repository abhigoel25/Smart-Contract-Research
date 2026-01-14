// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // Parties
    address public lender;
    address public borrower;

    // Financial Terms
    uint256 public loanAmount;
    uint256 public monthlyPaymentAmount;
    uint256 public originationFeeAmount;

    // Dates
    uint256 public startDate;
    uint256 public disbursementDate;
    uint256 public firstPaymentDueDate;

    // Obligations
    string public borrowerObligation;
    string public borrowerObligationPenalty;

    // Special Terms
    string[] public specialTerms;

    // Conditions
    string[] public defaultConditions;
    string public defaultAcceleration;
    uint256 public defaultInterestRate;

    // Events
    event LoanCreated(address lender, address borrower);
    event PaymentMade(uint256 amount);
    event ObligationChecked(string description);

    constructor() {
        lender = 0x0000000000000000000000000000000000000000; // address(0) for missing lender address
        borrower = 0x0000000000000000000000000000000000000000; // address(0) for missing borrower address
        
        loanAmount = 0; // Default to 0 if missing
        monthlyPaymentAmount = 0; // Default to 0 if missing
        originationFeeAmount = 0; // Default to 0 if missing

        startDate = 0; // Default to 0 if missing
        disbursementDate = 0; // Default to 0 if missing
        firstPaymentDueDate = 0; // Default to 0 if missing

        borrowerObligation = ""; // Default to empty string if missing
        borrowerObligationPenalty = ""; // Default to empty string if missing

        defaultInterestRate = 0; // Default to 0 if missing
        defaultAcceleration = ""; // Default to empty string if missing
    }

    // View functions (getters)
    function getLender() public view returns (address) {
        return lender;
    }

    function getBorrower() public view returns (address) {
        return borrower;
    }

    function getLoanAmount() public view returns (uint256) {
        return loanAmount > 0 ? loanAmount : 0;
    }

    function getMonthlyPaymentAmount() public view returns (uint256) {
        return monthlyPaymentAmount > 0 ? monthlyPaymentAmount : 0;
    }

    function getOriginationFeeAmount() public view returns (uint256) {
        return originationFeeAmount > 0 ? originationFeeAmount : 0;
    }

    function getStartDate() public view returns (uint256) {
        return startDate > 0 ? startDate : 0;
    }

    function getDisbursementDate() public view returns (uint256) {
        return disbursementDate > 0 ? disbursementDate : 0;
    }

    function getFirstPaymentDueDate() public view returns (uint256) {
        return firstPaymentDueDate > 0 ? firstPaymentDueDate : 0;
    }

    function getBorrowerObligation() public view returns (string memory) {
        return bytes(borrowerObligation).length > 0 ? borrowerObligation : "";
    }

    function getBorrowerObligationPenalty() public view returns (string memory) {
        return bytes(borrowerObligationPenalty).length > 0 ? borrowerObligationPenalty : "";
    }

    function getDefaultInterestRate() public view returns (uint256) {
        return defaultInterestRate > 0 ? defaultInterestRate : 0;
    }

    // Action functions
    function initializeAgreement(
        address _lender,
        address _borrower,
        uint256 _loanAmount,
        uint256 _monthlyPayment,
        uint256 _originationFee,
        uint256 _startDate,
        uint256 _disbursementDate,
        uint256 _firstPaymentDueDate,
        string memory _borrowerObligation,
        string memory _borrowerObligationPenalty,
        uint256 _defaultInterestRate,
        string memory _defaultAcceleration
    ) public {
        if (_lender != address(0)) {
            lender = _lender;
        }
        if (_borrower != address(0)) {
            borrower = _borrower;
        }
        if (_loanAmount > 0) {
            loanAmount = _loanAmount;
        }
        if (_monthlyPayment > 0) {
            monthlyPaymentAmount = _monthlyPayment;
        }
        if (_originationFee > 0) {
            originationFeeAmount = _originationFee;
        }
        if (_startDate > 0) {
            startDate = _startDate;
        }
        if (_disbursementDate > 0) {
            disbursementDate = _disbursementDate;
        }
        if (_firstPaymentDueDate > 0) {
            firstPaymentDueDate = _firstPaymentDueDate;
        }
        if (bytes(_borrowerObligation).length > 0) {
            borrowerObligation = _borrowerObligation;
        }
        if (bytes(_borrowerObligationPenalty).length > 0) {
            borrowerObligationPenalty = _borrowerObligationPenalty;
        }
        if (_defaultInterestRate > 0) {
            defaultInterestRate = _defaultInterestRate;
        }
        if (bytes(_defaultAcceleration).length > 0) {
            defaultAcceleration = _defaultAcceleration;
        }

        emit LoanCreated(lender, borrower);
    }

    function makePayment(uint256 amount) public {
        if (amount > 0) {
            // Logic to handle payment
            emit PaymentMade(amount);
        }
    }

    function checkObligation() public {
        // Logic to check borrower obligations
        emit ObligationChecked(borrowerObligation);
    }
}