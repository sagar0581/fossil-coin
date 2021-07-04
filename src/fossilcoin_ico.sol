// Fossil Coin ICO

// Version of compiler
pragma solidity >=0.7.0 <0.9.0;

contract fossilcoin_ico {
    
    // Introducing the maximum number of Fossil Coins available for sale
    uint public max_fossil_coins = 1000000;
    
    // Introducing the USD to Fossil Coin conversion rate
    uint public usd_to_fossilcoin = 1000;
    
    // Introducing the total number of Fossil coins that have been bought by the investors
    uint public total_fossilcoins_bought = 0;
    
    // Mapping from the investor address to its equity in fossil coins and usd
    mapping(address => uint) equity_fossilcoins;
    
    mapping(address => uint) equity_usd;
    
    // Checking if an investor can buy Fossilcoins
    modifier can_buy_fossilcoins(uint usd_invested) {
        require(usd_invested * usd_to_fossilcoin <= max_fossil_coins - total_fossilcoins_bought);
        _;
    }
    
    // Getting the equity in Fossil Coins of an investor
    function equity_in_fossilcoin(address investor) external returns (uint) {
        return equity_fossilcoins[investor];
    }
    
    // Getting the equity in USD for an investor
    function equity_in_usd(address investor) external returns (uint) {
        return equity_usd[investor];
    }
    
    // Buying Fossil Coins
    function buy_fossilcoins(address investor, uint usd_invested) external 
    can_buy_fossilcoins(usd_invested) {
        uint fossilcoins_bought = usd_invested * usd_to_fossilcoin;
        equity_fossilcoins[investor] += fossilcoins_bought;
        equity_usd[investor] = equity_usd[investor] / 1000;
        total_fossilcoins_bought += fossilcoins_bought;
        
    }
    
    // Selling Fossil Coins
    function sell_fossilcoins(address investor, uint fossilcoins_to_sell) external {
        equity_fossilcoins[investor] -= fossilcoins_to_sell;
        equity_usd[investor] = equity_fossilcoins[investor] / 1000;
        total_fossilcoins_bought -= fossilcoins_to_sell;
    }
}

