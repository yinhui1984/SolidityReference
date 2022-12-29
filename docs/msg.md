---
key: msg,sender,data,sig,value
desc: 消息
---

消息是指来自外部的函数调用或交易。每个智能合约函数在被调用时，都会接收一条消息

## 说明

### msg.sender

数据类型: `address payable`

msg.sender 表示当前函数调用的发送者,这个值在执行函数调用时自动设置，用于表示谁在调用当前函数

https://yinhui1984.github.io/solidity_tx_origin_msg_sender/



### msg.data

数据类型 `bytes`

完整的调用数据，它是一个不可修改的、非持久的区域，函数参数存储在该区域中，其行为主要类似于内存

### msg.sig

数据类型`bytes4`

Calldata的前四个字节（即函数标识符）

### msg.value

数据类型 `uint256`

随消息发送的 wei 的数量



### msg.gas (弃用)

使用**gasleft()**函数替代





## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "hardhat/console.sol";

contract MyContract{

    function add(uint256 a, uint256 b) public payable  returns (uint256 c){
        c = a + b;
        console.log(msg.sender);
        console.log(msg.value);
        console.logBytes4(msg.sig);
        console.logBytes(msg.data);
    }
}
```



调用`add(1, 2)`

日志输出:

```
0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
0
0x771602f7
0x771602f700000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002
```

