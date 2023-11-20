---
key: addmod, mulmod
desc: 计算  (x + y) % k 和 (x*y) %k
---



```solidity
addmod(uint x, uint y, uint k) returns (uint)
```

计算 `(x + y) % k` 的值，其中加法的结果即使超过 `2**256` 也不会被截取. 从 0.5.0 版本开始会加入对 `k != 0` 的 assert（即会在此函数开头执行 `assert(k != 0);`)



```solidity
mulmod(uint x, uint y, uint k) returns (uint)
```

计算 `(x * y) % k` 的值， 其中乘法的结果即使超过 `2**256` 也不会被截取。从 0.5.0 版本开始会加入对 `k != 0` 的 assert（即会在此函数开头执行 `assert(k != 0);` )



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract MyContract{

    function addmodTest(uint256 x, uint256 y, uint256 k) public pure returns (uint256){
        return addmod(x,y, k);
    }
}

```



调用 `addmodTest(10,20,7)` 输出 2



## submod()

没有内置submod()函数,但可以这样写:

```solidity
pragma solidity ^0.8.0;

contract Example {
    function subMod(uint x, uint y, uint k) public pure returns (uint) {
        require(k != 0, "Modulus cannot be 0");

        if (x >= y) {
            return (x - y) % k;
        } else {
            // 防止负数的结果
            return (k + x - y) % k;
        }
    }
}
```





## 溢出与溢出保护

在编程中，溢出保护是一种机制，用于防止数值运算中的溢出错误。溢出是指当运算结果超出了数据类型所能表示的最大（或最小）范围时发生的情况。在没有溢出保护的情况下，这类溢出可能导致不可预测的结果，甚至可能导致安全漏洞。

### 溢出的类型

1. **整数溢出**：
   - **上溢（Overflow）**：当计算结果超过数据类型的最大值时发生。例如，在 `uint8` 类型中，值 `255 + 1` 会导致上溢。
   - **下溢（Underflow）**：当计算结果低于数据类型的最小值时发生。例如，在 `uint8` 类型中，值 `0 - 1` 会导致下溢。

### 溢出保护的重要性

- **数据完整性**：保护防止溢出确保数据保持完整和准确，防止由于意外溢出导致的数据损坏。
- **安全性**：在智能合约等敏感的程序中，溢出可能被恶意利用来攻击系统。溢出保护有助于增强程序的安全性。
- **可预测性**：防止溢出可以确保程序行为的可预测性和一致性。

### Solidity 中的溢出保护

<u>在 Solidity 版本 0.8.0 及之后的版本中，默认启用了算术运算的溢出和下溢保护。这意味着如果任何算术运算导致溢出，交易将被回滚，并抛出异常。这是一个重要的安全特性，因为它减少了智能合约中由于算术错误导致的风险。</u>

### 示例

在 Solidity 0.8.0 之前，开发者需要手动或使用第三方库（如 OpenZeppelin 的 SafeMath）来防止整数溢出。但从 0.8.0 版本开始，这样的保护已经内置在语言中：

```solidity
pragma solidity ^0.8.0;

contract SafeMathExample {
    function add(uint x, uint y) public pure returns (uint) {
        return x + y; // 安全，自动溢出检查
    }
}
```

在这个例子中，如果 `x + y` 导致溢出，合约将自动抛出异常，保证了运算的安全性。

