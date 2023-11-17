---
key: abi.encodeCall
desc: 将函数调用进行ABI编码
---



> abi.encodeCall在 Solidity 0.8.11 中被引入



## 函数原型

```solidity
abi.encodeCall(function functionPointer, (...)) returns (bytes memory)
```

它可以用于对函数调用进行编码，以便将其传递给合约的其他函数或通过Ethereum的调用或事务发送到其他合约

`functionPointer`是要调用的函数的指针，这是一个函数类型的参数。后面的括号中的三个点表示可变参数列表，即函数调用中传递的参数。此函数返回类型为`bytes memory`，返回一个字节数组，其中包含对函数调用进行编码的结果。



## 举例

假设我们有以下合约：

```solidity
pragma solidity ^0.7.0;

contract Example {
    function add(uint a, uint b) public pure returns (uint) {
        return a + b;
    }
}

```

我们可以使用`abi.encodeCall`函数来对合约中的`add`函数进行编码，然后将其传递给另一个函数或通过Ethereum调用发送到另一个合约。例如：

```solidity
Example example = new Example();
bytes memory callData = abi.encodeCall(example.add, 10, 20);
```

变量`callData`将包含编码后的函数调用，其中包括函数名称和参数。你可以将这个字节数组传递给另一个函数，或者使用`eth.call`或`eth.sendTransaction`发送到另一个合约

比如

```solidity
(bool success, bytes memory ret) = address(example).staticcall(callData);
assertEq(success, true);
uint sum = abi.decode(ret, (uint256));
console2.log(sum);
assertEq(sum, 30);
```





## bug

https://blog.soliditylang.org/2022/03/16/encodecall-bug/

## encodeCall  encodeWithSignature   encodeWithSelector

`abi.encodeCall`、`abi.encodeWithSignature` 和 `abi.encodeWithSelector` 在 Solidity 中都用于编码函数调用

比如有一个函数Add

```solidity
function Add(uint a, uint b) public pure returns (uint) {
        return a + b;
}
```

通过下面这三种方式

```solidity
abi.encodeCall(this.Add, (1, 2));
abi.encodeWithSignature("Add(uint256,uint256)", 1, 2);
abi.encodeWithSelector(this.Add.selector, 1, 2);
```

得到的结果都是一样的

```
0x7afbe4f100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002
```



但它们各有特点和使用场景。理解它们之间的关系有助于选择最适合特定需求的编码方法。

### abi.encodeCall

- **用途**：`abi.encodeCall` 用于安全地编码函数调用，包括函数选择器和参数。

- **特点**：它在编译时进行类型检查，确保参数类型与函数签名匹配，增加了调用的安全性。

- 示例：

  ```solidity
  solidityCopy code
  bytes memory callData = abi.encodeCall(SomeContract.someFunction, (arg1, arg2));
  ```

### abi.encodeWithSignature

- **用途**：`abi.encodeWithSignature` 用于编码函数调用，需要手动提供函数签名的字符串表示。

- **特点**：它在运行时将字符串转换为函数选择器，但不提供编译时的类型安全检查。

- 示例：

  ```solidity
  solidityCopy code
  bytes memory callData = abi.encodeWithSignature("someFunction(uint256,address)", arg1, arg2);
  ```

### abi.encodeWithSelector

- **用途**：`abi.encodeWithSelector` 用于编码函数调用，需要手动提供函数选择器。

- **特点**：与 `abi.encodeWithSignature` 类似，它允许更精确地控制函数选择器，但同样没有编译时的类型安全检查。

- 示例：

  ```solidity
  solidityCopy code
  bytes4 selector = bytes4(keccak256("someFunction(uint256,address)"));
  bytes memory callData = abi.encodeWithSelector(selector, arg1, arg2);
  ```

### 关系和选择

- **安全性**：`abi.encodeCall` 提供最高的安全性，因为它在编译时进行类型检查。
- **灵活性**：`abi.encodeWithSignature` 和 `abi.encodeWithSelector` 提供更高的灵活性，允许在运行时指定函数签名或选择器，但牺牲了类型安全。
- 使用场景：
  - 使用 `abi.encodeCall` 当你需要类型安全且明确知道要调用的函数。
  - 使用 `abi.encodeWithSignature` 或 `abi.encodeWithSelector` 当你需要在运行时动态确定函数调用或处理更复杂的交互场景。



## 编码函数的显示举例

以下是一些主要使用场景：

### 1. 智能合约函数调用

在以太坊中，当一个外部账户（比如用户的钱包）或另一个智能合约需要调用合约中的函数时，这个调用需要被编码为一串特定格式的字节码。这个编码过程包括函数选择器（即函数签名的哈希）和任何传递给函数的参数。

### 2. 构造交易

当通过区块链发送一个交易以调用智能合约的函数时，交易的数据字段需要包含对该函数调用的编码。这就是为什么你在区块链浏览器上看到的交易数据通常是一串十六进制编码：它代表了函数调用的编码形式。

### 3. 代理合约（Proxy Contracts）

在代理合约模式中，一个智能合约（代理）会将所有调用转发到另一个合约（逻辑合约）。这通常涉及使用 `delegatecall` 和对函数调用的编码。代理合约需要知道要调用哪个函数以及需要哪些参数，这就需要使用函数编码。

### 4. 底层调用

当使用底层函数（如 `call`、`delegatecall` 或 `staticcall`）进行更灵活或更底层的合约交互时，开发者需要手动编码这些调用。这对于高级功能，如合约升级或特定的交互模式（如跨合约查询）非常重要。

### 5. 多调用（Multicalls）

在进行一次事务中包含多个函数调用时（通常用于优化交易和减少gas成本），开发者会预先编码这些函数调用，并将编码后的数据作为一个单一事务发送。

### 6. 签名和验证

在某些情况下，函数调用需要在链外签名，然后在链上验证。这通常涉及到对函数参数进行编码，以便正确地生成或验证签名。