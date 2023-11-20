---
key: selfdestruct
desc: 合约自毁
---

```solidity
selfdestruct(address payable recipient)
```



合约自毁, 并将其资金发送到给定的地址.

使用 "自毁 "销毁合约时，其**代码、数据和存储**都会从以太坊网络中删除。合约持有的任何剩余以太币都会被发送到指定地址。

值得注意的是，合约一旦销毁，就不能再使用。此外，任何对已销毁合约有引用的合约都将无法再与之交互，已销毁合约持有的以太币也将无法收回。因此，只有在绝对必要的情况下，才应谨慎使用 "自毁 "函数。

 注意， `selfdestruct` 有一些从EVM继承的特殊性：

- 接收合约的接收函数不会被执行。
- 合约只有在交易结束时才真正被销毁， 任何一个 `revert` 可能会 "恢复" 销毁。

> 将自毁合约地址上的资金发送到给定的地址时, 这个地址可以是外部账户地址, 也可以是合约地址.
>
> 给定地址是被`强制` 接收资金的. 即便被指定地址对应的合约没有`receive`函数或`fallback`函数
>
> 参考:
>
> https://github.com/yinhui1984/EthernautGameReferenceAnswers/blob/main/08_Force.md

>"selfdestruct" deprecated in Solidity 0.8.18
>
>"selfdestruct" has been deprecated. The underlying opcode will eventually undergo breaking changes, and its use is not recommended.
>
>到目前为止,只会收到一个编译警告, 但仍然可用



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

