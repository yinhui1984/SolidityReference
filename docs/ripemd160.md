---
key: ripemd160
desc: 计算hash值
---

```solidity
ripemd160(bytes memory) returns (bytes20)
```



>注意返回的是`bytes20`



Ripemd-160 和 Keccak-256 是两种不同的哈希算法，它们用于将任意长度的输入数据映射为固定长度的输出数据（哈希值）。它们有一些区别：

- Ripemd-160 算法用于生成 160 位哈希值，而 Keccak-256 算法用于生成 256 位哈希值。
- Ripemd-160 算法由欧洲研究机构开发，用于替代传统的 MD5 和 SHA-1 算法。Keccak-256 算法是 SHA-3 算法的变体，由 NIST（美国国家标准与技术研究院）开发，用于替代现有的 SHA-1 和 SHA-2 算法。
- Ripemd-160 算法被广泛用于认证和数据完整性保护等方面。Keccak-256 算法在以太坊中被广泛使用，用于确定地址、计算块头哈希值、生成随机数等。
- Ripemd-160 和 Keccak-256 算法的哈希值长度不同，且其计算方式略有不同。





## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract MyContract{

    function getHash(string calldata _input) public pure returns (bytes32, bytes20) {
        bytes memory bs = abi.encodePacked(_input);
        return (keccak256(bs), ripemd160(bs));
    }
}

```

调用 `getHash("hello")` 输出

```

0:
bytes32: 0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8
1:
bytes20: 0x108f07b8382412612c048d07d13f814118445acd
```



> 在ganache上运行上面的例子时, 可能遇到错误
>
> `Error: Digest method not supported`
>
> 请换用`Remix EVM (London)` 节点