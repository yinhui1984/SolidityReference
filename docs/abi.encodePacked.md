---
key: abi.encodePacked
desc: ABI紧打包编码函数
---

## 函数原型

```solidity
abi.encodePacked(...) returns (bytes)
```

## 说明

### 关于编码 

参考 "abi.encode"

### 关于紧打包

非标准打包模式: https://docs.soliditylang.org/en/v0.8.15/abi-spec.html#strict-encoding-mode

Solidity 支持一种非标准打包模式：

- 短于32字节的类型被直接连接，没有填充或符号扩展。
- 动态类型是就地编码的，没有长度。
- 数组元素被填充，但仍被就地编码

>如果你使用keccak256(abi.encodePacked(a, b))，并且a和b都是动态类型，那么很容易通过将a的一部分移到b中，反之亦然，从而在哈希值中精心设计碰撞。更具体地说，abi.encodePacked("a", "bc") == abi.encodePacked("ab", "c")。如果你将abi.encodePacked用于签名、认证或数据完整性，确保总是使用相同的类型，并检查其中最多一个是动态的。除非有令人信服的理由，否则应该首选abi.encode。

