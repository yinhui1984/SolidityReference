---
key: tx,gasprice,origin
desc: 当前交易
---

在 Solidity 中，交易是指来自外部的函数调用或转账。每个交易都有一些属性，如交易发起者的地址、交易价值、汽油限制等。



## tx.gasprice

数据单位 `uint`

交易的 gas 价格



## tx.origin

数据单位 `address`

交易发送方（完整调用链上的原始发送方）



>注意`msg.sende` 和 `tx.origin`的区别
>
>https://yinhui1984.github.io/solidity_tx_origin_msg_sender/



> 注意: 在使用`address.delegatecall`时, `tx.origin`和`msg.sender`很可能是相同的了

### 例子

```solidity
    function deposit() public payable {
        console.log("tx.origin:",  tx.origin);
        console.log("tx.gasprice:", tx.gasprice);
        //....
    }
```



```solidity
// 看到网上有很多代码使用如下判断调用方是否是合约:
require(msg.sender == tx.origin, "Minting from smart contracts is disallowed");

//不要用codesize判断调用方是否是合约,那存在漏洞
```

