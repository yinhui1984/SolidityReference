---
key: ERC-20, EIP-20
desc: 同质化代币标准
---



# 同质化代币标准



ERC-20 :  Ethereum Request for Comments 20: https://ethereum.org/zh/developers/docs/standards/tokens/erc-20/ 来自于 EIP20: [Ethereum Improvement Proposals](https://eips.ethereum.org/) 20: https://eips.ethereum.org/EIPS/eip-20



## 含义

###  `decimals()`

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol#L87

返回用于获得其用户表示的小数的数量。

因为solidity不支持浮点数, 所以用一个"整数"加上一个"小数点后的位数"来表示浮点数

假设代币的精度为 6，那么当用户查询自己的代币余额时，合约会返回一个数字，这个数字表示用户拥有的代币数量。如果这个数字为 1000000，那么用户就拥有 1 个代币。如果这个数字为 100，那么用户就拥有 0.0001 个代币。

例如，如果`decimals`等于`2`，`505`代币的余额应该显示为`5.05`（`505 / 10 ** 2`）给用户。

代币通常选择18的值，模仿以`Ether` 和 `Wei`的关系。这是该函数返回的默认值，除非它被重写。

注意：该信息仅用于_显示_目的：它绝不影响合约的任何算术，包括`balanceOf`和`transfer`。



### `totalSupply()`

代币总供应量, 这包括创建合约时的初始供应量, 旷工奖励 , 销毁量

参考这里  https://docs.openzeppelin.com/contracts/3.x/erc20-supply

```js
    let decimals = await myContract.decimals();
    assert.equal(18, decimals, "decimals should be 18");

    let totalSupply = await myContract.totalSupply();
    // totalSupply is BN (big number)
    //console.log(totalSupply.toString());
    let total = 100 * 10 ** decimals;
    assert.equal(total.toString(), totalSupply.toString(), "totalSupply should be xx");

```



### `balanceOf()`

查询指定地址上的余额

```solidity
function balanceOf(address account) public view returns (uint256)
```



### `transfer()`

```solidity
function transfer(address _to, uint256 _value) public returns (bool success)
```

`msg.sender`将自己地址上的部分余额转移到指定地址上



### `approve()`

```solidity
function approve(address _spender, uint256 _value) public returns (bool success)
```

`msg.sener` 将自己的token授权一部分给`_spender`, 让`_spender`来支配 (transferFrom, burn等)



> 关于 approve allowance transferFrom 他们三者的关系, 参考下面示例代码

### `allowance()`

剩余额度查询, 查询`_owner`给`_spender`批准的额度还剩多少)

```solidity
function allowance(address _owner, address _spender) public view returns (uint256 remaining)
```

### `transferFrom()`

```solidity
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)
```



在 

+  `from ` 已经通过`approve()`的给`msg.sender`授权 

  和 

+ `msg.sender`在`from`那里的 `allowance()`还有剩余

的基础之上,

`msg.sender`  从 `from` 那里转移一定数量的代币给 `to`

## 注意事项

> 不要搞混淆代码中的各种数量  和  口头上的或用户界面上的 "多少个代币"之间的关系:
>
> 比如: 我有3个代币, 实际代码运算时是: 3 * (10 * decimals())

> `name()`  ` symbol()`  ` decimals()` 三个方法是可选的

> 调用者要自己处理返回`false`的情况, `不能`假定方法始终返回`true`

> `transfer`时, 正常转移必须触发 `Transfer`事件

> `transfer`时, 不足以转移时要触发异常, 并且转移量为`0`是正常操作

> 创建新代币的代币合约应该在代币创建时触发一个转移事件，`_from`地址设置为`0x0`





## 例子

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
//import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

contract ExampleToken is ERC20Burnable {
    constructor(string memory _name, string memory _symbol)
        ERC20(_name, _symbol)
    {
        //用户界面上显示的是100个代币
        uint256 initSupply = 100 * 10**decimals();
        _mint(msg.sender, initSupply);
    }
}

```



```js
const ExampleToken = artifacts.require("ExampleToken");


contract("ExampleToken", function (/* accounts */) {
  it("should assert true", async function () {
    let ext = await ExampleToken.deployed();
    let accounts = await web3.eth.getAccounts();
    let owner = accounts[0];
    let user0 = owner;
    let user1 = accounts[1];
    let user2 = accounts[2];

    let name = await ext.name();
    assert.equal("ExampleToken", name, "name should be ExampleToken");

    let symbol = await ext.symbol();
    assert.equal("EXT", symbol, "symbol should be EXT");

    let decimals = await ext.decimals();
    assert.equal(18, decimals, "decimals should be 18");

    let totalSupply = await ext.totalSupply();
    //console.log(totalSupply.toString());
    let total = 100 * 10 ** decimals;
    assert.equal(total.toString(), totalSupply.toString(), "totalSupply should be xx");

    let balanceOfOwner = await ext.balanceOf(owner);
    assert.equal(totalSupply.toString(), balanceOfOwner.toString(), "balanceOfOwner should be totalSupply");

    let balanceOfUser1 = await ext.balanceOf(user1);
    assert.equal(0, balanceOfUser1, "balanceOfUser1 should be 0");

    await ext.transfer(user1, 500);


    //调用者(message.sender, 也就是这里的user0)给user1批准10000的额度,让user1支配
    await ext.approve(user1, 10000, { from: user0 });
    let allowance = await ext.allowance(user0, user1);
    assert.equal("10000", allowance.toString(), "allowance should be 10000");

    //user1从user0转账1000给user2
    await ext.transferFrom(user0, user2, 1000, { from: user1 });
    //查询user1在user0哪里的额度，应该减少了1000了
    allowance = await ext.allowance(user0, user1);
    assert.equal(9000, allowance, "allowance should be 9000");

    //查询user2的余额，应该增加了1000
    let balanceOfUser2 = await ext.balanceOf(user2);
    assert.equal(1000, balanceOfUser2, "balanceOfUser2 should be 1000");

    //user1将剩余的额度中的3000转给自己
    await ext.transferFrom(user0, user1, 3000, { from: user1 });
    allowance = await ext.allowance(user0, user1);
    assert.equal(6000, allowance, "allowance should be 6000");

    //user1将剩余的额度对应的代币全部销毁
    await ext.burnFrom(user0, 6000, { from: user1 });
    allowance = await ext.allowance(user0, user1);
    assert.equal(0, allowance, "allowance should be 0");

  });
});

```



## EIP20 翻译

https://eips.ethereum.org/EIPS/eip-20 



### EIP-20 : 代币标准

| Author   | [Fabian Vogelsteller](mailto:fabian@ethereum.org), [Vitalik Buterin](mailto:vitalik.buterin@ethereum.org) |
| -------- | ------------------------------------------------------------ |
| Status   | Final                                                        |
| Type     | Standards Track                                              |
| Category | ERC                                                          |
| Created  | 2015-11-19                                                   |

####  Simple Summary

一个标准的代币接口。

####  摘要

以下标准允许在智能合约内实现一个标准的代币API。这个标准提供了转移代币的基本功能，以及允许代币被批准，以便它们可以被另一个 链上的第三方消费(can be spent by another on-chain third party.)

#### 动机

一个标准接口允许以太坊上的任何代币被其他应用程序重新使用：从钱包到去中心化的交易所。

#### 规范



#### 代币

##### 方法

> 以下规范使用Solidity 0.4.17（或以上）的语法
> 调用者必须从返回（bool success）中处理 false。调用者决不能假定false永远不会被返回(Callers MUST handle false from returns (bool success). Callers MUST NOT assume that false is never returned!)

###### name() 

返回令牌的名称 - 例如 "MyToken"。

OPTIONAL - 这个方法可以用来提高可用性，但是接口和其他合约不可以期望这些值出现。

```solidity
function name() public view returns (string)
```



###### symbol()

返回令牌的符号。例如："HIX"。

OPTIONAL - 这个方法可以用来提高可用性，但是接口和其他合约不可以期望这些值出现。

```solidity
function symbol() public view returns (string)
```



###### decimals()

返回令牌使用的小数点的数量--例如，`8`，意味着用令牌金额除以100000000 (10^8)来获得其用户表示。

OPTIONAL - 这个方法可以用来提高可用性，但是界面和其他合约不可以期望这些值出现。

```solidity
function decimals() public view returns (uint8)
```



###### totalSupply()

返回总的代币供应量。

```solidity
function totalSupply() public view returns (uint256)
```



###### transfer()

将`_value`数额的代币转移到地址`_to`，**并且必须触发`Transfer`事件**。如果消息调用者的账户余额没有足够的代币可以花费，该函数应该`throw`。

注意 `0`值的转移必须被视为正常的转移，并触发`Transfer`事件。

```solidity
function transfer(address _to, uint256 _value) public returns (bool success)
```

###### transferFrom()

从地址`_from`向地址`_to`转移`_value`数量的代币，并且必须触发`Transfer`事件。

`transferFrom`方法用于提款工作流程，**允许合约代表你转移代币**。例如，这可用于允许合约代表你转移代币和/或以子货币收取费用。

该函数应该`throw`，除非`_from`账户通过某种机制故意授权消息的发送者。

注意 `0`值的转移必须被视为正常的转移，并触发`Transfer`事件

```solidity
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)
```

###### approve()

<u>(译者注: 额度批准, 批准一定额度给`_spender` 使用)</u>

允许`_spender`**多次**从你的账户中提款，最多到`_value`的金额。如果这个函数被再次调用，它将用`_value`覆盖当前的限额(allowance)。

注意：为了防止像[这里所描述的](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/)和[这里所讨论的](https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729)那样的攻击媒介，客户应该确保在创建用户界面时，先将`allowance`设置为0，然后再为同一个花费者设置另一个值。然而，合约本身不应该强制执行，以允许向后兼容之前部署的合约。

```solidity
function approve(address _spender, uint256 _value) public returns (bool success)
```



###### allowance()

 (<u>译者注: 额度查询, 查询`_owner`给`_spender`批准的额度还剩多少</u>)

返回`_spender`仍可从`_owner`那里提取的金额。

```solidity
function allowance(address _owner, address _spender) public view returns (uint256 remaining)
```



##### 事件

###### event Transfer

必须在代币被转移时触发，包括零值转移。

创建新代币的代币合约应该在代币创建时触发一个转移事件，`_from`地址设置为`0x0`。

```solidity
event Transfer(address indexed _from, address indexed _to, uint256 _value)
```



###### event Approval

必须在任何对`approve(address _spender, uint256 _value)`的成功调用中触发。

```solidity
event Approval(address indexed _owner, address indexed _spender, uint256 _value)
```



#### 实现

已经有很多符合ERC20标准的代币部署在以太坊网络上。不同的团队编写了不同的实现方式，有不同的权衡：从节省`gas`到提高安全性。

 实现的例子:

- OpenZeppelin : https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
- ConsenSys : https://github.com/ConsenSys/Tokens/blob/master/contracts/eip20/EIP20.sol



#### 历史



Historical links related to this standard:

- Original proposal from Vitalik Buterin: https://github.com/ethereum/wiki/wiki/Standardized_Contract_APIs/499c882f3ec123537fc2fccd57eaa29e6032fe4a
- Reddit discussion: https://www.reddit.com/r/ethereum/comments/3n8fkn/lets_talk_about_the_coin_standard/
- Original Issue #20: https://github.com/ethereum/EIPs/issues/20



#### Copyright

Copyright and related rights waived via [CC0](https://eips.ethereum.org/LICENSE).

#### 引用

Please cite this document as:

[Fabian Vogelsteller](mailto:fabian@ethereum.org), [Vitalik Buterin](mailto:vitalik.buterin@ethereum.org), "EIP-20: Token Standard," *Ethereum Improvement Proposals*, no. 20, November 2015. [Online serial]. Available: https://eips.ethereum.org/EIPS/eip-20.
