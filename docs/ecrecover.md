---
key: ecrecover
desc: 从椭圆曲线签名中恢复与公钥相关的地址
---

```solidity
ecrecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) returns (address)
```

用于从给定的数据中恢复出椭圆曲线签名的发送方地址。

该函数接受四个参数：

- `hash`：要签名的数据的哈希值。
- `v`：签名中的 V 值, 表示签名使用的私钥的类型。
- `r`：签名中的 R 值, 表示签名的一部分。
- `s`：签名中的 S 值, 表示签名的另一部分。



签名的 V 值、R 值和 S 值可以通过使用私钥对数据进行签名获得。例如，你可以使用以下代码生成签名：

```solidity
pragma solidity ^0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/cryptography/ECDSA.sol";

contract Signer {
    // 生成签名
    function sign(bytes32 message, address signer) public view returns (uint8 v, bytes32 r, bytes32 s) {
        (v, r, s) = ECDSA.sign(message, signer);
    }
}

```





假设你有一个合约，其中有一个函数可以接受用户的投票。你希望通过使用签名来验证用户的身份，以确保只有合法用户才能进行投票。

```solidity
pragma solidity ^0.6.0;

contract Voting {
    // 保存用户的投票结果
    mapping(address => bool) public votes;

    // 允许用户投票
    function vote(uint8 v, bytes32 r, bytes32 s) public {
        // 使用 ecrecover 函数恢复签名的发送方地址
        address sender = ecrecover(abi.encodePacked(msg.sender), v, r, s);

        // 只有合法用户才能投票
        require(sender == msg.sender, "Invalid signature");

        // 保存用户的投票结果
        votes[sender] = true;
    }
}

```

