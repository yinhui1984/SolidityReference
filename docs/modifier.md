---
key: modifier
desc: 函数修饰符
---



来自 https://solidity-by-example.org/function-modifier/

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FunctionModifier {
    // We will use these variables to demonstrate how to use
    // modifiers.
    address public owner;
    uint public x = 10;
    bool public locked;

    constructor() {
        // Set the transaction sender as the owner of the contract.
        owner = msg.sender;
    }

		//检查调用者是否是合同的所有者
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        //下划线是一个特殊的字符，只在函数修饰符内使用，
        //它告诉 Solidity 执行代码的其余部分。
        _;
    }

    // Modifiers can take inputs. This modifier checks that the
    // address passed in is not the zero address.
    modifier validAddress(address _addr) {
        require(_addr != address(0), "Not valid address");
        _;
    }
    
    //可以同时使用多个函数修饰符
    function changeOwner(address _newOwner) public onlyOwner validAddress(_newOwner) {
        owner = _newOwner;
    }

		//函数修饰符可以在一个函数之前 和/或 之后被调用。
		//这个函数修饰符可以防止一个函数在执行过程中被调用。
    modifier noReentrancy() {
        require(!locked, "No reentrancy");

        locked = true;
        _;
        locked = false;
    }

    function decrement(uint i) public noReentrancy {
        x -= i;

        if (i > 1) {
            decrement(i - 1);
        }
    }
}

```

