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

其中包含被调用函数的签名,参数值以及发送的value等

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;


contract MsgDemo {

    function GetMsgData() public payable  returns (bytes memory){
        return msg.data;
    }

    function GetMsgData2(int256 i) public payable  returns (bytes memory){
        return msg.data;
    }


    receive() external payable {}
}
```

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;

import "forge-std/Test.sol";
import "../src/msgdemo.sol";

contract MsgDemoTest is Test {
    MsgDemo md;

    function setUp() public {
        vm.createSelectFork("theNet");
        md = new MsgDemo();
    }

    function testGetMsgData() public {
        bytes memory data = md.GetMsgData();
        console2.logBytes(data);
        bytes memory sig = abi.encodeWithSignature("GetMsgData()");
        console2.logBytes(sig);
        assertTrue(keccak256(data) == keccak256(sig));

        vm.deal(address(this), 100);
        (bool ok, bytes memory data2) = (address(md)).call{value:100, gas:50000 }(abi.encodeWithSignature("GetMsgData()"));
        assertTrue(ok);
        console2.logBytes(data2);
    }

    function testGetMsgData2() public{
        bytes memory data = md.GetMsgData2(1);
        console2.logBytes(data);
        bytes memory sig = abi.encodeWithSignature("GetMsgData2(int256)", 1);
        console2.logBytes(sig);
        assertTrue(keccak256(data) == keccak256(sig));

        vm.deal(address(this), 100);
        (bool ok, bytes memory data2) = (address(md)).call{value:100, gas:50000 }(abi.encodeWithSignature("GetMsgData2(int256)", 1));
        assertTrue(ok);
        console2.logBytes(data2);
    }
}

```

输出

```
[PASS] testGetMsgData() (gas: 21949)
Logs:
  0x72538ea6
  0x72538ea6
  0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000472538ea600000000000000000000000000000000000000000000000000000000

[PASS] testGetMsgData2() (gas: 22662)
Logs:
  0x6bc5ecff0000000000000000000000000000000000000000000000000000000000000001
  0x6bc5ecff0000000000000000000000000000000000000000000000000000000000000001
  0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000246bc5ecff000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000
```



### msg.sig

数据类型`bytes4`

Calldata的前四个字节（即被调用函数的标识符）

### msg.value

数据类型 `uint256`

随消息发送的 wei 的数量

> 注: 函数要能接受以太币, 需要函数声明为payable, 并且合约要能接受以太币则需要有receive或fallback函数, 否则会evm revert 

### msg.gas (弃用)

使用**gasleft()**函数替代





## 举例1

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



## 举例2

```solidity
require(msg.sender == tx.origin, "Minting from smart contracts is disallowed");
```

