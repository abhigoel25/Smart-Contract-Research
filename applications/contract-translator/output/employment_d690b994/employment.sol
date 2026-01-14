// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    // Events declared at contract level
    event EmployerAssigned(address indexed employer);
    event EmployeeAssigned(address indexed employee);
    
    // State variables
    address public employer;
    address public employee;
    uint256 public salary;
    uint256 public performanceBonus;
    uint256 public stockOptions;
    
    string[] public employerObligations;
    string[] public employeeObligations;

    // Constructor for initialization
    constructor() {
        employer = 0x0000000000000000000000000000000000000001; // Example address
        employee = 0x0000000000000000000000000000000000000002; // Example address
        
        salary = 150000 * 1e18; // Set salary in wei
        performanceBonus = 25000 * 1e18; // Set bonus in wei
        stockOptions = 5000 * 1e18; // Set stock options in wei

        employerObligations.push("Provide full health insurance coverage and 401(k) with 5% employer match");
        employeeObligations.push("Serve as Senior Software Engineer, develop enterprise-level applications, mentor junior developers, and make architectural decisions");

        emit EmployerAssigned(employer);
        emit EmployeeAssigned(employee);
    }

    // Getter for employer address
    function getEmployer() external view returns (address) {
        return employer;
    }

    // Getter for employee address
    function getEmployee() external view returns (address) {
        return employee;
    }

    // Getter for salary
    function getSalary() external view returns (uint256) {
        return salary;
    }

    // Getter for performance bonus
    function getPerformanceBonus() external view returns (uint256) {
        return performanceBonus;
    }

    // Getter for stock options
    function getStockOptions() external view returns (uint256) {
        return stockOptions;
    }

    // Getter for employer obligations
    function getEmployerObligation(uint256 index) external view returns (string memory) {
        return employerObligations[index];
    }

    // Getter for employee obligations
    function getEmployeeObligation(uint256 index) external view returns (string memory) {
        return employeeObligations[index];
    }
}