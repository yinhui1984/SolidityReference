---
key: abi.encode
desc: ABI编码函数
---

## 函数原型

```solidity
abi.encode(...) returns (bytes memory)
```

## 说明

 应用二进制接口Application Binary Interface(ABI) 是从区块链外部与合约进行交互以及合约与合约间进行交互的一种标准方式。 

该函数接收任意参数, 参数类型参考https://solidity-cn.readthedocs.io/zh/develop/abi-spec.html#id4, 返回将内存字节序列

返回的长度是 32的整数倍.

## 编码规则

编码规则来参考这里 https://solidity-cn.readthedocs.io/zh/develop/abi-spec.html

> 编码时将数据分为 "静态的" 和 "动态的"
>
> 静态类型会被直接编码，动态类型则会在当前数据块之后单独分配的位置被编码



## 举例

```solidity
function encode(int a, int b) public pure returns (bytes memory){
    return abi.encode(a, b);
}
```

调用 `encode(2,3)` 输出:

```
0x00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003
```



```solidity
function encode(int a, string calldata b) public pure returns (bytes memory){
    return abi.encode(a, b);
}
```

调用 `encode(2,"hello")` 输出:

```
0x00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000568656c6c6f000000000000000000000000000000000000000000000000000000
```





## 在线编码器

https://abi.hashex.org