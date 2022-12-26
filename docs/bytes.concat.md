---
key: bytes.concat
desc: 连接2个或多个字节数组
---

```solidity
bytes.concat(bytes1, bytes2, ..., bytesN) returns (bytes memory)
```



## 描述

用于连接两个或多个字节数组（`bytes` 类型）并返回一个新的字节数组



## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "hardhat/console.sol";

contract MyContract{

    function sayHello(bytes calldata name)public pure returns (bytes memory){
        return bytes.concat("hello,", name);
    }
}
```



在REMIX中传入参数`"0x7A68616E6773616E"` (zhangsan的16进制)

输出

```
0x68656c6c6f2c7a68616e6773616e
```

