---
key: mapping
desc: mapping
---

```solidity
mapping(T1 => T2) mymap
```



在Solidity中，`mapping` 是一种非常重要且常用的数据结构，用于存储键值对。以下是关于 `mapping` 的详细说明：

### 定义和基本特性

1. **基本定义**：
   - `mapping` 是一个键值存储结构，类似于其他编程语言中的哈希表或字典。
   - 它以 `mapping(KeyType => ValueType)` 的形式定义，其中 `KeyType` 可以是几乎所有的 Solidity 基本类型，而 `ValueType` 可以是任何类型，包括另一个 `mapping`。

2. **键（Key）的特性**：
   - 键类型必须是一个“值类型”，比如 `uint`, `address` 或 `bytes`。它不能是引用类型，比如数组、结构体或其他 `mapping`。
   - `mapping` 中的键是唯一的，且每个键都会映射到一个值。

3. **值（Value）的特性**：
   - 值可以是任何类型，包括基本类型、数组、结构体或其他 `mapping`。
   - 如果没有显式设置，默认值取决于值的类型。例如，`uint` 类型的默认值是 `0`。

### 使用和访问

1. **初始化**：
   - `mapping` 不需要初始化或预设大小，它理论上可以存储无限数量的键值对。
   - 在创建 `mapping` 时，其实并没有为每个可能的键分配存储空间，只有在键实际被使用时才会分配存储空间。

2. **读取和设置值**：
   - 通过 `mapping[key]` 的方式来读取或设置键对应的值。
   - 如果尝试读取一个未被设置的键，将返回值类型的默认值。

3. **特殊性质**：
   - 与传统的哈希表不同，Solidity 中的 `mapping` 实际上不能追踪存储的键，也就是说你不能遍历 `mapping`，也不能获取其大小。
   - 由于这个特性，通常需要额外的数据结构来跟踪已使用的键。

### 限制和注意事项

1. **不可迭代**：
   - 如上所述，不能遍历 `mapping`。如果需要遍历或获取所有键值对，通常需要结合使用数组或其他方式来记录所有键。

2. **不可删除**：
   - `mapping` 中的元素不能被删除。设置键对应的值为其类型的默认值（比如 `uint` 的 `0`，`address` 的 `address(0)`）通常被视为等效于删除。

3. **不可作为函数参数或返回值**：
   - 不能将 `mapping` 直接作为外部函数的参数或返回值。这是因为 `mapping` 的大小和结构都是不确定的。

4. **存储位置**：
   - `mapping` 只能存储在 `storage` 中，即只能作为状态变量或者在存储指针中使用。

### 应用场景

1. **数据关联**：
   - `mapping` 非常适合用于关联唯一标识符（如用户地址）到用户信息（如余额或投票权）。

2. **数据存储和访问**：
   - 在需要快速查找和更新数据时，`mapping` 提供了一种有效的方式。





```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Temp {
    mapping(uint256 => uint256) map;

    function insertToMap(uint256 _key, uint256 _value) public {
        //key不存在则插入， 存在则更新
        map[_key] = _value;
    }

    function getFromMap(uint256 _key) public view returns (uint256) {
        //获取值， 如果key不存在则会返回value的默认值
        return map[_key];
    }

    function deleteFromMap(uint256 _key) public {
        //无论key是否存在，都是将map[_key]重置为默认值
        delete map[_key];
    }
}

```

官方文档

https://docs.soliditylang.org/en/v0.8.17/types.html?highlight=delete#mapping-types



## key 和value允许的类型

![](https://github.com/yinhui1984/imagehosting/blob/main/images/1672293665096381000.jpg)

https://github.com/yinhui1984/imagehosting/blob/main/images/1672293665096381000.jpg



## Iterable Mappings

https://docs.soliditylang.org/en/v0.8.17/types.html#iterable-mappings



## 存储 (storage)

参考:  https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/

总的说来

mapping 声明的位置对应的slot内容为空

根据key和slot的hash来对key对应是实际存储位置进行定位

```solidity
//伪代码
function mapLocation(uint256 slot, uint256 key) public pure returns (uint256) {
    return uint256(keccak256(key, slot));
}
```

更多的, 参考 storage.md
