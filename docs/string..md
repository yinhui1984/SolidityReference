---
key: string, string.concat
desc: string, concat
---





`string`就是动态数组`bytes1[]` 

###  字符串的存储

在Solidity中，字符串的存储位置——`memory`、`storage`和`calldata`——是一个关键概念，它们各有特定的使用场景和内部机制

Storage（存储）

- **定义**：`storage`是永久存储，用于保存合约的状态变量。它是写入区块链的，因此数据持久化并在合约调用之间保持不变。

- **成本**：操作`storage`的成本很高，因为它涉及区块链状态的更改。

- **使用场景**：一般用于存储合约的长期状态，例如用户余额、所有权信息等。

- **特点**：`storage`是默认的存储位置，但在声明局部变量时可以显式指定。

  - String类型的存储布局

    1. **长度和内容的分离**：在`storage`中，`string`类型的实际内容和其长度是分开存储的。对于`string`类型的变量，其本身的存储槽位实际上存储的是字符串的长度（而不是内容）。

    2. **内容的存储位置**：字符串内容的实际存储位置是通过对`string`变量的存储槽位地址进行keccak256哈希计算得出的。具体来说，如果`string`变量的存储槽位是`x`，那么其内容存储的起始位置是`keccak256(x)`。

    3. **动态大小**：`string`类型在`storage`中是动态大小的，这意味着它可以根据需要来增长或缩短。增长可能涉及为字符串分配更多的存储槽位，而缩短则意味着释放一些槽位。

    4. **存储优化**：由于字符串可能占用多个存储槽位（特别是对于较长的字符串），所以在使用`string`类型时要注意合约的存储和Gas成本。

       ```solidity
       pragma solidity ^0.8.10;
       
       contract MyContract {
       //myString变量的存储槽位（假设为0）将包含字符串的长度。字符串"hello"的实际内容（编码为字节）将存储在keccak256(0)计算出的槽位开始的地方。
           string public myString = "hello";
       }
       
       ```

       

Memory（内存）

- **定义**：`memory`是临时存储，用于在函数调用过程中存储数据。一旦函数执行完毕，其中的数据就会消失。
- **成本**：与`storage`相比，读写`memory`的成本较低。
- **使用场景**：常用于存储方法调用期间需要的临时数据，如函数参数、局部变量等。
- **特点**：需要在声明时显式指定为`memory`，尤其是对于引用类型如数组和结构体

Calldata（调用数据）

- **定义**：`calldata`是一个特殊的数据位置，只用于存储外部函数调用的输入参数。
- **成本**：类似于`memory`，但只用于外部函数（`external`）参数。它是只读的且相比于`memory`，使用`calldata`可以节省更多的gas，因为它直接读取交易的输入数据。
- **使用场景**：用于存储`external`函数的参数，特别是在处理大型数组或结构体时更为有效。
- **特点**：`calldata`是不可变的，仅适用于`external`函数的参数。

## 拼接 

可以使用 `abi.encodePacked(str1, str2)` 

```solidity
function concatenate(string memory str1, string memory str2) public pure returns (string memory) {
    return string(abi.encodePacked(str1, str2));
}
```



或从 Solidity 0.8.11 开始


```solidity
string.concat(...) returns (string memory)
```

连接2个或多个字符串,然后返回新的字符串

> 不能用 "+" 连接字符串

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "hardhat/console.sol";

contract MyContract{

    function sayHello(string calldata name)public pure returns (string memory){
        //error when use "+"
        //return "hello," + name;
        return string.concat("hello," , name);
        //也可以用下面这种方式
        //return string(abi.encodePacked("hello,", name));
    }
}

```

## length

获取字符串的长度没有内置函数, 但可以通过将`string`类型转换为`bytes`类型来获取

```solidity
pragma solidity ^0.8.10;

contract StringExample {
    function getLength(string memory str) public pure returns (uint) {
        return bytes(str).length;
    }
}

```

## 哈希 与 比较

比较字符串不像其他语言一样通过`==`而是先计算其哈希值,然后比较哈希

计算字符串的Keccak-256哈希值也是通过将`string`类型转换为`bytes`类型来获取. 或通过 `keccak256(abi.encodePacked(s))`

```solidity
function isEqual(string memory str1, string memory str2) public pure returns (bool) {
    return keccak256(bytes(str1)) == keccak256(bytes(str2));
}
```



## 子字符串

```solidity
function substring(string memory str, uint startIndex, uint endIndex) public pure returns (string memory) {
    bytes memory strBytes = bytes(str);
    bytes memory result = new bytes(endIndex - startIndex);
    for (uint i = startIndex; i < endIndex; i++) {
        result[i - startIndex] = strBytes[i];
    }
    return string(result);
}
```



## 字符串转整数

```solidity
    function StringToInt(string memory s) public pure returns (int) {
        bytes memory stringBytes = bytes(s);
        int result = 0;
        bool negative = false;
        uint startIndex = 0;

        // Check if the string represents a negative number
        if (stringBytes.length > 0 && stringBytes[0] == "-") {
            negative = true;
            startIndex = 1;
        }

        for (uint i = startIndex; i < stringBytes.length; i++) {
            require(
                stringBytes[i] >= "0" && stringBytes[i] <= "9",
                "String must be a valid integer."
            );
            result = result * 10 + (int8(uint8(stringBytes[i])) - 48);
        }

        if (negative) {
            result = -result;
        }

        return result;
    }
```

## 整数转字符串

```solidity
    function IntToString(int i) public pure returns (string memory) {
        if (i == 0) return "0";
        bool negative = i < 0;
        uint len;
        int j = i;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(negative ? len + 1 : len);
        uint k = negative ? len + 1 : len;
        if (negative) {
            i = -i; // Convert to positive to handle the modulus operation
            bstr[0] = bytes1(uint8(45)); // ASCII value for '-'
        }
        while (i != 0) {
            k = k - 1;
            uint8 temp = uint8(48 + uint256(i % 10)); // Convert to uint256 before converting to uint8
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            i /= 10;
        }
        return string(bstr);
    }
```



## 开源库

>字符串操作在EVM上的成本相对较高, 非必要不使用

一个开源库是 https://github.com/Arachnid/solidity-stringutils/blob/master/src/strings.sol
