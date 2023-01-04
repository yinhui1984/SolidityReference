---
key: address,balance,code,codehash,transfer,send,call,delegatecall,staticcall
desc: 地址与成员函数
---



地址类型: https://docs.soliditylang.org/zh/latest/types.html#address

地址类型成员: https://docs.soliditylang.org/zh/latest/units-and-global-variables.html#address-related



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

## transfer (不推荐)

```
<address payable>.transfer(uint256 amount)
```

向 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 发送数量为 amount 的 Wei，失败时抛出异常，发送 2300 gas 的矿工费，不可调节。

```solidity
function sendViaTransfer(address payable _to) public payable {
  // This function is no longer recommended for sending Ether.
  _to.transfer(msg.value);
}
```

## send

```
<address payable>.send(uint256 amount) returns (bool)
```

向 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 发送数量为 amount 的 Wei，失败时返回 `false` 2300 gas 的矿工费用，不可调节。

```solidity
function sendViaSend(address payable _to) public payable {
  // Send returns a boolean value indicating success or failure.
  // This function is not recommended for sending Ether.
  bool sent = _to.send(msg.value);
  require(sent, "Failed to send Ether");
}
```



## call

```
<address>.call(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `CALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。

```solidity
function sendViaCall(address payable _to) public payable {
  // Call returns a boolean value indicating success or failure.
  // This is the current recommended method to use.
  (bool sent, bytes memory data) = _to.call{value: msg.value}("");
  require(sent, "Failed to send Ether");
}
```

```solidity
(bool success, bytes memory result) = addr.call(abi.encodeWithSignature("myFunction(uint,address)", 10, msg.sender));
```

```solidity
_addr.call{value: 1 ether, gas: 1000000}(abi.encodeWithSignature("myFunction(uint,address)", 10, msg.sender));
```



> 在大多数情况下，对于合约函数的调用，<u>不推荐</u>使用 call，因为它绕过了类型检查、函数存在性检查和参数打包,  以及 revert时不会向上冒泡传递。最好是导入合约的接口来调用其上的函数。

> call比在合同实例上调用函数消耗的gas更少。所以在某些情况下，调用是优化gas的首选。

## delegatecall

```
<address>.delegatecall(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `DELEGATECALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。

`delegatecall`用于从合约A调用合约B的一个函数，并向该函数提供合约A的上下文(存储、余额和地址)。这样做的目的是将合约B中的函数作为库代码使用。因为该函数将表现为它是合约A本身的一个函数。请看这个帖子的代码例子: https://solidity-by-example.org/delegatecall/

`delegatecall`语法与`call`语法完全相同，只是它**不能接受**`value`选项，只能接受`gas`选项。

`delegatecall`的一个流行且非常有用的用例是可升级合约。可升级合约使用一个代理合约，它将所有的函数调用转发给使用delegatecall的执行合约。代理合约的地址保持不变，而新的实现可以被多次部署。新实现的地址在代理合约中被更新。代理合约有完整的合约存储的状态。详细解释请查看[Openzepplin](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies)文档。

## staticcall

```
<address>.staticcall(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `STATICCALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。

 `staticcall` 与 `call `完全一样，唯一的区别是它不能修改被调用的合约的状态。

