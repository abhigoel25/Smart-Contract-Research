// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SalesAgreement {
    address public seller;
    address public buyer;
    
    enum PaymentStatus { PENDING, COMPLETED, TERMINATED }
    PaymentStatus public paymentStatus;

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        bool isPaid;
    }
    
    struct Obligation {
        string description;
        string deadline;
        bool isFulfilled;
    }

    FinancialTerm[3] public financialTerms;
    Obligation[2] public obligations;

    event PaymentReceived(address indexed from, uint256 amount, string purpose);
    event ObligationFulfilled(address indexed party, string description);
    event AgreementTerminated(string reason);

    modifier onlyBuyer() {
        require(msg.sender == buyer, "Only buyer can call this function");
        _;
    }

    modifier onlySeller() {
        require(msg.sender == seller, "Only seller can call this function");
        _;
    }

    constructor(address _buyer) {
        seller = msg.sender;
        buyer = _buyer;
        paymentStatus = PaymentStatus.PENDING;

        // Initialize financial terms
        financialTerms[0] = FinancialTerm(1275000 ether, "USD", "down payment", false);
        financialTerms[1] = FinancialTerm(1700000 ether, "USD", "payment upon production completion", false);
        financialTerms[2] = FinancialTerm(1275000 ether, "USD", "payment upon delivery and inspection", false);

        // Initialize obligations
        obligations[0] = Obligation("Deliver goods", "January 31, 2025", false);
        obligations[1] = Obligation("Inspect goods within 15 days", "15 days post-delivery", false);
    }

    function payDownPayment() external payable onlyBuyer {
        require(!financialTerms[0].isPaid, "Down payment already made");
        // Payment logic here (e.g., transfer from buyer to seller)
        require(msg.value == financialTerms[0].amount, "Incorrect payment amount");
        
        financialTerms[0].isPaid = true;
        emit PaymentReceived(msg.sender, msg.value, financialTerms[0].purpose);
    }

    function confirmProductionCompletion() external onlySeller {
        require(financialTerms[0].isPaid, "Down payment must be paid first");
        require(!financialTerms[1].isPaid, "Payment already made");

        // Logic to confirm production
        financialTerms[1].isPaid = true;
        emit PaymentReceived(seller, financialTerms[1].amount, financialTerms[1].purpose);
    }

    function finalizeDelivery() external onlySeller {
        require(financialTerms[1].isPaid, "Production payment must be paid first");
        require(!financialTerms[2].isPaid, "Delivery payment already made");

        // Logic for delivery after inspection
        financialTerms[2].isPaid = true;
        emit PaymentReceived(seller, financialTerms[2].amount, financialTerms[2].purpose);
    }

    function fulfillObligation(uint256 obligationIndex) external {
        require(obligationIndex < obligations.length, "Invalid obligation index");
        if (msg.sender == seller) {
            require(keccak256(abi.encodePacked(obligations[obligationIndex].description)) == keccak256("Deliver goods"), "Invalid obligation for seller");
        } else if (msg.sender == buyer) {
            require(keccak256(abi.encodePacked(obligations[obligationIndex].description)) == keccak256("Inspect goods within 15 days"), "Invalid obligation for buyer");
        } else {
            revert("Caller is neither seller nor buyer");
        }
        
        obligations[obligationIndex].isFulfilled = true;
        emit ObligationFulfilled(msg.sender, obligations[obligationIndex].description);
    }

    function terminateAgreement(string memory reason) external {
        require(msg.sender == seller || msg.sender == buyer, "Only parties can terminate the agreement");
        paymentStatus = PaymentStatus.TERMINATED;
        emit AgreementTerminated(reason);
    }

    function getFinancialTerms() external view returns (FinancialTerm[3] memory) {
        return financialTerms;
    }
    
    function getObligations() external view returns (Obligation[2] memory) {
        return obligations;
    }
}