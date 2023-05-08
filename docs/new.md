---
key: new
desc: new
---

有几种不同的方法可以从现有的智能合约创建智能合约。一种方法是在 Solidity 中使用 `new` 关键字。 Solidity 中的 `new` 关键字用于创建智能合约的新实例。

## 在 智能合约函数中使用 `new`关键字将导致：

+ 部署一个新的合约
+ 初始化状态变量
+ 执行新合约的构造函数
+ nonce值设置为1
+ 返回给调用者的新合约实例的地址



## 成功使用`new`的前提

+ 创建新合约的代码在执行前就已经知道了
+ 新合约的地址是由创建合约的地址计算出来的。
+ 创建一个新的合约需要一个gas费用，以完成该操作



## Use case

有很多用例需要一个智能合约来创建其他合约。`new`关键字对于保持你的应用程序的通用性很有用。作为一个例子，自动做市商（AMM），如Uniswap和Pancake Swap，使用`new`关键字来创建交易对。阅读[这里](https://cryptomarketpool.com/how-do-the-uniswap-solidity-smart-contracts-work/)，了解更多关于Ethereum上的Uniswap solidity智能合约。

创建其他合约的合约通常被称为工厂合约(**factory contracts**)。作为一个例子，Uniswap工厂合约被用来创建交易对。此外，关于Uniswap工厂合约的信息可以在[这里](https://docs.uniswap.org/protocol/reference/core/interfaces/IUniswapV3Factory)找到。



## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

//账户
contract UserAccount {
    address public company;
    address public user;
    string public name;

    constructor(address _user, string memory _name) payable {
        company = msg.sender;
        user = _user;
        name = _name;
    } 

}

// 下面的AccountFactory合约将部署上面UserAccount合约中的代码
contract AccountFactory {
    // 状态变量数组，用于跟踪使用该合约创建的账户。
    UserAccount[] public useraccounts;


    // 这个函数需要两个参数。 一个用户的帐号和一个名字
    function CreateUserAccount(address _user, string memory _name) external payable{
        // new关键字用于创建一个新的合约

        // 如果要发生ether到新合约,则使用UserAccount{value: "amount"}(_user, _name);
        UserAccount account = new UserAccount(_user, _name);
        useraccounts.push(account);
    }

}
```



> 官方示例:
>
> https://docs.soliditylang.org/en/v0.8.9/control-structures.html?highlight=new%20keyword#creating-contracts-via-new



## create2

当创建一个合约时，合约的地址是由创建合约的地址和一个计数器计算出来的，这个计数器在每次创建合约时都会增加。

如果你指定了`salt`的选项（一个字节32的值），那么合约创建将使用不同的机制来得出新合约的地址。

它将从创建合约的地址、给定的`salt`值、创建合约的（creation）bytecode和构造器参数中计算出地址。

特别是，计数器（"nonce"）不被使用。这允许在创建合约时有更多的灵活性。你能够在新合约被创建之前推导出它的地址。此外，在创建合约的同时创建其他合约的情况下，你也可以依靠这个地址。

这里的主要用例是作为链外互动的judges的合约，只有在有争议的时候才需要创建。

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
contract D {
    uint public x;
    constructor(uint a) {
        x = a;
    }
}

contract C {
    function createDSalted(bytes32 salt, uint arg) public {
        // This complicated expression just tells you how the address
        // can be pre-computed. It is just there for illustration.
        // You actually only need ``new D{salt: salt}(arg)``.
        address predictedAddress = address(uint160(uint(keccak256(abi.encodePacked(
            bytes1(0xff),
            address(this),
            salt,
            keccak256(abi.encodePacked(
                type(D).creationCode,
                arg
            ))
        )))));

        D d = new D{salt: salt}(arg); // 注意new的时候要带上salt参数
        require(address(d) == predictedAddress);
    }
}
```

>在salt creation方面，有一些特殊性。一个合约在被销毁后可以在同一地址重新创建。然而，新创建的合约有可能有不同的部署字节码，即使创建字节码是相同的（这是一个要求，因为否则地址会改变）。这是由于编译器可以查询两次创建之间可能发生变化的外部状态，并在存储之前将其纳入部署的字节码中。
