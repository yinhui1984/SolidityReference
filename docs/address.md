---
key: address,balance,code,codehash,transfer,send,call,delegatecall,staticcall
desc: 地址与成员函数
---



地址类型: https://docs.soliditylang.org/zh/latest/types.html#address

地址类型成员: https://docs.soliditylang.org/zh/latest/units-and-global-variables.html#address-related

地址类型有两种基本相同的类型：

- `address`: 保存一个20字节的值（一个以太坊地址的大小）。

- `address payable`: 与 `address` 类型相同，但有额外的方法 `transfer` 和 `send`。
  允许从 `address payable` 到 `address` 的隐式转换， 而从 `address` 到 `address payable` 的转换必须通过 `payable(<address>)` 来明确。

  ```solidity
  address payable ap = payable(msg.sender);
  address ad = ap;
  ```

  

对于 `uint160`、整数、 `bytes20` 和合约类型，允许对 `address` 进行明确的转换和输出。

uint 与address 之间转换

```solidity
uint256 i = uint256(uint160(msg.sender));
address a = address(uint160(uint(keccak256(abi.encodePacked(i)))));
```



对于合约类型，只有在合约可以接收以太的情况下才允许这种转换，也就是说， 合约要么有一个 [receive](https://docs.soliditylang.org/zh/latest/contracts.html#receive-ether-function) 函数，要么有一个 payable 类型的 fallback 的函数。 请注意， `payable(0)` 是有效的，是这个规则的例外。



## 关于大小写

`address` 类型本身是**不区分**大小写的。以太坊地址可以表示为 40 个十六进制字符的字符串，通常在这个字符串中字母可以是大写或小写，或者两者的混合。地址的大小写形式不影响其代表的实际地址。

### 为什么存在大小写混写

大小写混写形式主要是为了遵循 ERC-55 标准，这是一种通过大小写字母的使用来增加地址的校验信息的方法。这种校验机制可以帮助检测地址输入错误，但它并不改变地址本身的有效性

> ERC-55:
>
> https://github.com/ethereum/ercs/blob/master/ERCS/erc-55.md
>
> 为了生成符合 ERC-55 的大小写混写地址，可以按照以下步骤：
>
> 1. 将地址转换为小写形式，并去除前缀 `0x`。
> 2. 对该小写地址字符串进行 Keccak-256 哈希运算，得到一个新的哈希值。
> 3. 遍历原始地址的每个字符：
>    - 如果地址中的字符是一个数字（0-9），保持不变。
>    - 如果地址中的字符是一个字母（a-f），检查哈希值在相同位置的字符：
>      - 如果哈希值的字符在十六进制中大于或等于 8（即高四位为 1），则将原始地址中的字符转换为大写。
>      - 否则，保持为小写

## balance

`<address>.balance` （ `uint256` ）以 Wei 为单位的 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的余额。

```solidity
    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        //注意： owner是 payable的
        (bool ok, ) = owner.call{value: balance}("");
        require(ok, "Failed to withdraw");
        emit EtherWithdraw(owner, balance);
    }
```

## code

`<address>.code` （ `bytes memory` ）在 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的bytecode（可以是空的）。



## codehash

`<address>.codehash` （ `bytes32` ）[地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的代码哈希值



>`transfer`  `send` `call` 都可以向合约发送ether, 前提是 合约实现了下面之一
>
>- `receive() external payable`
>- `fallback() external payable`
>

>Which method should you use?
>
>`call` in combination with re-entrancy guard is the recommended method to use after December 2019.
>
>Guard against re-entrancy by
>
>- making all state changes before calling other contracts
>
>- using re-entrancy guard modifier
>
>  ```solidity
>      bool public locked;
>      
>      // Modifiers can be called before and / or after a function.
>      // This modifier prevents a function from being called while
>      // it is still executing.
>      modifier noReentrancy() {
>          require(!locked, "No reentrancy");
>  
>          locked = true;
>          _;
>          locked = false;
>      }
>  ```
>
>  



## transfer

```solidity
<address payable>.transfer(uint256 amount)
```

- **用途**：向指定地址发送固定数量的以太币（`amount`），单位是 Wei。
- **行为**：如果交易失败（比如因为被调用合约的 `fallback` 函数耗尽 Gas 或抛出异常），会自动回滚整个交易。
- **Gas 限制**：`transfer` 固定提供 2300 Gas，这足以完成基本日志操作，但不足以执行任何状态更新。
- **安全性**：防止重入攻击的一种方法，因为被调用方无法再次调用原始合约。

```solidity
function sendViaTransfer(address payable _to) public payable {
  _to.transfer(msg.value);
}
```

## send

```
<address payable>.send(uint256 amount) returns (bool)
```

- **用途**：与 `transfer` 类似，用于向指定地址发送以太币。
- **行为**：如果交易失败，不会自动回滚，而是返回 `false`。
- **Gas 限制**：与 `transfer` 相同，提供 2300 Gas。
- **安全性**：需要手动检查返回值来确认交易是否成功。

```solidity
function sendViaSend(address payable _to) public payable {
  // Send returns a boolean value indicating success or failure.
  // This function is not recommended for sending Ether.
  bool sent = _to.send(msg.value);
  require(sent, "Failed to send Ether");
}
```



> 关于2300 Gas
>
> 2300gas 能执行的操作很少,  比如使用transfer或call函数给合约发送ethers时,如在fallback函数或receive函数中有一些稍稍费gas的逻辑, 都会导致"EvmError: OutOfGas". 当然这也就是防止了重入
>
> 比如:
>
> ```solidity
> // SPDX-License-Identifier: SEE LICENSE IN LICENSE
> pragma solidity ^0.8.11;
> 
> contract FallbackDemo{
>     string public lastCalledFuncationName;
> 
>     function LastCalledFuncationName() public view returns (string memory) {
>         return lastCalledFuncationName;
>     }
> 
>     fallback() external payable {
>         // 如果使用transfer和send进行转账，会导致fallback函数失败
>         // 原因： transfer和send只有2300gas，不足以执行这里的字段赋值操作
>         lastCalledFuncationName = "fallback";
>     }
> 
>     function Hello() public payable {
>         lastCalledFuncationName = "Hello";
>     }
> }
> 
> //那么:
> // SPDX-License-Identifier: SEE LICENSE IN LICENSE
> pragma solidity ^0.8.11;
> 
> 
> import "forge-std/Test.sol";
> 
> import "../src/receivce_fallback_demo.sol";
> 
> 
> contract FallbackDemoTest is Test {
>     FallbackDemo fbd;
> 
>     function setUp() public {
>         vm.createSelectFork("theNet");
> 
>         fbd = new FallbackDemo();
>         vm.deal(address(this), 100 ether);
>     }
> 
>     function test1() public {
>         fbd.Hello();
>         console2.logString(fbd.LastCalledFuncationName());
>         assertTrue(keccak256(abi.encodePacked(fbd.LastCalledFuncationName())) == keccak256(abi.encodePacked("Hello")));
>     }
> 
> 		//失败
>     function testFail1() public{
>         address payable addr = payable(fbd);
>         addr.transfer(1 ether);
>     }
> 
> 		//失败
>     function testFail2() public{
>         address payable addr = payable(fbd);
>         addr.send(1 ether);
>     }
> 		
> 		//成功
>     function  test3() public{
>         address payable addr = payable(fbd);
>         addr.call{value: 1 ether}("");
>         console2.logString(fbd.LastCalledFuncationName());
>         assertTrue(keccak256(abi.encodePacked(fbd.LastCalledFuncationName())) == keccak256(abi.encodePacked("fallback")));
>     }
> }
> ```
>
> 

## call

```
<address>.call(bytes memory) returns (bool, bytes memory)
```

- **用途**：用于发起通用的函数调用，可以发送以太币和/或调用合约的函数。(也就是可以纯转账,也可以调用函数)
- **行为**：返回一个表示成功或失败的布尔值和包含返回数据的字节。
- **Gas 限制**：可以发送所有可用 Gas，或通过 `{value: x, gas: y}` 指定。
- **安全性**：需要谨慎使用，特别是当调用未知合约时。它允许更多复杂的交互，但也可能引入安全风险。

```solidity
function sendViaCall(address payable _to) public payable {
  // Call returns a boolean value indicating success or failure.
  // This is the current recommended method to use.
  // calldata为空, 纯转账
  (bool sent, bytes memory data) = _to.call{value: msg.value}("");
  require(sent, "Failed to send Ether");
}
```

```solidity
//注意, 被调用函数的参数是放到encodeWithSignature的括号里面的
(bool success, bytes memory result) = addr.call(abi.encodeWithSignature("myFunction(uint,address)", 10, msg.sender));
```

```solidity
_addr.call{value: 1 ether, gas: 1000000}(abi.encodeWithSignature("myFunction(uint,address)", 10, msg.sender));
```



> 返回的 `bytes momory result` 可以用 `abi.decode` 进行解码
>
> `bool ret = abi.decode(result, (bool));`
>
> `(bool ret, uint256 v) = abi.decode(result, (bool, uint256));`

> 在大多数情况下，对于合约函数的调用，<u>不推荐</u>使用 call，因为它绕过了类型检查、函数存在性检查和参数打包,  以及 revert时不会向上冒泡传递。最好是导入合约的接口来调用其上的函数。

> call比在合约实例上调用函数消耗的gas更少。所以在某些情况下，调用是优化gas的首选。

## delegatecall

```
<address>.delegatecall(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `DELEGATECALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节旷工费。

`delegatecall`**用于从合约A调用合约B的一个函数，并向该函数提供合约A的上下文(context)。**这样做的目的是将合约B中的函数作为库代码使用。因为该函数将表现为它是合约A本身的一个函数。请看这个帖子的代码例子: https://solidity-by-example.org/delegatecall/

>注意: 由于`delegatecal`用的是调用合约的上下文和被调用合约的算法, 所以这个时候`msg.sender`是等于`tx.origin`的
>
>而如果使用的是`call`,则 `msg.sender`是不等于`tx.origin`的

`delegatecall`语法与`call`语法完全相同，只是它**不能接受**`value`选项，只能接受`gas`选项。

`delegatecall`的一个流行且非常有用的用例是可升级合约。可升级合约使用一个代理合约，它将所有的函数调用转发给使用delegatecall的执行合约。代理合约的地址保持不变，而新的实现可以被多次部署。新实现的地址在代理合约中被更新。代理合约有完整的合约存储的状态。详细解释请查看文档https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies  和  https://docs.openzeppelin.com/contracts/4.x/api/proxy 以及代码 https://github.com/OpenZeppelin/openzeppelin-contracts/tree/v4.8.1/contracts/proxy .  和博客:  https://fravoll.github.io/solidity-patterns/proxy_delegate.html



```solidity
//注意, 被调用函数的参数是放到encodeWithSignature的括号里面的
(bool success, bytes memory data) = _contract.delegatecall(
							abi.encodeWithSignature("setVars(uint256)", _num));
```



> `delegatecall`  <u>暴露了自己的上下文给被调用的代码</u>, 如果你不能100%确定被调用代码的内容,则是非常危险的操作. 被调用的代码可以"以你的身份"干很多非法的事情, 比如修改状态变量等.
>
> 参考 https://github.com/yinhui1984/EthernautGameReferenceAnswers 中的 [第"17"个挑战](https://github.com/yinhui1984/EthernautGameReferenceAnswers/blob/main/17_Preservation.md).



> 上下文(context):  https://www.evm.codes/about#executionenv
>
> 包括: 代码, PC(程序计数器), 栈, 内存, 存储, calldata,  returndata



> 在EOA上调用delegateCall, 什么也不会发生, 并且返回true
>
> ```solidity
> (bool success, ) =EOA_addres.delegatecall(data);
> require(success, "delegate call failed");
> ```
>
> 

## staticcall

```
<address>.staticcall(bytes memory) returns (bool, bytes memory)
```

- **用途**：用于执行只读的合约调用。
- **行为**：与 `call` 相似，但保证不会修改状态。
- **适用场景**：在需要保证不改变任何状态的情况下查询合约信息时使用。

 `staticcall` 与 `call `完全一样，唯一的区别是它不能修改被调用的合约的状态。



> - **`transfer` 和 `send`**：更适用于简单的以太币转账，提供了防止重入的基本安全性。
> - **`call`**：适用于更复杂的交互，包括发送以太币和执行合约函数，但需要谨慎使用。
> - **`delegatecall`**：用于高级模式，如合约升级，但风险较高。
> - **`staticcall`**：适用于只读调用，保证不改变状态。

## 资金流向

合约A存在如下函数：  

```solidity
contract A {
    function SendEther(address payable to) public payable {
        to.transfer(msg.value);
    }
}
```

当合约B调用合约A的SendEther函数中，以太币是由谁发送给谁

```solidity
contract B{
	function XXX() public {
	  // ...
		_address_of_a.SendEther{value: 1 ether}(addr);
	}
}
```

### 流程

1. **发起交易**：
   - 调用者（可能是合约B或其调用者）发起一笔包含以太币的交易，调用合约A的 `SendEther` 函数。
2. **传递以太币**：
   - 交易中附带的以太币（`msg.value`）首先被发送到合约A。
3. **执行 `SendEther`**：
   - 合约A中的 `SendEther` 函数被执行。该函数接收一个参数 `address payable to`，这是以太币最终要发送到的地址。
4. **转账操作**：
   - 在 `SendEther` 函数内部，调用 `to.transfer(msg.value)` 将收到的以太币转发到地址 `to`。

### 以太币的流向

- 以太币最初由调用者（合约B或其调用者）发送给合约A。
- 随后，合约A将这些以太币发送到 `SendEther` 函数指定的 `to` 地址。
- 在这个过程中，合约A仅作为中间人，接收并立即将以太币转发到另一个地址
