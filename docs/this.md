---
key: this
desc: 指向当前合约实例Address的指针
---

```solidity
this
```

指向当前合约实例Address的指针. 可明确转换为 `address` 或 `address payable`。



## 关于`this`和`address(this)`



`this` 和 `address(this)` 是同一个东西

`this` 是当solidity版本**低于0.5.0**时用于智能合约的术语。

`address(this)`是最新版本的solidity中用来指代智能合约的术语。



在 0.5.0 版本之前，Solidity 允许地址成员被一个合约实例访问，例如 this.balance。现在这被禁止了，必须做一个明确的地址转换：address(this).balance



更多的, 参考这里 https://www.geeksforgeeks.org/difference-between-this-and-addressthis-in-solidity/



