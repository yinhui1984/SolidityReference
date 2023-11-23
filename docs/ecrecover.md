---
key: ecrecover
desc: 从椭圆曲线签名中恢复出签名者的地址
---

```solidity
ecrecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) returns (address)
```

用于从给定的数据中恢复出椭圆曲线签名的发送方地址。

该函数接受四个参数：

- `hash`：这是签名之前的原始消息的散列值。通常，这个散列是使用 `keccak256` 算法得到的。
- `v`：签名中的 V 值, 表示签名使用的私钥的类型。它是一个用于区分公钥的小整数。在以太坊中，`v` 通常是 27 或 28。(它告诉我们在恢复公钥时应该使用椭圆曲线上的哪一半。这是因为在计算 `r` 时，我们丢失了点 `(x, y)` 的 `y` 坐标的符号信息。`v` 帮助我们确定正确的 `y` 坐标。)
- `r`：签名中的 R 值, 表示签名的一部分。`s`：签名中的 S 值, 表示签名的另一部分。这两个参数组成了实际的数字签名。它们是从签名过程中生成的，通常由签名者的私钥生成。

当调用 `ecrecover` 函数时，它会计算并返回一个地址，这个地址是与给定的签名（由 `r`、`s` 和 `v` 参数表示）相对应的以太坊地址。如果签名是由该地址的私钥创建的，那么 `ecrecover` 将返回该地址。如果签名无效或不匹配，它将返回零地址（0x0）。



签名的 V 值、R 值和 S 值可以通过使用私钥对数据进行签名获得。例如，你可以使用以下代码生成签名：

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.10;

import "forge-std/Test.sol";
import "src/ecrecoverDemo.sol";

contract EcrecoverDemoTest is Test {
    EcrecoverDemo ecd;

    function setUp() public {
        vm.createSelectFork("theNet");

        ecd = new EcrecoverDemo();
    }

    function testRecover() public {
        (address alice, uint256 alicePrivateKey) = makeAddrAndKey("alice");
        bytes32 hash = keccak256(abi.encodePacked("hello world"));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(alicePrivateKey, hash);
        address addr = ecd.RecoverFromMessage("hello world", v, r, s);
        console2.logAddress(addr);
        assertTrue(addr == alice);

        addr = ecd.RecoverFromMessage("hello world!!", v, r, s);
        console2.logAddress(addr);
        assertTrue(addr != alice);
    }
}


```

然后在合约中, 你可以通过v,r,s反推出对消息签名的地址:

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.10;

// import "lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol";

contract EcrecoverDemo {
    function RecoverFromMessage(
        string calldata message,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        bytes32 hash = keccak256(abi.encodePacked(message));
        return ecrecover(hash, v, r, s);
    }
}

```



另外一个例子:

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

与其对应的签名代码如下:

```js
const ethers = require('ethers');

async function signVote(account, provider) {
   //privateKey不要在前端代码中暴露。通常，签名会在用户的客户端环境（如使用 MetaMask）或在服务器端进行
    const signer = new ethers.Wallet(account.privateKey, provider);

    // 与 Solidity 合约中相同的消息，例如用户的地址
    const message = ethers.utils.arrayify(signer.address);

    // 签名消息
    const signature = await signer.signMessage(message);

    // 将签名分解为 v, r, s 组件
    const sig = ethers.utils.splitSignature(signature);

    return {
        v: sig.v,
        r: sig.r,
        s: sig.s
    };
}
```



## v, r, s 与signature

有时候我们会看到一些函数返回的是`signature`, 有时候返回的是`v, r, s`

它们的关系如下:

完整的签名通常表示为一串字节，其中包含 `r`, `s`, 和 `v` 的值。在以太坊中，这通常被编码为 65 字节的字符串：前 32 字节是 `r`，接下来的 32 字节是 `s`，最后一个字节是 `v`。





## 拓展:椭圆曲线数字签名算法 (chatgpt)

椭圆曲线数字签名算法（ECDSA）是一种在加密货币和网络安全中非常重要的技术，它可以被类比为一种特殊的锁和钥匙系统。其核心原理涉及椭圆曲线加密（ECC）和数字签名的概念，为了便于程序员理解，我们可以从数学和算法的角度来探讨它。

### 椭圆曲线的基础

- **选择特定的椭圆曲线**：ECDSA 通常基于特定的椭圆曲线，如 secp256k1（在比特币和以太坊中使用）。这些曲线在有限域上定义，具有特定的数学属性。
- **数学方程**：在 ECC 和 ECDSA 中，椭圆曲线通常通过 \(y^2 = x^3 + ax + b\) 的方程定义。
- **曲线的性质**：曲线的参数 \(a\) 和 \(b\) 以及曲线本身必须满足一定条件，如没有奇点。

### 密钥对的生成

- **私钥**：私钥是一个随机选取的数 \(k\)，通常介于 1 和曲线阶数之间。
- **公钥**：公钥由椭圆曲线上的点乘运算得出，即私钥 \(k\) 乘以曲线上的基点 \(G\)。

### 签名的生成和验证

- **哈希函数**：首先对消息进行哈希处理（如 SHA-256 或 Keccak-256）。
- **签名创建**：使用私钥和消息的哈希通过复杂的数学运算（模运算、点乘等）生成两个数值 \(r\) 和 \(s\)，构成签名。
- **验证过程**：接收方使用公钥和消息的哈希，通过一系列计算（点加和点乘）来验证 \(r\) 和 \(s\) 是否与公钥和消息哈希相匹配。

### 数学原理

- **点运算**：椭圆曲线上的运算（点加和点乘）满足特定的数学性质，如闭合性。
- **离散对数问题**：从公钥推算出私钥在计算上不可行，因为这涉及解决椭圆曲线离散对数问题（ECDLP），一个计算上极其困难的问题。

### 安全性和实用性

- **ECDSA 的安全性**：依赖于椭圆曲线的数学难题和私钥的保密性。
- **适用性**：ECDSA 提供了高效的密钥大小和安全性，是许多现代加密系统的基础。

### 签名组件：v, r, 和 s

- **签名的组成**：在以太坊的 ECDSA 中，签名由三个部分组成：\(r\)、\(s\) 和恢复标识符 \(v\)。
- **生成过程**：在签名过程中，私钥和消息的哈希值被用来生成 \(r\) 和 \(s\)。
- **公钥恢复**：\(v\) 用于确定椭圆曲线上哪一半被用于生成签名，帮助恢复公钥。
- **恢复公钥**：通过 \(r\)、\(s\) 和 \(v\)，可以逆向推导出用于生成公钥的私钥。

总体来说，ECDSA 就像是一个高度安全的锁和钥匙系统，它允许人们安全地签名和验证信息，而不用担心私钥被盗或签名被
