// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SalesAndPurchaseAgreement {
    address public seller;
    address public buyer;

    uint256 public downPayment;
    uint256 public payment1;
    uint256 public payment2;
    uint256 public totalPurchasePrice;
    uint256 public deliveryCost;

    uint256 public agreementDate;
    uint256 public deliveryDate;
    
    enum State { Created, InProgress, Completed, Terminated }
    State public state;

    event PaymentMade(address indexed payer, uint256 amount);
    event GoodsDelivered(address indexed seller, uint256 quantity);
    event AgreementTerminated(address indexed party, string reason);

    struct Obligation {
        string party;
        string description;
        uint256 deadline;
        string penaltyForBreach;
    }

    Obligation[] public obligations;

    modifier onlySeller() {
        require(msg.sender == seller, "Only seller can call this function");
        _;
    }
    
    modifier onlyBuyer() {
        require(msg.sender == buyer, "Only buyer can call this function");
        _;
    }

    modifier inState(State _state) {
        require(state == _state, "Invalid state for this operation");
        _;
    }

    constructor(
        address _seller,
        address _buyer,
        uint256 _agreementDate,
        uint256 _deliveryDate
    ) {
        seller = _seller;
        buyer = _buyer;

        downPayment = 1275000 ether; // Assume a conversion from USD to a suitable token or currency
        payment1 = 1700000 ether;
        payment2 = 1275000 ether;
        totalPurchasePrice = 4250000 ether;
        deliveryCost = 50000 ether;

        agreementDate = _agreementDate;
        deliveryDate = _deliveryDate;

        obligations.push(Obligation("Seller", "Deliver goods and provide warranty", deliveryDate, "10% of undelivered goods value"));
        obligations.push(Obligation("Buyer", "Pay purchase price as outlined in payment terms", 0, "Contract may be terminated"));

        state = State.Created;
    }

    function makeDownPayment() external payable onlyBuyer inState(State.Created) {
        require(msg.value == downPayment, "Incorrect down payment amount");
        emit PaymentMade(msg.sender, msg.value);
    }

    function makePayment1() external payable onlyBuyer inState(State.InProgress) {
        require(msg.value == payment1, "Incorrect payment amount");
        emit PaymentMade(msg.sender, msg.value);
    }

    function makePayment2() external payable onlyBuyer inState(State.InProgress) {
        require(msg.value == payment2, "Incorrect payment amount");
        emit PaymentMade(msg.sender, msg.value);
    }

    function confirmDelivery(uint256 quantity) external onlySeller inState(State.InProgress) {
        // Implement delivery logic, e.g., transfer ownership of goods
        emit GoodsDelivered(msg.sender, quantity);
        state = State.Completed;
    }

    function terminateAgreement(string memory reason) external {
        require(msg.sender == seller || msg.sender == buyer, "Only involved parties can terminate the agreement");
        state = State.Terminated;
        emit AgreementTerminated(msg.sender, reason);
    }

    function isAgreementActive() public view returns (bool) {
        return state == State.Created || state == State.InProgress;
    }  
}