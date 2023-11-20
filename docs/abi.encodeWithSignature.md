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

函数签名:

1. **函数名称**：这是定义在合约中的函数的名称。
2. **参数类型列表**：这是函数参数的类型，按照在函数声明中出现的顺序排列。重要的是，这里只包括参数的类型，不包括参数的名称。
3. 在计算函数签名时，参数名称、返回类型和访问修饰符（如 `public`、`private`）都不被考虑在内，仅参数的类型顺序重要。
4. 函数签名的唯一性意味着即使是微小的变化（比如参数类型的不同顺序）也会产生完全不同的签名



## 举例

```solidity
bytes memory callData = abi.encodeWithSignature("add(uint256,uint256)", 1, 2);
```

> 注意:
>
> 1,  类型要写全称, 比如`uint256` 而不是 `uint`
>
> 2, 传入的字符串不要有空格
