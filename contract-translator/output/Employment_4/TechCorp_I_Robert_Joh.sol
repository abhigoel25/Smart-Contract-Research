// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {

    // Define parties
    struct Party {
        string name;
        string role;
        string entityType;
        string address;
    }

    Party public employer;
    Party public employee;

    // Define financial terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
    }

    FinancialTerm[] public financialTerms;

    // Define obligations
    struct Obligation {
        string party;
        string description;
    }

    Obligation[] public obligations;

    // Define special terms
    string[] public specialTerms;

    // Define termination conditions
    string[] public terminationConditions;

    // Event declarations
    event EmploymentTerminated(address indexed party, string reason);
    event PaymentReleased(address indexed to, uint256 amount, string currency);

    // Access control
    address public employerAddress;
    address public employeeAddress;

    modifier onlyEmployer() {
        require(msg.sender == employerAddress, "Caller is not the employer");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employeeAddress, "Caller is not the employee");
        _;
    }

    // Contract constructor
    constructor(
        address _employerAddress,
        address _employeeAddress
    ) {
        employer = Party({
            name: "TechCorp Industries, Inc.",
            role: "employer",
            entityType: "company",
            address: ""
        });
        employee = Party({
            name: "Robert Johnson",
            role: "employee",
            entityType: "individual",
            address: "456 Oak Avenue, San Francisco, CA 94102"
        });

        // Set addresses
        employerAddress = _employerAddress;
        employeeAddress = _employeeAddress;

        // Financial terms
        financialTerms.push(FinancialTerm(150000 * 1e18, "USD", "salary", "monthly"));
        financialTerms.push(FinancialTerm(25000 * 1e18, "USD", "performance bonus", "annual"));
        financialTerms.push(FinancialTerm(5 * 1e18, "options", "stock options", "vesting over 4 years with 1-year cliff"));
        
        // Obligations
        obligations.push(Obligation("employee", "serve as Senior Software Engineer, develop enterprise-level applications, mentor junior developers, and make architectural decisions"));
        obligations.push(Obligation("employer", "provide compensation, benefits including health insurance and retirement plan"));
        
        // Special terms
        specialTerms.push("Employee agrees to maintain confidentiality of all proprietary information.");
        specialTerms.push("Non-Compete Period: 12 months post-employment within 100-mile radius of headquarters");
        
        // Termination conditions
        terminationConditions.push("Either party may terminate with 30 days written notice");
        terminationConditions.push("Severance: 3 months base salary upon termination without cause");
        terminationConditions.push("Cause: Breach of confidentiality, gross negligence, or policy violation");
    }

    // Function to release payment
    function releasePayment(uint256 amount, string memory currency) public onlyEmployer {
        require(amount > 0, "Payment amount must be greater than zero");
        emit PaymentReleased(employeeAddress, amount, currency);
        // Logic to transfer payment can be added here
    }

    // Function to terminate employment
    function terminateEmployment(string memory reason) public {
        require(
            msg.sender == employerAddress || msg.sender == employeeAddress,
            "Only employer or employee can terminate"
        );
        emit EmploymentTerminated(msg.sender, reason);
        // Logic for termination can be added here
    }

    // View functions
    function getFinancialTerms() public view returns (FinancialTerm[] memory) {
        return financialTerms;
    }

    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }

    function getSpecialTerms() public view returns (string[] memory) {
        return specialTerms;
    }

    function getTerminationConditions() public view returns (string[] memory) {
        return terminationConditions;
    }
}