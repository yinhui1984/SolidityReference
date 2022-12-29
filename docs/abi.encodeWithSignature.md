---
key: abi.encodeWithSignature
desc: 函数签名和参数编码
---





## 函数原型

```solidity
abi.encodeWithSignature(string memory signature, ...) returns (bytes memory)
```



## 说明

同 

```solidity
abi.encodeWithSelector(bytes4(keccak256(bytes(signature)), ...) returns (bytes memory)
```



`signature`是函数的签名，是一个字符串类型的参数。后面的括号中的三个点表示可变参数列表，即函数调用中传递的参数。此函数返回类型为`bytes memory`，返回一个字节数组，其中包含对函数调用进行编码的结果，并在开头添加了函数签名。



## 举例

```solidity
bytes memory callData = abi.encodeWithSignature("add(uint256,uint256)", 1, 2);
```

> 注意, 类型要写全称, 比如`uint256` 而不是 `uint`
