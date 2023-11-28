---
key: modifier
desc: 函数修饰符
---

修饰符（modifier）是一种用于修改智能合约函数行为的特殊声明。它们的主要特点和用途如下：

1. **代码重用**：
   - 修饰符允许您编写可重用的代码，可以附加到函数上，以避免代码重复。

2. **前置和后置条件**：
   - 常用于实现前置条件（比如权限检查）和后置条件（比如状态更新）。

3. **实现控制流**：
   - 可以用于控制函数执行的流程，例如，确保某个条件满足后才执行函数主体。

4. **`_`占位符**：
   - 在修饰符中，`_` 代表被修饰的函数的原始代码。修饰符中的代码可以在 `_` 之前或之后执行，从而实现不同的控制流。

5. **参数化**：
   - 修饰符可以接受参数，使得它们的行为更加灵活。

6. **组合使用**：
   - 一个函数可以使用多个修饰符，修饰符将按照声明的顺序执行。

通过使用修饰符，开发者能够更加高效和清晰地控制函数行为，尤其是在处理权限控制和验证逻辑时。

来自 https://solidity-by-example.org/function-modifier/

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FunctionModifier {
    // We will use these variables to demonstrate how to use
    // modifiers.
    address public owner;
    uint public x = 10;

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
    function changeOwner(address _newOwner) public onlyOwner validAddress(_newOwner){
        owner = _newOwner;
    }
}

```

```solidity
pragma solidity ^0.8.11;

contract Secure {
    mapping(address => uint) public balances;
    bool private locked;

    modifier noReentrancy() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public noReentrancy {
       // Checks-Effects-Interactions 模式
    
        uint balance = balances[msg.sender];
        // check
        require(balance > 0, "Insufficient balance");
				 // effects
        balances[msg.sender] = 0;
				// interactions
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
    }
}

```

