// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PartnershipAgreement {

    struct Party {
        string name;
        string role;
        address addr;
        bool isActive;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
    }

    struct Asset {
        string assetType;
        string description;
    }

    event PartnerAdded(string name, string role);
    event CapitalContributed(address indexed partner, uint256 amount);
    event ObligationAssigned(string indexed party, string description);

    address[] public partners;
    mapping(address => Party) public partyDetails;
    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;
    Asset[] public assets;

    modifier onlyPartners() {
        require(partyDetails[msg.sender].isActive, "Not a registered partner");
        _;
    }

    constructor(address[] memory _partners, string[] memory _names, string[] memory _roles) {
        require(_partners.length == _names.length && _partners.length == _roles.length, "Mismatched lengths");
        for (uint256 i = 0; i < _partners.length; i++) {
            partyDetails[_partners[i]] = Party(_names[i], _roles[i], _partners[i], true);
            partners.push(_partners[i]);
            emit PartnerAdded(_names[i], _roles[i]);
        }
    }

    function addFinancialTerm(uint256 amount, string memory currency, string memory purpose, string memory frequency) public onlyPartners {
        financialTerms.push(FinancialTerm(amount, currency, purpose, frequency));
    }

    function contributeCapital(uint256 index) public onlyPartners {
        require(index < financialTerms.length, "Invalid financial term index");
        uint256 amount = financialTerms[index].amount;
        // Implementing a mock contribution as actual transfer requires handling of an ERC20/ERC721 token                        
        emit CapitalContributed(msg.sender, amount);
    }

    function assignObligation(string memory party, string memory description) public onlyPartners {
        obligations.push(Obligation(party, description));
        emit ObligationAssigned(party, description);
    }

    function addAsset(string memory assetType, string memory description) public onlyPartners {
        assets.push(Asset(assetType, description));
    }

    function getPartners() public view returns (address[] memory) {
        return partners;
    }

    function getFinancialTerms() public view returns (FinancialTerm[] memory) {
        return financialTerms;
    }

    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }

    function getAssets() public view returns (Asset[] memory) {
        return assets;
    }

    function withdrawMembership() public onlyPartners {
        partyDetails[msg.sender].isActive = false;
    }

    // Additional functions for managing special terms and termination conditions can be added here
}