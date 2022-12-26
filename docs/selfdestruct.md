---
key: selfdestruct
desc: 合约自毁
---

```solidity
selfdestruct(address payable recipient)
```



合约自毁, 并将其资金发送到给定的地址.

> 将自毁合约地址上的资金发送到给定的地址时, 这个地址可以是外部账户地址, 也可以是合约地址.
>
> 给定地址是被`强制` 接收资金的. 即便被指定地址对应的合约没有`receive`函数或`fallback`函数
>
> 参考:
>
> https://github.com/yinhui1984/EthernautGameReferenceAnswers/blob/main/08_Force.md