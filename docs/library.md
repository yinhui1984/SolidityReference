---
key: library
desc: 库
---

在Solidity中，当我们提到库（libraries）的功能是“受限的”相比于合约（contracts），这主要是指以下几个方面的限制：

1. **无状态存储**：
   - 库不能拥有自己的状态变量。这意味着它们不能像合约那样存储和维护自己的数据。库的函数只能访问调用它们的合约中的数据。
2. **无法持有以太币（Ether）**：
   - 库不能持有或直接管理以太币。它们没有与自身相关联的以太币余额，也不能通过诸如`payable`函数接收以太币。库可以包含实现转账的函数，但这些操作是在调用合约的上下文中执行的。
3. **受限的可见性和类型**：
   - 库通常只包含`internal`或`public`函数。`internal`类型的库函数会被嵌入到调用它们的合约中，而`public`函数需要独立部署的库。
   - 库不支持某些类型的成员，如构造函数、回退（fallback）函数或接收（receive）函数。
4. **部署和链接机制**：
   - 当库包含`public`或`external`函数时，它们需要被单独部署到区块链上。合约在部署之前必须将这些库与自身进行链接，这是一个编译和部署过程的一部分。
   - 这种部署和链接机制与合约不同，因为合约是作为独立的实体部署的。
5. **使用模式**：
   - 库主要用于提供可重用的代码和工具函数，而不是作为数据存储或独立的应用实体。合约则更为全面和自足，可以包含逻辑、数据存储和以太币管理等功能



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

library Math {
    function sqrt(uint y) internal pure returns (uint z) {
        if (y > 3) {
            z = y;
            uint x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
        // else z = 0 (default value)
    }
}

contract TestMath {
    function testSquareRoot(uint x) public pure returns (uint) {
        return Math.sqrt(x);
    }
}

// Array function to delete element at index and re-organize the array
// so that there are no gaps between the elements.
library Array {
    function remove(uint[] storage arr, uint index) public {
        // Move the last element into the place to delete
        require(arr.length > 0, "Can't remove from empty array");
        arr[index] = arr[arr.length - 1];
        arr.pop();
    }
}

contract TestArray {
    using Array for uint[];

    uint[] public arr;

    function testArrayRemove() public {
        for (uint i = 0; i < 3; i++) {
            arr.push(i);
        }

        arr.remove(1);

        assert(arr.length == 2);
        assert(arr[0] == 0);
        assert(arr[1] == 2);
    }
}

```

更多的, 参考这篇文章:

https://cryptomarketpool.com/libraries-in-solidity/



