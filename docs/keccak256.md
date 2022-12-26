---
key: keccak256
desc: 计算哈希值
---

```solidity
keccak256(bytes memory) returns (bytes32)
```

单词发音: https://forvo.com/word/keccak/

> 注意, 输入参数是`bytes`



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "hardhat/console.sol";

contract MyContract{

    function getHash(string calldata _input) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_input));
    }
}

```

