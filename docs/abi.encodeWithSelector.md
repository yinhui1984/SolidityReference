---
key: abi.encodeWithSelector
desc: 函数选择器和参数编码
---

## 函数原型

```solidity
abi.encodeWithSelector(bytes4 selector, ...) returns (bytes memory)
```

## 说明

它可以将一个函数的参数编码为字节数组。

`abi.encodeWithSelector`接受两个参数：

1. `bytes4 selector`：这是函数的四个字节的选择器，也就是函数的哈希值的前四个字节。选择器用于在多个同名函数之间区分，因为它们可能具有不同的参数类型和数量。
2. `...`：这是可变参数列表，表示函数的任意数量的参数。

这个函数返回一个字节数组，其中包含编码的选择器和参数。



## 举例

假设你有一个名为`add`的函数，它接受两个整数参数`a`和`b`，并返回它们的和。你可以使用`abi.encodeWithSelector`来编码函数调用，如下所示：

```solidity
function add(uint a, uint b) public pure returns (uint) {
    return a + b;
}

bytes memory encoded = abi.encodeWithSelector(add.selector, 3, 5);

```



在不知道确切返回值类型的情况下调用函数：

**更一般地说，它允许您通过函数的字符串名称调用函数（类似于 Java 中的反射）**。

```solidity
bytes4 private constant FUNC_SELECTOR = bytes4(keccak256("someFunc(address,uint256)"));

function func(address _contract, address _param1, uint256 _param2) view returns (uint256, uint256) {
    bytes memory data = abi.encodeWithSelector(FUNC_SELECTOR, _param1, _param2);
    (bool success, bytes memory returnData) = address(_contract).staticcall(data);
    if (success) {
        if (returnData.length == 64)
            return abi.decode(returnData, (uint256, uint256));
        if (returnData.length == 32)
            return (abi.decode(returnData, (uint256)), 0);
    }
    return (0, 0);
}
```

