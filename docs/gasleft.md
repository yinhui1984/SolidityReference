---
key: gasleft
desc: 剩余gas
---

```solidity
gasleft() returns (uint256)
```

正在运行的合约还剩下多少gas





```solidity
function test() returns (uint256 gasUsed)
{
    uint256 startGas = gasleft();

    // ...some code here...

    gasUsed = startGas - gasleft();
}
```



> 你需要为一笔交易支付多少以太币？
>
> [gas数量] \* [gas价格]
>
> 其中：
>
> - gas是一个计算单位
>
> - 耗费的gas是指在一次交易中使用的gas总量
>
> - gas price是指你愿意为每个gas支付多少ether



> gas不够?
>
> There are 2 upper bounds to the amount of gas you can spend
>
> - `gas limit` (max amount of gas you're willing to use for your transaction, set by you)
> - `block gas limit` (max amount of gas allowed in a block, set by the network)