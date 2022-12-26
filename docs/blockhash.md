---
key: blockhash
desc: 获取指定块的hash值
---

```solidity
blockhash(uint blockNumber) returns (bytes32)
```

获取给定区块的哈希值 - 只对最近的256个区块有效, 且不包含当前块(当前块还没算出来的)



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;


contract MyContract{

    function getBlockHash() public view returns (uint256, bytes32) {
        //没有合法值时返回 0x0000000000000...000000000000000
        //return (block.number, blockhash(block.number));
        
        return (block.number, blockhash(block.number - 1));
        
    }
}

```

> 使用remix运行上面的示例是, 如果选择的是非本地节点, 会报错 
>
> `errored: Key not found in database [hn]`