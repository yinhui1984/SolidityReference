---
key: string.concat
desc: 连接2个或多个字符串
---

```solidity
string.concat(...) returns (string memory)
```



## 说明

连接2个或多个字符串,然后返回新的字符串

> 不能用 "+" 连接字符串



## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "hardhat/console.sol";

contract MyContract{

    function sayHello(string calldata name)public pure returns (string memory){
        //error when use "+"
        //return "hello," + name;
        return string.concat("hello," , name);
        //也可以用下面这种方式
        //return string(abi.encodePacked("hello,", name));
    }
}

```

