---
key: this
desc: 指向当前合约实例Address的指针
---

```solidity
this
```

 `this`关键字指的是合约自身的指针。它用于引用当前合约的实例，类似于其他面向对象编程语言中的`this`。`this`在Solidity合约内部使用，提供了一种方式来访问合约的当前实例及其属性和函数

可明确转换为 `address` 或 `address payable`。



使用`this`关键字无法调用合约的`private` 和 `internal` 成员（包括函数和变量）。`this`提供了对合约自身实例的引用，但它遵循Solidity的可见性规则



使用`this`调用函数与直接调用有不同的gas消耗：`this`会触发一个完整的EVM调用（即使是合约内部的），而直接调用则被视为内部调用



## 关于`this`和`address(this)`

`this` 是当solidity版本**低于0.5.0**时用于智能合约的术语。

`address(this)`是最新版本的solidity中用来指代智能合约的术语。



在 0.5.0 版本之前，Solidity 允许地址成员被一个合约实例访问，例如 `this.balance`。现在这被禁止了，必须做一个明确的地址转换：`address(this).balance`



更多的, 参考这里 https://www.geeksforgeeks.org/difference-between-this-and-addressthis-in-solidity/



## `this`的主要用途

1. `this` 可以用来获取当前合约的地址。在合约中，`address(this)`表示合约自身的地址。这在需要合约地址进行计算或传递时非常有用。

2. **调用合约的公共和外部函数**：

   通过`this`，你可以调用合约的公共（`public`）和外部（`external`）函数。尽管合约内部的函数可以直接调用，但有时使用`this`来显式调用它们可以使代码更清晰，或者在需要以外部调用（消耗更少的gas）的方式执行函数时很有用。
