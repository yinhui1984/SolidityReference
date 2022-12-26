---
key: abi.encodeCall
desc: 将函数调用进行ABI编码
---

## 函数原型

```solidity
abi.encodeCall(function functionPointer, (...)) returns (bytes memory)
```

它可以用于对函数调用进行编码，以便将其传递给合约的其他函数或通过Ethereum的调用或事务发送到其他合约

`functionPointer`是要调用的函数的指针，这是一个函数类型的参数。后面的括号中的三个点表示可变参数列表，即函数调用中传递的参数。此函数返回类型为`bytes memory`，返回一个字节数组，其中包含对函数调用进行编码的结果。



## 举例

假设我们有以下合约：

```solidity
pragma solidity ^0.7.0;

contract Example {
    function add(uint a, uint b) public pure returns (uint) {
        return a + b;
    }
}

```

我们可以使用`abi.encodeCall`函数来对合约中的`add`函数进行编码，然后将其传递给另一个函数或通过Ethereum调用发送到另一个合约。例如：

```solidity
Example example = new Example();
bytes memory callData = abi.encodeCall(example.add, 10, 20);
```

变量`callData`将包含编码后的函数调用，其中包括函数名称和参数。你可以将这个字节数组传递给另一个函数，或者使用`eth.call`或`eth.sendTransaction`发送到另一个合约





## bug

https://blog.soliditylang.org/2022/03/16/encodecall-bug/