---
key: addmod
desc: 计算  (x + y) % k
---



```solidity
addmod(uint x, uint y, uint k) returns (uint)
```





计算 `(x + y) % k` 的值，其中加法的结果即使超过 `2**256` 也不会被截取. 从 0.5.0 版本开始会加入对 `k != 0` 的 assert（即会在此函数开头执行 `assert(k != 0);`

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