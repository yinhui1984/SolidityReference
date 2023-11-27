---
key:slot
desc:slot
---

https://solidity-by-example.org/app/write-to-any-slot/



Solidity 存储就像一个长度为 2^256 的数组。数组中的每个槽可以存储 32 个字节。
声明的顺序和状态变量的类型定义了它将使用哪些插槽。
但是使用汇编，您可以写入任何插槽。

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

library StorageSlot {
    // Wrap address in a struct so that it can be passed around as a storage pointer
    struct AddressSlot {
        address value;
    }

    function getAddressSlot(
        bytes32 slot
    ) internal pure returns (AddressSlot storage pointer) {
        assembly {
            // Get the pointer to AddressSlot stored at slot
            pointer.slot := slot
        }
    }
}

contract TestSlot {
    bytes32 public constant TEST_SLOT = keccak256("TEST_SLOT");

    function write(address _addr) external {
        StorageSlot.AddressSlot storage data = StorageSlot.getAddressSlot(TEST_SLOT);
        data.value = _addr;
    }

    function get() external view returns (address) {
        StorageSlot.AddressSlot storage data = StorageSlot.getAddressSlot(TEST_SLOT);
        return data.value;
    }
}

```



> 参考这篇文章:  https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/



## slot的分配与存储

在Solidity中，`storage` 的槽（slot）分配和存储方式主要遵循以下规则：

1. **固定大小变量的槽分配**：
   - 固定大小的状态变量（如 `uint256`、`address`）按照它们在合约中声明的顺序被分配到连续的槽中。每个变量占用一个槽，每个槽大小为32字节。
   - 结构体（`struct`）和固定大小数组会占用多个连续的槽，根据它们的成员或元素数量。

2. **动态大小变量的存储**：
   - 动态大小的数组和 `mapping` 使用一种特殊的哈希机制来确定它们的存储位置。
   - 对于动态数组，它的长度存储在一个固定的槽中，而数组元素的位置是通过哈希其索引来计算的。
   - 对于 `mapping`，它的每个元素的位置是通过哈希其键（和其他信息）来计算的。

3. **存储位置的计算**：
   - 动态数组和 `mapping` 的元素位置通常是通过将其键或索引与一个固定值（如数组或 `mapping` 的起始槽地址）一起哈希计算得出的。

4. **存储优化**：
   - Solidity会尝试优化存储布局以减少空间消耗。例如，多个较小的变量可能会被打包进同一个槽中。

这些规则确保了存储的有效利用和快速访问，但也意味着合约开发者需要仔细考虑变量的声明顺序和类型，以优化Gas消耗和存储使用。

> 动态数组的存储位置计算遵循特定的算法：
>
> 1. **数组长度的存储**：
>    - 动态数组的长度存储在数组的起始槽（slot）中。这个槽的位置是根据数组在合约中声明的顺序决定的。
> 2. **数组元素的位置计算**：
>    - 动态数组的每个元素的存储位置是通过哈希计算得出的。具体算法是：对数组起始槽的地址进行keccak256哈希运算，然后加上元素的索引。换句话说，数组元素的位置是 `keccak256(hash(starting_slot) + index)`，其中 `starting_slot` 是数组起始槽的位置，`index` 是数组元素的索引。
>
> 通过这种方式，Solidity确保动态数组的元素可以在巨大的存储空间中有效地定位，同时避免了潜在的存储位置冲突。



> `mapping` 的每个元素的存储位置是通过特定的哈希算法来计算的。这个算法如下：
>
> 1. **基本算法**：
>
>    - 对于一个 `mapping` 类型的变量，它的每个元素的存储位置是通过对键（key）和 `mapping` 变量自身的存储起始槽地址进行keccak256哈希运算来确定的。
>
> 2. **具体计算**：
>
>    ```solidity
>    function mapLocation(uint256 slot, uint256 key) public pure returns (uint256) {
>        return uint256(keccak256(abi.encodePacked(key, slot)));
>    }
>    ```
>
>    
>
>    - 计算公式为 `keccak256(hash(key) + hash(starting_slot))`，其中 `starting_slot` 是 `mapping` 变量的起始槽地址。
>    - 这里的 `+` 操作是指将 `key` 的哈希值和 `starting_slot` 的哈希值串联在一起，然后对整个串联的结果进行哈希运算。
>
> 这种方法可以确保 `mapping` 中每个键值对的位置是唯一的，且可以在巨大的存储空间中有效地定位，同时避免存储位置的冲突。
