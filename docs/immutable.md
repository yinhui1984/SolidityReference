---
key: immutable
desc: 不可变量
---

`immutable`关键字表示该变量的值在部署时必须设置，并且在整个合约生命周期中不可更改。它可以用于智能合约中的常量值、地址、字符串等类型的数据。



声明为 `immutable` 的变量比声明为 `constant` 的变量受到的限制要少一些。 不可变的变量可以在合约的构造函数中或在声明时被分配一个任意的值。 它们只能被分配一次，并且从那时起，即使在creation time也可以被读取。

编译器生成的合约创建代码将在其返回之前修改合约的运行时代码， 用分配给它们的值替换所有对不可变量的引用。 当您将编译器生成的运行时代码与实际存储在区块链中的代码进行比较时，这一点很重要。



> 在声明时被分配的不可变量只有在合约的构造函数执行时才会被视为初始化。 这意味着您不能在内联中用一个依赖于另一个不可变量的值来初始化不可变量。 然而，您可以在合约的构造函数中这样做。
>
> 这是对状态变量初始化和构造函数执行顺序的不同解释的一种保障，特别是在继承方面。



```solidity
pragma solidity ^0.8.0;

contract MyContract {
    address immutable owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function getOwner() public view returns (address) {
        return owner;
    }
}

```

