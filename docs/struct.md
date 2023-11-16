---
key: struct
desc: 结构体
---

在 Solidity 中，结构体（`struct`）可以定义在合约内部或者在合约外部，具体取决于你的需求和设计：

### 在合约内部定义 `struct`

当你在合约内部定义一个 `struct` 时，它只能被这个合约（及其派生的子合约）访问和使用。这种方式通常用于当结构体与特定合约的逻辑紧密相关时。

```
solidityCopy code
contract MyContract {
    struct MyStruct {
        uint a;
        string b;
    }

    // 使用 MyStruct 的函数和变量...
}
```

在这个示例中，`MyStruct` 只能在 `MyContract` 中被访问和使用。

### 在合约外部定义 `struct`

你也可以在合约外部定义一个 `struct`，这样它就可以被多个合约共享。这种方式适用于当多个合约需要使用相同的数据结构时。

```
solidityCopy code
struct SharedStruct {
    uint a;
    string b;
}

contract ContractA {
    // 使用 SharedStruct...
}

contract ContractB {
    // 也使用 SharedStruct...
}
```

在这个例子中，`SharedStruct` 被 `ContractA` 和 `ContractB` 共享。

### 选择哪种方式

选择在合约内部还是外部定义 `struct` 取决于你的具体需求。如果你的结构体仅在一个合约中使用，或者是与特定合约的逻辑密切相关的，那么在合约内部定义可能更合适。相反，如果多个合约需要使用同一个结构体，那么在合约外部定义可以减少代码重复，并提高代码的可维护性。

## 可见性

在 Solidity 中，结构体（`struct`）本身不提供字段级别的可见性控制。结构体中的所有字段默认都是公开的，这意味着它们可以在声明该结构体的合约内部被访问。然而，有几种方法可以间接控制对结构体字段的访问：

### 1. 封装结构体

一种方法是将结构体作为合约的一部分，并通过合约的函数来控制对其字段的访问。在这种情况下，你可以使用函数来控制外部对这些字段的读写访问。

```solidity
solidityCopy code
contract MyContract {
    struct MyStruct {
        uint private data;
    }

    MyStruct private myStruct;

    function setData(uint _data) public {
        myStruct.data = _data;
    }

    function getData() public view returns (uint) {
        return myStruct.data;
    }
}
```

在这个例子中，`MyStruct` 的 `data` 字段是私有的，只能通过 `MyContract` 的 `setData` 和 `getData` 函数来访问和修改。

### 2. 使用内部函数

另一种方式是使用内部（`internal`）函数作为获取和设置结构体字段的方法。这些函数只能在合约内部或从派生合约中被调用。

```solidity
solidityCopy code
contract MyContract {
    struct MyStruct {
        uint data;
    }

    MyStruct private myStruct;

    function _setStructData(uint _data) internal {
        myStruct.data = _data;
    }

    function _getStructData() internal view returns (uint) {
        return myStruct.data;
    }
}
```

在这个例子中，通过内部函数 `_setStructData` 和 `_getStructData` 来控制对 `MyStruct` 中 `data` 字段的访问。

### 3. 使用库

你还可以使用 Solidity 的库来定义结构体和相关的操作。库可以包含一组操作特定数据结构的函数，但不存储状态。

```solidity
solidityCopy code
library MyStructOps {
    struct MyStruct {
        uint data;
    }

    function setData(MyStruct storage self, uint _data) internal {
        self.data = _data;
    }

    function getData(MyStruct storage self) internal view returns (uint) {
        return self.data;
    }
}

contract MyContract {
    using MyStructOps for MyStructOps.MyStruct;

    MyStructOps.MyStruct private myStruct;

    // 使用库函数
}
```

在这种设计中，结构体的操作被封装在库中，而合约通过使用这个库来间接操作结构体。