---
key: gas, gasleft
desc: 剩余gas
---

```solidity
gasleft() returns (uint256)
```

正在运行的合约还剩下多少gas



>注意: 当你调用`gasleft()`时，你已经花费了数百个gas单位进入智能合约并跳转到你所调用的函数，更不用说交易本身使用的至少21000个gas

> opcode gas消耗表  [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) (Appendix H)
>
> 或 
>
> https://www.evm.codes/?fork=merge



>不同的 Solidity 编译器版本将以不同的方式计算gas。而且是否启用优化也会影响gas的使用。



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



以太坊的任何交易，甚至只是将以太币从一个地址转移到另一个地址，都需要至少21000个gas。
因此，所有的智能合约都应该期望至少燃烧21000个gas。调用函数、复制变量或存储信息的额外开销会在此基础上增加很多gas。