---
key: delete
desc: 重置
---

`delete`关键字表示将值进行重置, 而不是删除



https://docs.soliditylang.org/zh/latest/types.html#delete

在Solidity中，`delete` 关键字的行为取决于它作用的数据类型。

### 删除变量

- **基本类型**：对于基本类型（如整数），`delete a` 将变量 `a` 重置为其类型的初始值。例如，对于整数，这相当于 `a = 0`。
  
  **示例**:
  ```solidity
  uint a = 5;
  delete a; // 现在 a == 0
  ```

- **数组**：对于数组，`delete a` 行为不同，具体取决于数组是动态数组还是静态数组。
  - 对于**动态数组**，它将数组长度设为 `0`，但不会改变已分配的内存。
  - 对于**静态数组**，它将数组的每个元素重置为类型的初始值，但数组长度保持不变。
  
  **示例**:
  ```solidity
  uint[] dynamicArray;
  uint[5] staticArray;
  delete dynamicArray; // 动态数组现在长度为 0
  delete staticArray;  // 静态数组的每个元素现在都是 0，长度仍为 5
  ```

### 删除数组元素

- 使用 `delete a[x]` 可以删除数组 `a` 中索引为 `x` 的元素。这会将元素重置为其类型的初始值，但不会改变数组的长度。

  **示例**:
  ```solidity
  uint[] numbers = [1, 2, 3];
  delete numbers[1]; // 数组现在是 [1, 0, 3]
  ```

### 结构体

- 对于结构体，`delete a` 将结构体中的所有属性重置为初始值。如果结构体包含映射，映射成员不受影响。

  **示例**:
  ```solidity
  struct MyStruct {
      uint num;
      mapping(address => uint) map;
  }
  MyStruct data;
  delete data; // data.num 被重置为 0，data.map 不受影响
  ```

### 映射

- 对于映射，`delete a[x]` 将删除键 `x` 对应的值，但 `delete a` 对映射本身没有影响。

  **示例**:
  
  ```solidity
  mapping(address => uint) balances;
  delete balances[userAddress]; // 删除 userAddress 的余额
  ```

### 引用变量

- 对于引用变量（如结构体或数组的引用），`delete a` 只会重置引用本身，而不影响它所指向的数据。

### 总结

`delete` 在Solidity中的行为实际上是对变量进行赋值操作，即将新的默认值存储在变量中。这在处理引用类型时尤其重要，因为 `delete` 只重置引用，而不改变引用指向的数据。



> 在Solidity中，您只能删除存储引用指向的数据（如 `delete dataArray;`），而不能删除存储引用本身

比如下面的`delete y`是非法的

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.0 <0.9.0;

contract DeleteExample {
    uint data;
    uint[] dataArray;

    function f() public {
        uint x = data;
        delete x; // 将 x 设为 0，并不影响data变量
        delete data; // 将 data 设为 0，并不影响 x
        uint[] storage y = dataArray;
        delete dataArray; // 将 dataArray.length 设为 0，但由于 uint[] 是一个复杂的对象，
        // y 也将受到影响，它是一个存储位置是 storage 的对象的别名。
        // 另一方面："delete y" 是非法的，引用了 storage 对象的局部变量只能由已有的 storage 对象赋值。
        assert(y.length == 0);
    }
}
```

在上面的例子中, 

`uint[] storage y = dataArray;` 这行代码创建了一个指向 `dataArray` 的存储（`storage`）指针。在Solidity中，`storage`引用是路径依赖的，它们不是独立的数据副本，而是直接指向存储在区块链上的数据。因此，`y` 实际上是 `dataArray` 的一个别名（或引用），它们指向相同的数据。

当执行 `delete dataArray;` 时，它将 `dataArray` 的长度设置为0。由于 `y` 是 `dataArray` 的别名，这也影响了 `y`。在这种情况下，`y` 依然指向 `dataArray`，但是由于 `dataArray` 现在是一个空数组，`y` 的长度也为0。

`delete y;` 被认为是非法的，因为 `y` 是一个指向存储（`storage`）的引用，而不是一个独立的变量。在Solidity中，您不能删除存储引用本身，只能删除存储引用所指向的内容。由于 `y` 只是 `dataArray` 的一个别名，删除 `y` 就相当于尝试删除 `dataArray` 的引用本身，而不是它的内容。这是不允许的，因为 `storage` 引用应该总是指向一个有效的存储位置。

简而言之，`delete y;` 是非法的，因为它尝试删除一个 `storage` 引用，而不是它所指向的数据。在Solidity中，您只能删除存储引用指向的数据（如 `delete dataArray;`），而不能删除存储引用本身。