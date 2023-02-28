---
key: selector
desc: 函数选择器
---



https://solidity-by-example.org/function-selector/

当一个函数被调用时，`calldata`的前4个字节指定要调用哪个函数。这4个字节被称为**函数选择器**。

以下面这段代码为例。它使用call来执行地址为addr的合约上的transfer函数。

```solidity
addr.call(abi.encodeWithSignature("transfer(address,uint256)", 0xSomeAddress, 123))
```

从`abi.encodeWithSignature(....)`返回的前**4**个字节是函数选择器。

如果你在代码中预先计算并内联函数选择器，也许你可以节省少量的gas？

以下是函数选择器的计算方法。

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FunctionSelector {
    /*
    "transfer(address,uint256)"
    0xa9059cbb
    "transferFrom(address,address,uint256)"
    0x23b872dd
    */
    function getSelector(string calldata _func) external pure returns (bytes4) {
        return bytes4(keccak256(bytes(_func)));
    }
}
```

solidity 中如果能访问到合约或接口代码, 可以如下调用直接返回函数选择器

```solidity
bytes4 _sig = myContract.ownerOf.selector
```

