---
key: proxy, upgradeable
desc: 可升级代理模式
---



## 可升级的合约

参考 :  https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable



> 可升级合约中, 不允许使用 `selfdestruct` 或 `delegatecall`
>
> https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#potentially-unsafe-operations

> 更新可升级合约中, 不允许修改已有状态变量的类型和声明顺序. 反正注意对存储的影响
>
> https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#modifying-your-contracts

> 可以使用`Storage Gaps` 来为未来预留存储槽
>
> https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps

### 普通的可升级合约

对于可升级合约,  不能使用构造函数, 而应该将构造函数的工作拿到一个普通函数`initialize`中, 并且该函数应该和构造函数一样只能被调用一次, 对于这个工作, openzeppelin提供了 initializer修改器供使用

```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

// contract MyContract{
//     uint256 public x;
//     bool private initialized;

//     function initialize(uint256 _x) public{

//         require(!initialized, "already initialized");
//         initialized = true;
//         x = _x;
//     }
// }

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract MyContract is Initializable {
    uint256 public x;

    function initialize(uint256 _x) public initializer{
        x = _x;
    }

}
```

`对于有继承关系的合约` 请注意下面的写法

```solidity
// contracts/MyContract.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract BaseContract is Initializable {
    uint256 public y;

    function initialize() public onlyInitializing {
        y = 42;
    }
}

contract MyContract is BaseContract {
    uint256 public x;

    function initialize(uint256 _x) public initializer {
        BaseContract.initialize(); // Do not forget this call!
        x = _x;
    }
}
```



> 如果某个字段没有在`initialize`中进行初始化, 那么在可升级合约的实例中将会缺失这些字段
>
>  比如 `uint256 public hasInitialValue = 100; `
>
> 但是, 定义常量状态变量仍然是可以的，因为[编译器不会为这些变量保留一个存储槽](https://docs.soliditylang.org/en/latest/contracts.html#constant-state-variables)，每一次出现都会被相应的常量表达式取代, 比如 `uint256 public constant hasInitialValue = 100; `



> 如果在编写可升级合约时, 在其内部`new`了一个合约, 由于`new`关键字直接将该合约进行部署了, 那么该合约将不可升级. 参考这里:  https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#creating-new-instances-from-your-contract-code

### 可升级的ERC20

`对于可升级的ERC20合约` 由于普通的ERC20需要使用构造函数初始化Token Name和Token Symbol, 参考这里 https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#use-upgradeable-libraries  并使用 [ERC20Upgradeable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/v4.7.3/contracts/token/ERC20/ERC20Upgradeable.sol)  





## 代理模式

参考 : https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies

其基本思想是使用代理进行升级。第一个合约是一个简单的包装或 "代理"，用户直接与之互动，并负责将交易转发给第二个合约，其中包含逻辑。需要理解的关键概念是，逻辑合约可以被替换，而代理，或接入点永远不会改变。这两个合约仍然是不可改变的，因为它们的代码不能被改变，但逻辑合约可以简单地被另一个合约所取代。因此，封装器可以指向不同的逻辑实现，这样一来，软件就 "升级 "了。

```
User ---- tx ---> Proxy ----------> Implementation_v0
                     |
                      ------------> Implementation_v1
                     |
                      ------------> Implementation_v2
```

### 转发

代理需要解决的最直接的问题是，代理如何公开逻辑合约的整个接口，而不需要对整个逻辑合约的接口进行一对一的映射。这样就很难维护，容易出错，而且会使接口本身无法升级。因此，需要一个动态转发机制。这种机制的基本原理在下面的代码中呈现。

https://github.com/OpenZeppelin/openzeppelin-contracts/tree/v4.8.1/contracts/proxy



```solidity

assembly {
  let ptr := mload(0x40)

  // (1) copy incoming call data
  calldatacopy(ptr, 0, calldatasize)

  // (2) forward call to logic contract
  // _impl is the address of current implemention 
  let result := delegatecall(gas, _impl, ptr, calldatasize, 0, 0)
  let size := returndatasize

  // (3) retrieve return data
  returndatacopy(ptr, 0, size)

  // (4) forward return data back to caller
  switch result
  case 0 { revert(ptr, size) }
  default { return(ptr, size) }
}

```

这段代码可以放在代理的`回退函数`中，并将任何对带有任何参数集的函数的调用转发给逻辑合约，而不需要知道逻辑合约的任何具体接口。实质上，（1）调用数据被复制到内存中，（2）调用被转发到逻辑合约，（3）从调用到逻辑合约的返回数据被检索，（4）返回数据被转发回调用者。

需要注意的一个非常重要的事情是，该代码利用了EVM的委托调用操作码，该操作码在调用者的状态背景下执行被调用者的代码。也就是说，逻辑合约(也就是可升级的那个合约)控制着代理的状态，而逻辑合约的状态是没有意义的。因此，代理不仅仅是在逻辑合约之间转发事务，而且还代表了这一对的状态。状态在代理中，逻辑在代理所指向的特定实现中。

### 存储

> 状态变量是存储在代理中的, 可升级合约值提供逻辑, 这是因为代理通过delegatecall调用的逻辑合约
> 



### 存储逻辑合约的地址

> 除了存储普通状态变量外, 还需要一个槽来存储当前使用的逻辑合约`implementation`的地址`implementationPosition` 

在使用代理时，很快就会出现一个问题，这与代理合约中变量的存储方式有关。假设代理将逻辑合约的地址存储在其唯一的变量地址`public implementation;`中。现在，假设逻辑合约是一个基本标记，其第一个变量是地址`public _owner`。这两个变量的大小都是32字节，就EVM所知，占据了代理调用的结果执行流程的第一个槽。当逻辑合约写到owner时，它是在代理的状态范围内进行的，实际上是写到了_implementation。这个问题可以被称为 Storage collision "存储碰撞"。

```
|Proxy                     |Implementation           |
|--------------------------|-------------------------|
|address _implementation   |address _owner           | <=== 存储碰撞!
|...                       |mapping _balances        |
|                          |uint256 _supply          |
|                          |...                      |
```



有许多方法可以克服这个问题，而OpenZeppelin升级版实现的 "非结构化存储 "方法的工作原理如下。它没有将`_implementation`地址存储在代理的第一个存储槽，而是选择了一个伪随机槽。这个槽是足够随机的，以至于逻辑合约在同一槽中声明一个变量的概率可以忽略不计。在代理的存储槽位置随机化的原则同样用于代理可能拥有的任何其他变量，例如管理地址（允许更新_implementation的值），等等。

```
|Proxy                     |Implementation           |
|--------------------------|-------------------------|
|...                       |address _owner           |
|...                       |mapping _balances        |
|...                       |uint256 _supply          |
|...                       |...                      |
|...                       |                         |
|...                       |                         |
|...                       |                         |
|...                       |                         |
|address _implementation   |                         | <=== Randomized slot.
|...                       |                         |
|...                       |                         |
```

在[EIP1967](http://eips.ethereum.org/EIPS/eip-1967)年之后，如何实现随机存储的一个例子。

```solidity
bytes32 private constant implementationPosition = bytes32(uint256(
  keccak256('eip1967.proxy.implementation')) - 1
));
```

因此，逻辑合约不需要关心重写代理的任何变量。其他面临这个问题的代理实现通常意味着让代理知道逻辑合约的存储结构并适应它，或者让逻辑合约知道代理的存储结构并适应它。这就是为什么这种方法被称为 "非结构化存储"；两个合约都不需要关心另一个合约的结构。



### 不同实现版本之间的存储

如前所述，非结构化的方法避免了逻辑合同和代理之间的存储碰撞。然而，不同版本的逻辑合同之间可能会发生存储碰撞。在这种情况下，想象一下，逻辑合约的第一个实现在第一个存储槽中存储了地址`public _owner`，而升级后的逻辑合约在同一个第一槽中存储了地址`public _lastContributor`。当升级后的逻辑合约试图写入`_lastContributor`变量时，它将使用与之前存储`_owner`的值相同的存储位置，并将其覆盖！在这种情况下，逻辑合约就会出现问题。

> 为什么是发生碰撞?
>
> 1. 编译完成后已经没有变量名称的概念了, 而是按照slot编号进行读写的
> 2. 存储在proxy合约中, 而不是在逻辑合约中, 各个版本的逻辑合约都共用的同一份在proxy合约中的存储布局.

错误的:

```
|Implementation_v0   |Implementation_v1        |
|--------------------|-------------------------|
|address _owner      |address _lastContributor | <=== 存储碰撞!
|mapping _balances   |address _owner           |
|uint256 _supply     |mapping _balances        |
|...                 |uint256 _supply          |
|                    |...                      |
```

正确的

```
|Implementation_v0   |Implementation_v1        |
|--------------------|-------------------------|
|address _owner      |address _owner           |
|mapping _balances   |mapping _balances        |
|uint256 _supply     |uint256 _supply          |
|...                 |address _lastContributor | <=== Storage extension.
|                    |...                      |
```

非结构化存储代理机制并不能防止这种情况。这取决于用户是否让新版本的逻辑合约扩展以前的版本，或以其他方式保证存储层次结构总是被附加到但不被修改。然而，OpenZeppelin升级会检测到这种碰撞，并适当地警告开发者。



### 构造函数!

在 Solidity 中，位于构造函数内的代码或一部分全局变量声明不属于已部署合约的运行时字节码。这段代码只在合约实例被部署时执行一次，。因此，逻辑合约的构造函数中的代码永远不会在代理的状态背景下被执行。换句话说，代理对构造函数的存在是完全无视的。对代理来说，这就好像它们不存在一样。

> 构造函数的代码和部分全局变量声明 是在创建时被执行的(creation code)
>
> 而代理只知道运行时代码(runtime code)

不过这个问题很容易解决。逻辑合约应该把构造函数中的代码移到一个普通的 "初始化 "函数中，并且在代理链接到这个逻辑合约时调用这个函数。需要特别注意这个初始化函数，以便它只能被调用一次，这也是一般编程中构造函数的属性之一。

这就是为什么当我们使用OpenZeppelin Upgrades创建一个代理时，你可以提供初始化函数的名称并传递参数。

为了确保初始化函数只能被调用一次，我们使用了一个简单的修改器。OpenZeppelin Upgrades通过一个可以扩展的合约提供这个功能。

参考上面的可升级合约部分



### 透明代理和函数冲突

如前所述，可升级的合约实例（或代理）通过委托所有调用逻辑合约来工作。然而，代理需要一些自己的函数，比如 upgradeTo(address) 来升级到一个新的实现。这就引出了一个问题：如果逻辑合约也有一个名为upgradeTo(address)的函数，该如何进行：在调用该函数时，调用者是想调用代理还是逻辑合约？

> 冲突也可能发生在具有不同名称的函数之间。作为合同的公共ABI的一部分，每个函数在字节码水平上都由一个4字节的标识符来识别。这个标识符取决于函数的名称和算术，但由于它只有4个字节，有可能两个不同名称的函数最终会有相同的标识符。Solidity 编译器会跟踪这种情况在同一合约内发生的情况，但不跟踪在不同合约之间发生的碰撞，例如在代理和它的逻辑合约之间。[阅读这篇文章](https://medium.com/nomic-labs-blog/malicious-backdoors-in-ethereum-proxies-62629adf3357)以获得更多关于此的信息。

OpenZeppelin Upgrades处理这个问题的方式是通过透明代理模式。一个透明的代理将根据调用者的地址（即msg.sender）来决定哪些调用被委托给底层逻辑合约。

+ If the caller is the admin of the proxy (the address with rights to upgrade the proxy), then the proxy will not delegate any calls, and only answer any messages it understands.

+ f the caller is any other address, the proxy will always delegate a call, no matter if it matches one of the proxy’s functions.

假设一个具有 owner() 和 upgradeTo() 函数的代理，将调用委托给具有 owner() 和 transfer() 函数的 ERC20 合约，下表涵盖了所有场景：

| msg.sender | owner()               | upgradeto()               | transfer()               |
| ---------- | --------------------- | ------------------------- | ------------------------ |
| Owner      | returns proxy.owner() | returns proxy.upgradeTo() | fails                    |
| Other      | returns erc20.owner() | fails                     | returns erc20.transfer() |

幸运的是，OpenZeppelin Upgrades考虑到了这种情况，并创建了一个中间的ProxyAdmin合同，负责你通过Upgrades插件创建的所有代理。即使你从你的节点的默认账户调用部署命令，ProxyAdmin合同将是你所有代理的实际管理员。这意味着，你将能够从你的任何一个节点的账户与代理进行互动，而不必担心透明代理模式的细微差别。只有从 Solidity 创建代理的高级用户才需要了解透明代理模式。





## example

https://solidity-by-example.org/app/upgradeable-proxy/

https://dev.to/yakult/tutorial-write-upgradeable-smart-contract-proxy-contract-with-openzeppelin-1916



## 其它

https://rya-sge.github.io/access-denied/2022/10/31/proxy-contract-summary/

https://www.certik.com/resources/blog/FnfYrOCsy3MG9s9gixfbJ-upgradeable-proxy-contract-security-best-practices



