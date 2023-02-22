---
key: selfdestruct
desc: 合约自毁
---

```solidity
selfdestruct(address payable recipient)
```



合约自毁, 并将其资金发送到给定的地址.

When a contract is destroyed using `selfdestruct`, its **code, data and storage** are all removed from the Ethereum network. Any remaining ether held by the contract is sent to the designated address

It's important to note that once a contract is destroyed, it cannot be used again. Additionally, any contracts that have a reference to the destroyed contract will no longer be able to interact with it, and any ether held by the destroyed contract will be irretrievable. Therefore, the `selfdestruct` function should be used with caution and only when absolutely necessary.

> 将自毁合约地址上的资金发送到给定的地址时, 这个地址可以是外部账户地址, 也可以是合约地址.
>
> 给定地址是被`强制` 接收资金的. 即便被指定地址对应的合约没有`receive`函数或`fallback`函数
>
> 参考:
>
> https://github.com/yinhui1984/EthernautGameReferenceAnswers/blob/main/08_Force.md



## delegatecall 与 selfdestruct

在下面的代码中执行了test()以后, MyContract会被毁掉,  再次返回 mycontract.i 时返回0

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;


contract MyContract{

    uint256 public i = 1000;

    function Delegate( address _delegatee, bytes memory _data) external{
        _delegatee.delegatecall(_data);
    }
    
}

contract Boom{

    uint256 public i = 2000;

    function Destory() external {
        selfdestruct(payable(address(0x0)));
    }
}

contract Test{
    function test(MyContract c, Boom b) public{
        c.Delegate(address(b), abi.encodeWithSignature("Destory()"));
    }
}

```

