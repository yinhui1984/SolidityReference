---
key: abi.decode
desc: 使用提供的类型对ABI编码的数据进行解码
---

## 函数原型

```solidity
abi.decode(bytes memory encodedData, (type1,type2...)) returns (...)
```



## 说明

它接收一个字节数组，其中包含编码后的数据，以及一个包含解码数据预期类型的元组。它返回一个元组，其中包含与预期类型相同顺序的解码数据。

> 重要的, 传入的类型列表要匹配, 否则可能发生非预期的行为



## 举例

```solidity
function decode(bytes calldata data) public pure returns (int, string memory ){
    return abi.decode(data, (int, string));
}
```

调用`decode`传入

```
0x00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000568656c6c6f000000000000000000000000000000000000000000000000000000
```

输出: `2, "hello"`



## 在线解码器

https://adibas03.github.io/online-ethereum-abi-encoder-decoder/#/decode

