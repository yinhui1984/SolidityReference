---
key: shadowing
desc: 掩盖
---

在 Solidity 中，"Shadowing Inherited State Variables" 指的是在一个合约中声明一个与继承自父合约的状态变量同名的变量，并且在这个合约中使用这个变量时，会忽略父合约中的状态变量，而是使用这个合约中的变量。

假设有一个合约 A，其中有一个状态变量 "x"。如果另一个合约 B 继承自 A，并在 B 中声明一个同名的变量 "x"，那么在 B 中访问 "x" 变量时，将忽略 A 中的 "x" 变量，而是使用 B 中的 "x" 变量。

>Shadowing 在0.6版本后被禁用了, 也就是说在0.6版本前可被利用

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract A {
    string public name = "Contract A";

    function getName() public view returns (string memory) {
        return name;
    }
}

// !!!! 
// Shadowing is disallowed in Solidity 0.6
// This will not compile
// contract B is A {
//     string public name = "Contract B";
// }

contract C is A {
    // This is the correct way to override inherited state variables.
    constructor() {
        name = "Contract C";
    }

    // C.getName returns "Contract C"
}

```

