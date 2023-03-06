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

