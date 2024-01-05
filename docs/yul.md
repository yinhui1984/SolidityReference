---
key: yul
desc: yul的函数解释和举例
---



https://docs.soliditylang.org/zh/latest/yul.html#

https://docs.soliditylang.org/zh/latest/yul.html#evm



> 下面函数中的参数和返回值默认都是 uint256 (对应yul的u256)

## stop()

1. 不接受参数。
2. 不返回任何值。
3. 用于安全地停止合约的执行并返回控制权给EVM。

```solidity
    function Stop() public pure {
        assembly {
            stop()
            // unreachable code
            //revert(0, 0)
        }
    }
```



## add(x, y)

1. **参数**:
   - `x`: 第一个加数，一个整数值。
   - `y`: 第二个加数，同样是一个整数值。
2. **返回值**:
   - 函数返回 `x` 和 `y` 两个值的和。这个和是一个整数，如果结果超过了EVM的单个槽位能存储的最大值（通常是256位），则会自动模256位整数大小。这意味着加法是模运算，可能会出现溢出。在EVM中，如果加法的结果超过了256位，它不会抛出错误，而是简单地回绕到最小值。这种行为在某些情况下可能导致逻辑错误或安全漏洞。

```solidity
    function Add(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := add(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testAdd() public {
        // 正常
        uint256 result = demo.Add(1, 2);
        assertTrue(result == 3, "result should be 3");

        // 溢出
        result = demo.Add(
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            1
        );
        console2.logUint(result);
        assertTrue(result == 0, "result should be 0");

        result = demo.Add(
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            2
        );
        console2.logUint(result);
        assertTrue(result == 1, "result should be 1");
    }
```



## sub(x, y)

1. **参数**:
   - `x`: 被减数，一个整数值。
   - `y`: 减数，同样是一个整数值。
2. **返回值**:
   - 函数返回 `x` 减去 `y` 的差值。这个差值是一个整数，如果结果是一个负数，则会按照256位整数的模进行计算。这意味着减法也是模运算，可能会出现下溢。在EVM中，如果减法的结果是负数，它不会抛出错误，而是从最大的256位整数开始回绕。这种行为在某些情况下可能导致逻辑错误或安全漏洞。

```solidity
    function Sub(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := sub(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testSub() public {
        // 正常
        uint256 result = demo.Sub(3, 2);
        assertTrue(result == 1, "result should be 1");

        // 溢出
        result = demo.Sub(1, 2);
        console2.logUint(result);
        assertTrue(
            result ==
                0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            "result should be 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        );
    }
```



## mul(x,y)

1. **参数**:
   - `x`: 第一个乘数，一个整数值。
   - `y`: 第二个乘数，同样是一个整数值。
2. **返回值**:
   - 函数返回 `x` 和 `y` 两个值的乘积。这个乘积是一个整数，如果结果超过了EVM的单个槽位能存储的最大值（通常是256位），则会自动模256位整数大小。这意味着乘法是模运算，可能会出现溢出。在EVM中，如果乘法的结果超过了256位，它不会抛出错误，而是简单地回绕到最小值。这种行为在某些情况下可能导致逻辑错误或安全漏洞。

```solidity
    function Mul(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := mul(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testMul() public {
        // 正常
        uint256 result = demo.Mul(3, 2);
        assertTrue(result == 6, "result should be 6");

        // 溢出
        result = demo.Mul(
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            2
        );
        console2.logUint(result);
        assertTrue(
            result <
                0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            "result should be less than 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        );
    }
```



### div(x,y)

1. **参数**:
   - `x`: 被除数，一个整数值。
   - `y`: 除数，也是一个整数值。
2. **返回值**:
   - 函数返回 `x` 除以 `y` 的商。这个商是一个整数，Yul中的除法是**向下取整的**，即如果有余数，会舍弃不计。
3. **注意事项**:
   - **如果 y == 0，则为 返回 0**
   - 和其他算术操作一样，需要注意256位整数的限制。虽然除法不太可能导致溢出，但在特定的上下文中处理大数时还是要小心。

```solidity
    function Div(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := div(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testDiv() public {
        // 正常
        uint256 result = demo.Div(6, 2);
        assertTrue(result == 3, "result should be 3");

        // 向下取整
        result = demo.Div(5, 2);
        assertTrue(result == 2, "result should be 2");
    }

    function testDiv0() public view {
        // 除数为0, 返回0
        uint256 result = demo.Div(6, 0);
        console2.logUint(result);
    }
```



## sdiv(x,y)

用于处理**有符号整数**的除法运算。

1. **参数**:
   - `x`: 被除数，一个有符号整数值。
   - `y`: 除数，也是一个有符号整数值。
2. **返回值**:
   - 函数返回 `x` 除以 `y` 的商。与 `div` 不同，`sdiv` 处理的是有符号整数，所以它可以正确处理负数。如果 `x` 和 `y` 有一个是负数，返回的商将是负数。如果两者都是负数，返回的商将是正数。
3. **注意事项**:
   - **如果 y == 0，则为 返回 0**
   - 由于EVM中的整数都是256位的，`sdiv` 在处理非常大的数或非常小的负数时也需要小心，以防止意外行为。

```solidity
    function Sdiv(int256 a, int256 b) public pure returns (int256) {
        int256 result;
        assembly {
            let sum := sdiv(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testSdiv() public {
        // 正常
        int256 result = demo.Sdiv(6, 2);
        assertTrue(result == 3, "result should be 3");

        // 向下取整
        result = demo.Sdiv(5, 2);
        assertTrue(result == 2, "result should be 2");

        // 负数
        result = demo.Sdiv(-5, 2);
        assertTrue(result == -2, "result should be -2");
    }

    function testSdiv0() public {
        // 除数为0, 返回0
        int256 result = demo.Sdiv(6, 0);
        assertTrue(result == 0, "result should be 0");
    }
```



## mod(x, y)

取模运算(求余数)

1. **参数**:
   - `x`: 被模数，一个整数值。
   - `y`: 模数，也是一个整数值。
2. **返回值**:
   - 函数返回 `x` 对 `y` 取模的结果。这个结果是两数相除后的余数，总是非负的，即使 `x` 是负数。
3. **注意事项**:
   - **如果 y == 0，则为 返回 0**
   - 和其他算术操作一样，需要注意256位整数的限制。模运算通常不会导致溢出，但在特定的上下文中仍需谨慎处理大数

```solidity
    function Mod(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := mod(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testMod() public {
        uint256 result = demo.Mod(6, 2);
        assertTrue(result == 0, "result should be 0");

        result = demo.Mod(5, 2);
        assertTrue(result == 1, "result should be 1");
    }

    function testMod0() public {
        // 除数为0, 返回0
        uint256 result = demo.Mod(6, 0);
        assertTrue(result == 0, "result should be 0");
    }
```



## smod(x,y)

有符号数的取模运算(求余数)

1. **参数**:
   - `x`: 被模数，一个有符号整数值。
   - `y`: 模数，也是一个有符号整数值。
2. **返回值**:
   - 函数返回 `x` 对 `y` 取模的结果。与 `mod` 不同，`smod` 处理的是有符号整数，所以它可以正确处理负数。结果的符号与被模数 `x` 的符号相同。
3. **注意事项**:
   - **如果 y == 0，则为 返回 0**
   - 结果的符号与被模数 `x` 的符号相同。 所以 `smod(-5, -2`)返回`-1`  , `smod(5, -2)`返回 `1`
   - 由于EVM中的整数都是256位的，`smod` 在处理非常大的数或非常小的负数时也需要小心，以防止意外行为。

```solidity
    function Smod(int256 a, int256 b) public pure returns (int256) {
        int256 result;
        assembly {
            let sum := smod(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testSmod() public {
        int256 result = demo.Smod(6, 2);
        assertTrue(result == 0, "result should be 0");

        result = demo.Smod(5, 2);
        assertTrue(result == 1, "result should be 1");

        result = demo.Smod(-5, 2);
        assertTrue(result == -1, "result should be -1");

        result = demo.Smod(-5, -2);
        assertTrue(result == -1, "result should be -1");

        result = demo.Smod(5, -2);
        assertTrue(result == 1, "result should be 1");
    }

    function testSmod0() public {
        // 除数为0, 返回0
        int256 result = demo.Smod(6, 0);
        assertTrue(result == 0, "result should be 0");
    }
```



## exp(x, y)

计算x的y次方

1. **参数**:
   - `x`: 基数，一个整数值。
   - `y`: 指数，也是一个整数值。
2. **返回值**:
   - 函数返回 `x` 的 `y` 次方。这个结果是一个整数，如果结果超过了EVM的单个槽位能存储的最大值（通常是256位），则会自动模256位整数大小。这意味着指数运算也是模运算，可能会出现溢出。
3. **注意事项**:
   - 使用 `exp` 函数时，需要注意整数溢出的问题。由于指数运算可以迅速产生非常大的数，因此在EVM中，如果结果超过了256位，它不会抛出错误，而是简单地回绕到最小值。这种行为在某些情况下可能导致逻辑错误或安全漏洞。

```solidity
    function Exp(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let sum := exp(a, b)
            result := sum
        }
        return result;
    }
```

```solidity
    function testExp() public {
        uint256 result = demo.Exp(2, 3);
        assertTrue(result == 8, "result should be 8");

        result = demo.Exp(2, 0);
        assertTrue(result == 1, "result should be 1");

        result = demo.Exp(2, 1);
        assertTrue(result == 2, "result should be 2");

        //溢出
        result = demo.Exp(
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            2
        );
        console2.logUint(result);
        assertTrue(
            result <
                0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
            "result should be less than 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        );
    }
```



## not(x)

位运行: 非

1. **参数**:
   - `x`: 一个整数值，将对其执行位非操作。
2. **返回值**:
   - 函数返回 `x` 的位非结果。这个操作是对 `x` 中每个位（bit）执行逻辑非操作，即将所有的0变为1，所有的1变为0。
3. **作用**:
   - `not(x)` 主要用于在智能合约中进行位级的逻辑操作。这在处理标志位、权限控制、状态切换等需要对位进行操作的场景中非常有用。
4. **注意事项**:
   - 在使用 `not` 函数时，需要记住它是对整个256位的数值执行位非操作，包括所有的前导零。这意味着操作的结果可能会与只考虑数值有效位的直觉预期不同。



## lt(x, y)

比较大小: x是否小于y

1. **参数**:
   - `x`: 第一个比较数，一个整数值。
   - `y`: 第二个比较数，同样是一个整数值。
2. **返回值**:
   - 如果 `x` 小于 `y`，函数返回1（真）。
   - 如果 `x` 不小于 `y`，函数返回0（假）。

```solidity
    function Lt(uint256 a, uint256 b) public pure returns (bool) {
        bool result;
        assembly {
            let s := lt(a, b)
            result := s
        }
        return result;
    }
```

```solidity
    function testLt() public {
        bool result = demo.Lt(1, 2);
        assertTrue(result == true, "result should be true");

        result = demo.Lt(2, 1);
        assertTrue(result == false, "result should be false");

        result = demo.Lt(1, 1);
        assertTrue(result == false, "result should be false");
    }
```



## slt(x,y)

对于有符号数比较大小: x是否小于y

函数详细说明如下：

1. **参数**:
   - `x`: 第一个比较数，一个有符号整数值。
   - `y`: 第二个比较数，同样是一个有符号整数值。
2. **返回值**:
   - 如果 `x` 在有符号整数的意义下小于 `y`，函数返回1（真）。
   - 如果 `x` 不小于 `y`，函数返回0（假）。

```solidity
    function Slt(int256 a, int256 b) public pure returns (bool) {
        bool result;
        assembly {
            let s := slt(a, b)
            result := s
        }
        return result;
    }
```

```solidity
    function testSlt() public {
        bool result = demo.Slt(1, 2);
        assertTrue(result == true, "result should be true");

        result = demo.Slt(2, 1);
        assertTrue(result == false, "result should be false");

        result = demo.Slt(1, 1);
        assertTrue(result == false, "result should be false");

        result = demo.Slt(-1, 1);
        assertTrue(result == true, "result should be true");

        result = demo.Slt(-1, -2);
        assertTrue(result == false, "result should be false");

        result = demo.Slt(-2, -1);
        assertTrue(result == true, "result should be true");
    }
```



## gt(x,y)   sgt(x,y)

判断大小, x是否大于y

用法与`lt(x,y)`  和 `slt(x,y)`相同



## eq(x, y)

1. - `x`: 第一个比较数，一个整数值。
   - `y`: 第二个比较数，同样是一个整数值。
2. **返回值**:
   - 如果 `x` 等于 `y`，函数返回1。
   - 如果 `x` 不等于 `y`，函数返回0。
3. **注意事项**:
   - 在使用 `eq` 函数时，需要记住它是基于完全的数值等价比较的。这意味着即使两个数在数学上等价，但在二进制表示上不同，它们也被认为是不相等的。



## iszero(x)

1. **参数**:
   - `x`: 一个整数值，将对其进行零值检查。
2. **返回值**:
   - 如果 `x` 为0，函数返回1（真）。
   - 如果 `x` 不为0，函数返回0（假）。

> 为什么要有iszero(x)，直接用eq(x, 0)不就行了吗 (chatgpt)
>
> 在Yul和EVM（Ethereum Virtual Machine）上下文中，确实可以使用 `eq(x, 0)` 来检查 `x` 是否为零。然而，提供 `iszero(x)` 作为一个单独的操作有其特定的优点：
>
> 1. **优化性能**：`iszero(x)` 直接对应于EVM的一个单一操作码（`ISZERO`），而 `eq(x, 0)` 需要两个操作码（`PUSH0` 来推送0到栈上，然后 `EQ`）。在EVM中，每个操作码的执行都有相应的燃料成本（gas cost），因此使用 `iszero` 可以减少执行成本，提高效率。
>
> 2. **代码可读性**：`iszero(x)` 语义明确，直接表示检查 `x` 是否为零。使用 `eq(x, 0)` 虽然在功能上等价，但从代码可读性和意图表达的角度来看，`iszero(x)` 更加直接和清晰。
>
> 3. **历史和兼容性**：EVM的设计和开发早于多种高级智能合约语言的普及，包括Solidity和Yul。在这些早期设计中，特定的操作码（如 `ISZERO`）被引入以满足常见的、简单的操作需求。随着时间的推移，这些操作码和对应的函数在智能合约开发中形成了标准模式。
>
> 综上所述，尽管从功能上看 `iszero(x)` 与 `eq(x, 0)` 相似，但 `iszero(x)` 在性能优化、代码清晰度以及历史兼容性方面提供了额外的好处。



## and(x, y)     or(x, y)       xor(x, y)

x 和 y 的按位 "与"  "或"  "异或"



## byte(n, x)

用于获取整数 `x` 中的特定字节。这个函数直接映射到EVM的 [`BYTE` 操作码](https://www.evm.codes/#1a?fork=shanghai)

1. **参数**:
   - `n`: 字节的位置索引，一个整数值。最右边为31。
   - `x`: 要从中提取字节的整数值。
2. **返回值**:
   - 函数返回 `x` 中位置为 `n` 的单个字节。如果 `n` 大于31（即超出了256位整数的范围），则返回0。

```solidity
    function Byte(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let s := byte(a, b)
            result := s
        }
        return result;
    }
```

```solidity
    function testByte() public {
        uint256 result = demo.Byte(31, 0x1234567890abcdef);
        console2.logBytes1(bytes1(uint8(result)));
        assertTrue(result == 0xef, "result should be 0xef");

        result = demo.Byte(30, 0x1234567890abcdef);
        console2.logBytes1(bytes1(uint8(result)));
        assertTrue(result == 0xcd, "result should be 0xcd");

        result = demo.Byte(1, 0x1234567890abcdef);
        console2.logBytes1(bytes1(uint8(result)));
        assertTrue(result == 0x00, "result should be 0x00");

        result = demo.Byte(100, 0x1234567890abcdef);
        console2.logBytes1(bytes1(uint8(result)));
        assertTrue(result == 0x00, "result should be 0x00");
    }
```



## shl(x, y)  shr(x, y)

分别用于执行逻辑左位移（SHL）和逻辑右位移（SHR）操作

1. **`shl(x, y)`**:
   - 参数
     - `x`: 位移量，一个整数值，表示要将 `y` 左移多少位。
     - `y`: 要进行位移操作的整数值。
   - **返回值**: 返回 `y` 左移 `x` 位的结果。左移操作会将 `y` 的二进制表示向左移动 `x` 位，右边空出的位用0填充。
   - **作用**: 常用于乘以2的幂、生成位掩码或调整二进制数据的位置。
2. **`shr(x, y)`**:
   - 参数
     - `x`: 位移量，一个整数值，表示要将 `y` 右移多少位。
     - `y`: 要进行位移操作的整数值。
   - **返回值**: 返回 `y` 右移 `x` 位的结果。右移操作会将 `y` 的二进制表示向右移动 `x` 位，左边空出的位用0填充（对于无符号整数）。
   - **作用**: 常用于除以2的幂、提取特定位段或调整二进制数据的位置。



```solidity
    function Shr(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result;
        assembly {
            let s := shr(a, b)
            result := s
        }
        return result;
    }
```

```solidity
    function testShr() public {
        uint256 result = demo.Shr(0, 2);
        assertTrue(result == 2, "result should be 2");

        result = demo.Shr(1, 2);
        assertTrue(result == 1, "result should be 1");

        result = demo.Shr(2, 2);
        assertTrue(result == 0, "result should be 0");
    }
```



## sar(x, y)

算数右移

1. **参数**:
   - `x`: 位移量，一个整数值，表示要将 `y` 右移多少位。
   - `y`: 要进行位移操作的整数值。
2. **返回值**:
   - 返回 `y` 算术右移 `x` 位的结果。算术右移与逻辑右移（`shr`）不同，它会保留被移动数值的符号位。这意味着，如果 `y` 是正数，左边空出的位用0填充；如果 `y` 是负数，左边空出的位用1填充。
3. **作用**:
   - `sar(x, y)` 通常用于有符号整数的右位移操作，保持数值的符号不变。这在需要处理有符号整数的算术运算时特别有用，例如在算术运算中实现除以2的幂。
4. **注意事项**:
   - 在使用 `sar` 函数时，需要了解其与 `shr` 的区别。`shr` 是逻辑右位移，不考虑数值的符号，而 `sar` 是算术右位移，会考虑数值的符号。

> `shr` 是逻辑右位移，不考虑数值的符号，而 `sar` 是算术右位移，会考虑数值的符号

```solidity
    function Sar(uint256 a, int256 b) public pure returns (int256) {
        int256 result;
        assembly {
            let s := sar(a, b)
            result := s
        }
        return result;
    }
```

```solidity
    function testSar() public {
        int256 result = demo.Sar(0, 2);
        assertTrue(result == 2, "result should be 2");

        result = demo.Sar(1, 2);
        assertTrue(result == 1, "result should be 1");

        result = demo.Sar(2, 2);
        assertTrue(result == 0, "result should be 0");

        result = demo.Sar(1, -2);
        assertTrue(result == -1, "result should be -1");

        result = demo.Sar(2, -2);
        assertTrue(result == -1, "result should be -1");

        result = demo.Sar(5, -2);
        assertTrue(result == -1, "result should be -1");
    }
```



## addmod(x, y, m)

相当于 `mod(add(x,y),m)`



## mulmod(x, y, m)

相当于 `mod(mul(x,y),m)`



## signextend(i, x)

[符号扩展操作](https://zh.wikipedia.org/wiki/符号扩充)

1. **参数**:
   - `i`: 一个整数值，指定从哪个字节开始进行符号扩展。这个字节索引是从右向左的，即最低有效字节为0，最高有效字节为31。
   - `x`: 要进行符号扩展的整数值。
2. **返回值**:
   - 返回对 `x` 执行符号扩展后的结果。符号扩展是指将 `x` 的第 `i` 个字节（从右边数起）的符号位（最高位）扩展到左边的所有高位。如果该字节的符号位是1（表示负数），则高位都填充1；如果符号位是0（表示正数），则高位都填充0。
3. **作用**:
   - `signextend(i, x)` 通常用于在处理有符号整数时调整其长度，保持数值的符号不变。这在某些数学运算或数据处理场景中非常有用，特别是在需要将一个较短的有符号数值扩展到较长的有符号数值时。
4. **注意事项**:
   - 使用 `signextend` 时需要确保字节索引 `i` 的正确性。如果 `i` 大于31或小于0，则 `x` 的值不会改变。



## keccak256(p, n)

于计算存储在内存中某个特定区域的数据的Keccak-256哈希值。这个函数直接映射到EVM的 `KECCAK256` 操作码

1. **参数**:
   - `p`: 内存中数据的起始位置，一个整数值，指向要哈希的数据的第一个字节。
   - `n`: 要哈希的数据的长度（以字节为单位），一个整数值。
2. **返回值**:
   - 返回从内存位置 `p` 开始、长度为 `n` 字节的数据的Keccak-256哈希值。结果是一个32字节（256位）的哈希值。

> 在使用 `keccak256` 时，需要确保正确地指定内存位置和数据长度。不正确的参数可能导致错误的哈希值或运行时错误。



> yul中的`keccak256(p, n)` 和 solidity中 `keccak256(bytes memory)`的区别:
>
> - 在Solidity中，动态数组（如 `bytes`）在内存中的布局是以其长度开头，后跟数据本身。这意味着当你使用Solidity的 `keccak256(a)` 时，它计算的是从数组的长度信息开始的整个数组的哈希值。
> - 在内联汇编中，`keccak256(a, length)` 函数直接接受一个内存地址和长度作为参数。如果 `a` 是一个动态数组，你需要确保传递正确的内存地址和长度，以便它仅包括数据部分，而不包括长度前缀。

```solidity
    function Keccak256(
        bytes memory a,
        uint256 length
    ) public pure returns (bytes32) {
        bytes32 result;
        assembly {
            // 获取指向数组数据的指针，跳过长度前缀
            let dataPtr := add(a, 32)
            let s := keccak256(dataPtr, length)
            result := s
        }
        return result;
    }

    function Keccak256_2(bytes memory a) public pure returns (bytes32) {
        bytes32 result;
        assembly {
            let dataPtr := add(a, 32)
            let s := keccak256(dataPtr, mload(a))
            result := s
        }
        return result;
    }
```

```solidity
    function testKeccak256() public {
        bytes32 result = demo.Keccak256("hello world", 11);
        bytes32 result2 = keccak256("hello world");
        bytes32 result3 = demo.Keccak256_2("hello world");

        assertTrue(result == result2, "result should be equal");
        assertTrue(result == result3, "result should be equal");
    }
```



## pc()

- `pc()` 函数返回当前EVM指令的程序计数器值，即当前正在执行的指令的地址。这个函数主要用于调试目的，可以帮助开发者了解合约代码的执行流程和位置。在实际的智能合约开发中，它的用途相对有限，因为普通的合约逻辑通常不需要依赖于指令的具体位置。由于EVM是一个基于堆栈的虚拟机，其中的程序计数器会随着每条指令的执行而递增，因此 `pc()` 返回的值在合约执行过程中会不断变化。



## pop()

1. **参数**:
   - `x`: 要从栈中弹出的元素。在Yul中，这通常是一个变量或表达式的结果。
2. 返回值: 无
3. **作用**:
   - `pop(x)` 主要用于移除并丢弃不再需要的栈顶元素。在EVM中，由于资源（如燃气）的限制，有效地管理栈空间是很重要的。`pop` 函数允许开发者显式地移除不再需要的值，这有助于优化燃气使用和避免栈溢出。
4. **使用场景**:
   - 这个函数通常用在不需要存储函数调用的返回值时，或者在对某些操作的结果不感兴趣时。例如，某些EVM操作（如 `CALL`、`MUL` 等）会推送结果到栈上，如果这些结果不需要，可以使用 `pop` 来移除它们。
5. **注意事项**:
   - 使用 `pop` 函数时，需要确保你确实想要丢弃该元素。一旦使用了 `pop`，该元素将从栈中移除，无法恢复。



## mload(x)

用于从EVM的内存中读取数据。这个函数直接映射到EVM的 `MLOAD` 操作码

1. **参数**:
   - `p`: 一个整数值，表示内存中的起始地址。这个地址指向内存中你想要读取的数据的开始位置。
2. **返回值**:
   - `mload(p)` 返回从内存地址 `p` 开始的32字节（256位）数据。在EVM中，内存操作通常以32字节为单位进行。

> 在使用`mload(x)`前你应该先搞清楚`x`的内存布局
>
> 比如 ` bytes memory str = "hello world";`这种动态数组(或字符串)的内存布局是:  [length, data...]   
> 字符串的长度（以字节为单位）存储在前32个字节。这是因为EVM的字长为256位，即32字节。
> 紧接着长度信息之后的是字符串的实际数据。每个字符按照其ASCII码值存储。例如，`"hello world"` 将会按照其每个字符的ASCII码值来存储。如果字符串的长度不是32字节的整数倍，那么最后一个32字节段将使用0来填充剩余空间。
>
> ```
> 0x000000000000000000000000000000000000000000000000000000000000000b
> 0x68656c6c6f20776f726c64000000000000000000000000000000000000000000
> ```
>
> 



>`mload(0x40)` 存储着下一个可用内存地址的指针



```solidity
    function Mload(
        bytes memory a,
        uint256 offset
    ) public pure returns (bytes32) {
        bytes32 result;
        assembly {
            let dataPtr := add(a, offset)
            let s := mload(dataPtr)
            result := s
        }
        return result;
    }

    function Mload_GetLength(bytes memory a) public pure returns (uint256) {
        uint256 result;
        assembly {
            let s := mload(a)
            result := s
        }
        return result;
    }
```

```solidity
    function testMload() public {
        bytes memory str = "hello world";
        // 对于动态数组（或字符串），其内存布局为：[length, data...] ，其中 length 为数组长度（32个字节，256位），data 为数组数据。
        // mload()读取前32个字节，即读取length
        uint256 result = demo.Mload_GetLength(str);
        assertTrue(result == 11, "result should be 11");

        // offset为32，即从data开始读取,读取长度为32个字节
        bytes32 result2 = demo.Mload(str, 32);
        // 使用 abi.encodePacked 来动态生成期望的 bytes32 值
        bytes32 expected = bytes32(abi.encodePacked(str));
        assertTrue(result2 == expected, "Incorrect data read from memory");
    }
```



## mstore(p, v)

与`mload(p)`向对应,  将`v`值写入`p`指向的内存位置

1. **参数**:
   - `p`: 一个整数值，表示内存中的起始地址，用于指定要写入数据的位置。
   - `v`: 要写入的数据。在EVM中，每次写入操作写入32字节的数据。
2. 返回值: 无
3. **作用**:
   - `mstore(p, v)` 用于将32字节的数据 `v` 写入到内存地址 `p` 开始的位置。这在需要临时存储或修改内存中的数据时非常有用。
4. **注意事项**:
   - 在使用 `mstore` 时，需要确保提供的地址 `p` 是有效的，并且内存空间足够存储32字节的数据。
   - 由于 `mstore` 操作是32字节对齐的，因此它总是写入32字节的数据块。如果你只需要写入较小的数据，如一个整数或地址，你需要正确地处理数据，以确保写入的内容符合你的预期。



> 如果你尝试使用mstore来修改字符串时, 如果你试图修改的字符串被作为参数传递的话,则可能不会按预期工作. 因为字符串是不可变的,作为参数传递时,被传递的是副本
>
> 比如:
>
> ```solidity
>     function Mstore(bytes memory a, uint256 offset, bytes32 value) public pure {
>         assembly {
>             let dataPtr := add(a, offset)
>             mstore(dataPtr, value)
>         }
>     }
>         
> ```
>
> ```solidity
>     function testMstore() public {
>         bytes memory str = "hello world";
>         demo.Mstore(str, 32, bytes32(abi.encode("hello WORLD")));
>         console2.logString(string(str));
> 
>         // 不应该相等，调用demo.Mstore时传入的是字符串的副本
>         assertTrue(
>             keccak256(str) != keccak256("hello WORLD"),
>             "result should not be equal"
>         );
>     }
> ```
>
> 而下面这个则可以:
>
> ```solidity
>     function testMstore_local() public {
>         bytes memory str = "hello world";
>         assembly {
>             mstore(add(str, 32), "hello WORLD")
>         }
>         console2.logString(string(str));
>         // 应该相等，直接修改了字符串的内存
>         assertTrue(
>             keccak256(str) == keccak256("hello WORLD"),
>             "result should not be equal"
>         );
>     }
> ```
>
> 



## mstore8(p, v)

与 `mstore(p,v)`类似, 只不过只写入8位(1个字节), 而不是32个字节

**参数**:

- `p`: 一个整数值，表示内存中的起始地址，用于指定要写入单字节数据的位置。
- `v`: 要写入的单字节数据。即使提供了一个大于一个字节的值，只有最低有效的8位（一个字节）会被写入, 相当于写入是 ` v & 0xff`

返回值: 无



```solidity
    function testMstore8() public {
        bytes memory str = "hello world";
        assembly {
            mstore8(add(str, 32), 0x48) //0x48 'H'
        }
        console2.logString(string(str));
        assertTrue(
            keccak256(str) == keccak256("Hello world"),
            "result should  be equal"
        );
    }
```



## sload(x)   sstore(p, v)

与 `mload(x)`类似, 前者读取内存x处的32个字节, 而`sload(x)`读取storage 中slot x处的32个字节, 由于一个slot只能存储32个字节的数据,所以其就是读取slot x出完整的值

1. - `p`: 一个整数值，表示存储的槽位（slot）。每个槽位可以存储32字节（256位）的数据。
2. **返回值**:
   - `sload(p)` 返回存储在槽位 `p` 中的数据。这个数据是一个32字节的值。

​	**注意事项**:

- 存储读取（`sload`）是一个相对昂贵的操作，因为它需要访问区块链的状态。在编写智能合约时，频繁地使用 `sload` 可能会增加交易的燃料（gas）成本。

`sstore(p, v)` 则是在slot p 处存入32字节的值v

```solidity

    uint256 private value_0; // slot 0
    mapping(address => uint) map_1; // slot 1

    function SetV0(uint256 value) public {
        value_0 = value;
    }

    function GetV0() public view returns (uint256) {
        return value_0;
    }

    function Sload(uint256 slot) public view returns (uint256) {
        uint256 result;
        assembly {
            let s := sload(slot)
            result := s
        }
        return result;
    }

    function Sstore(uint256 slot, uint256 value) public {
        assembly {
            sstore(slot, value)
        }
    }

    function SetMap1Value(address key, uint256 value) public {
        map_1[key] = value;
    }

    function GetMap1Value(address key) public view returns (uint256) {
        return map_1[key];
    }



    function GetMap1Slot() public pure returns (uint256) {
        uint256 result;
        assembly {
            result := map_1.slot
        }
        return result;
    }
```



```solidity
    function testSload() public {
        // normal value
        demo.SetV0(100);
        uint256 result = demo.GetV0();
        assertTrue(result == 100, "result should be 100");
        uint256 result2 = demo.Sload(0);
        assertTrue(result2 == 100, "result should be 100");

        //mapping
        demo.SetMap1Value(address(this), 300);
        result = demo.GetMap1Value(address(this));
        assertTrue(result == 300, "result should be 300");

        uint256 slotOfThisValueInMapping = uint256(
            keccak256(abi.encodePacked(address(this), uint256(1)))
        );

        result2 = demo.Sload(slotOfThisValueInMapping);
        console2.logUint(result2);
        // why?
        // assertTrue(result2 == 300, "result should be 300");
    }

    function testSstore() public {
        demo.SetV0(100);
        uint256 result = demo.GetV0();
        assertTrue(result == 100, "result should be 100");
        demo.Sstore(0, 200);
        uint256 result2 = demo.GetV0();
        assertTrue(result2 == 200, "result should be 200");
    }
```



## msize()

获取当前已分配的内存大小的. 由于EVM分配内存是连续的, 所以其返回值也是下一个可用内存字的起始位置. 它总是32的整数倍.

1. **返回值**:

   返回一个整数值，表示当前已分配内存的大小。这个值是到目前为止合约执行过程中所分配的内存量的最大值。

```solidity
    function Msize() public pure returns (bytes32) {
        bytes32 str = "hello world";
        bytes32 data;

        // 如果需要编译通过，需要在编译器设置优化选项为false
        // 比如在foundry.toml中设置：optimize = false
        // 编译器优化打开时,不允许使用msize()
        assembly {
            let ptr := msize()
            mstore(ptr, str)
            data := mload(ptr)
        }

        return data;
    }
```



> 如果要知道下一个可以内存地址, 不推荐使用`msize()`, 推荐使用`mload(0x40)`
>
> 1. - 这是一种常用的约定，用于访问Solidity运行时环境中的“空闲内存指针”（free memory pointer）。这个指针存储在内存地址 `0x40` 的位置，并指向当前可用于分配的第一个空闲内存地址。
>    - 当您在Solidity的内联汇编中使用 `mload(0x40)` 时，您实际上是在读取这个空闲内存指针的当前值。
>    - 这个指针是由Solidity运行时维护的，用于跟踪合约内存中的动态分配情况。
> 2. **`msize()`**:
>    - `msize()` 是EVM的一个操作码，它返回当前已分配的内存大小（以字节为单位）。这个大小是下一个可用内存字的起始位置。
>    - 在Solidity的较新版本中（0.6.0及以上），`msize()` 不再推荐使用，因为启用Yul优化器后，`msize()` 的行为可能会发生变化，从而影响其返回值的预测性

## gas()

等效于solidity中的`gasleft()`

```solidity
pragma solidity ^0.8.0;

contract GasExample {
    function performOperation() public {
        uint256 remainingGas = gasleft();

        if (remainingGas > 100000) {
            // 执行燃料消耗较多的操作
        } else {
            // 执行燃料消耗较少的备选操作
        }
    }
}

```



## address()

获取当前正在执行代码的合约地址。

等效于 solidity中的`address(this)`



## balance(a)

获取以太坊地址 `a` 的以太币余额

等效于solidity的`address(a).balance`



## selfbalance()

获取当前正在执行代码的合约地址的以太币余额

等效于  `balance(address())`  或 solidity的 `address(this).balance`



## caller()

获取当前调用（或消息）的发送者的地址, 相当于`msg.sender`

> 注意: 在`delegatecall`中使用的是调用者的上下文

```solidity
    function Caller() public view returns (address) {
        address result;
        assembly {
            result := caller()
        }
        return result;
    }
```

```solidity
    function testCaller() public {
        address result = demo.Caller();
        console2.logAddress(result);
        assertTrue(result == address(this), "result should be equal");

        (, bytes memory data) = address(demo).delegatecall(
            abi.encodeWithSignature("Caller()")
        );
        address result2 = abi.decode(data, (address));
        assertTrue(result2 != address(this), "result should not be equal");
        assertTrue(result2 == msg.sender, "result should be equal");
    }
```

## callvalue()

等效于 solidity中的 `msg.value`

## calldatasize()

用于获取当前函数调用的输入数据的大小, 等效于 solidity中 `msg.data.length`

## calldataload(p)

获取calldata中从第 `p` 个字节开始的32个字节的数据.如果调用数据的长度小于 `p + 32` 字节，那么返回的数据将从位置 `p` 开始，直到调用数据的末尾，并且剩余的部分将用零填充。

`p` : 指定了要从调用数据（calldata）中读取数据的起始位置。

返回值: 32个字节的数据

> Calldata的内存结构：
>
> 1. **函数选择器**:
>    - 前4个字节包含函数的选择器（或签名哈希）。这是通过对函数签名进行Keccak-256哈希运算并取其前4个字节得到的。函数选择器用于合约内部确定哪个函数被调用。
> 2. **函数参数**:
>    - 函数参数紧随函数选择器之后。每个参数根据其类型进行ABI编码。
>    - 简单的值类型（如 `uint256`、`address`）直接按顺序编码，每个参数占据32字节。如果参数小于32字节（如 `uint8`），则在左侧填充零字节。
>    - 动态类型（如 `bytes`、`string`）则稍复杂，它们在主体部分被编码为指向其数据开始位置的偏移量（32字节），其实际数据则存储在参数区域的末尾。
> 3. **动态数据**:
>    - 动态数据类型（如 `string`、`bytes`、动态数组）的实际内容被放置在所有固定大小参数之后。首先是数据的长度（32字节），然后是数据本身。如果数据本身的长度不是32字节的整数倍，将在其后填充零字节，直到长度为32的倍数。

```solidity
    function Calldataload(uint256 p) public pure returns (bytes32) {
        bytes32 result;
        assembly {
            result := calldataload(p)
        }
        return result;
    }
```

```solidity
    function testCalldataload() public {
        bytes32 result = demo.Calldataload(4);
        // 为什么等于4
        // result := calldataload(4) 刚好跳过函数选择器的4个字节，读取第一个参数的前32个字节
        assertTrue(uint256(result) == 4, "should equal to the first argument");
    }
```







## calldatacopy(t, f, s)

用于将一部分调用数据（calldata）复制到内存中。这个函数直接映射到EVM的 `CALLDATACOPY` 操作码

参数:

- `t`（target）: 表示内存中的目标起始位置。（以字节为单位）
- `f`（from）: 表示调用数据中的起始位置。（以字节为单位）
- `s`（size）: 表示要复制的数据的大小（以字节为单位）

返回值: 无

```solidity
    function testCalldatacopy() public {
        // 我们会将本函数的函数选择器存到result中
        bytes memory result = new bytes(4);
        assembly {
            // add(result, 32) 跳过result内存布局中的前32个字节，即跳过length，直接指向数据区
            // calldata的前4个字节是函数选择器
            calldatacopy(add(result, 32), 0, 4)
        }

        // 错误的方式：
        // bytes4 result;
        // assembly {
        //     calldatacopy(result, 0, 4)
        // }

        // 正确的方式
        // bytes4 result;
        // assembly {
        //     let ptr := mload(0x40)
        //     calldatacopy(ptr, 0, 4)
        //     result := mload(ptr)
        // }

        assertTrue(
            bytes4(result) == this.testCalldatacopy.selector,
            "should equal to this function's selector"
        );
```





## codesize()

返回**当前**合约/执行环境的代码大小(字节)

由于是返回自己的代码大小,而不是去获取别人的,所以我的理解是此值永不会为0, 并且在creation time调用和run time调用该函数返回的结果是不一样的,前者包含了creation code

```solidity
contract demoContractForCodeSize {

    uint256 public codeSizeCallInConstructor ;
    constructor() {
        codeSizeCallInConstructor = GetCodeSize();
    }

    function GetCodeSize() public pure returns (uint256) {
        uint256 result;
        assembly {
            result := codesize()
        }
        return result;
    }
}

contract YulDemoContract {
    function CodeSize() public  returns (uint256, uint256) {
        uint256 s1;
        uint256 s2;

        demoContractForCodeSize d = new demoContractForCodeSize();
        s1 = d.codeSizeCallInConstructor();
        s2 = d.GetCodeSize();

        return (s1, s2);
    }
 }
```

```solidity
    function testCodeSize() public{
        (uint256 result1, uint256 result2) = demo.CodeSize();
        console2.logUint(result1);
        console2.logUint(result2);
    }
```

```
[PASS] testCodeSize() (gas: 111391)
Logs:
  297
  228
```



## extcodesize(a)

返回地址`a`的代码大小(字节)

如果地址`a`是外部账户, 返回 `0`

如果地址`a`是合约,  但合约的代码还没有被部署完成, 则返回`0`

如果地址`a`是合约,  并且合约的代码被部署完成, 则返回实际运行时代码大小

```solidity
contract demoContractForExtcodesize {
uint256 public extCodeSizeCallInConstructor ;
    constructor() {
        extCodeSizeCallInConstructor = GetExtCodeSize();
    }
    function GetExtCodeSize() public view returns (uint256) {
        uint256 result;
        address addr = address(this);
        assembly {
            result := extcodesize(addr)
        }
        return result;
    }
}


contract YulDemoContract {
    function ExtCodeSize() public  returns (uint256, uint256) {
       uint256 s1;
         uint256 s2;
         demoContractForExtcodesize d = new demoContractForExtcodesize();
         s1 = d.extCodeSizeCallInConstructor();
         s2 = d.GetExtCodeSize();
        return (s1, s2);
    }
 }
```

```solidity
    function testExtCodeSize() public{
        (uint256 result1, uint256 result2) = demo.ExtCodeSize();
        console2.logUint(result1);
        console2.logUint(result2);
    }
```

输出

```
[PASS] testExtCodeSize() (gas: 93138)
Logs:
  0
  235
```

> 所以使用codesize判断一个地址是否是合约还是EOA时不靠谱的, 使用
>
> ```solidity
> require(msg.sender == tx.origin, "Minting from smart contracts is disallowed");
> ```



## codecopy(t, f, s)

用于复制智能合约自己的代码到内存

1. **t (Target)**: 这是目标内存地址，表示代码将被复制到哪里。在EVM中，内存是线性的，并且以字节为单位寻址。这个参数指定了内存中的起始位置，代码将从这里开始复制。
2. **f (From)**: 这是代码的起始位置。它指的是当前执行的合约代码中的一个位置，从这个位置开始读取代码。
3. **s (Size)**: 这是要复制的代码的字节大小。这个参数指定了从源代码中复制多少字节到目标内存位置。



## extcodecopy(a, t, f, s)

类似于 `codecopy(t, f, s)`, 只不过代码来自于地址`a`



>不要试图通过克隆合约的代码并利用create函数来创建合约的副本, 上面两个函数所指的代码都是合约的运行时代码,而create函数需要的是创建时代码
>
>而应该使用 ERC-1167: https://eips.ethereum.org/EIPS/eip-1167



## extcodehash(a)

地址a的代码哈希值

## returndatasize()

用于获取外部函数调用（例如，通过 `call`、`delegatecall`、`staticcall` 等）返回的数据的字节大小



## returndatacopy(t, f, s)

用于将外部函数调用（例如，通过 `call`、`delegatecall`、`staticcall` 等）返回的数据拷贝到内存

1. **t (Target)**: 目标内存的起始位置，即将数据复制到内存的哪个位置。
2. **f (From)**: 返回数据缓冲区中的起始位置，通常为0，表示从缓冲区的开始复制。
3. **s (Size)**: 要复制的字节数。

```solidity
contract SimpleContract {
    uint256 private value;

    function getValue() public view returns (uint256) {
        return value;
    }

    function setValue(uint256 v) public {
        value = v;
    }
}

contract YulDemoContract {
    function CallData(
        address addr,
        bytes memory data
    ) public returns (bytes memory) {
        bytes memory result;
        // 演示目的，不使用call的返回值，而通过下面获取返回值
        (bool ok, ) = addr.call(data);
        require(ok, "call failed");

        assembly {
            // 外部调用返回的数据大小,也就是上面的call返回值的长度
            let size := returndatasize()
            // 读取空闲指针位置
            result := mload(0x40)
            // 更新空闲指针位置。以便为返回数据分配足够的空间
            // add(size, 0x20): 首先，将返回数据的大小（size）与0x20（即32字节，这是EVM中单个存储槽的大小）相加。这是因为动态字节数组在内存中的布局是首先存储数组的长度（占用32字节），紧接着是数组的数据。
            // add(add(size, 0x20), 0x1f): 然后，将上一步的结果与0x1f（即31）相加。这实际上是为了计算接下来最近的32字节边界。由于Solidity的内存是以32字节为单位对齐的，这一步确保分配的内存符合这一要求。
            // and(add(add(size, 0x20), 0x1f), not(0x1f)): 接下来，使用and操作符和not(0x1f)（即取0x1f的位反）进行位操作。这实际上是将上一步的结果向下舍入到最接近的32的倍数。这是通过掩盖掉数值的最后五位（二进制中的31）来实现的，从而确保结果是32的倍数。
            // add(result, ...): 最后，将这个对齐后的大小值加到当前的空闲内存指针result上。这个操作更新了空闲内存指针，指向足够容纳返回数据（包括其长度）的内存区域的末尾。
            mstore(
                0x40,
                add(result, and(add(add(size, 0x20), 0x1f), not(0x1f)))
            )
            // 将返回数据的大小存储到返回数据的开头32个字节中
            mstore(result, size)
            // 将返回数据复制到返回数据的开头32个字节之后的位置
            returndatacopy(add(result, 0x20), 0, size)
        }

        return result;
 }
```

```solidity
    function testCallData() public{

         bytes memory data = abi.encodeWithSignature("setValue(uint256)", 100);
         demo.CallData(address(simple), data);

        data = abi.encodeWithSignature("getValue()");
        bytes memory result = demo.CallData(address(simple), data);
        uint256 v = abi.decode(result, (uint256));
        assertTrue(v==100, "result should be 100");
    }
```



## create(v, p, n)  create2(v, p, n, s)

参考 new.md



## call(g, a, v, in, insize, out, outsize)

函数调用

1. **g (Gas)**: 这是为这次调用分配的 gas 数量。在EVM中，每个操作都需要一定量的 gas 来执行，包括合约调用。提供足够的 gas 是确保调用成功的关键。
2. **a (Address)**: 被调用的合约地址。
3. **v (Value)**: 要发送的以太币数量，以wei为单位。如果你不想发送以太币，这个值应该是0。
4. **in (Input Data Location)**: 输入数据在内存中的起始位置。这些数据通常是被调用合约函数的编码参数。
5. **insize (Input Data Size)**: 输入数据的大小，以字节为单位。
6. **out (Output Data Location)**: 输出数据在内存中的存放位置。这是调用完成后返回数据将被存放的地方。
7. **outsize (Output Data Size)**: 预期的返回数据的大小，以字节为单位。

> 被调用函数签名和函数参数是如何传递的?
>
> 在`in`和`insize`指定的内存区域, 按照abi编码规范进行的布局, 具体而言就是前4个字节是被调用函数的selector, 然后是参数依次被编码, 这和solidity中普通的calldata 是一样的

```solidity
contract SimpleContract {
    uint256 private value;

    function getValue() public view returns (uint256) {
        return value;
    }

    function setValue(uint256 v) public {
        value = v;
    }
}
```

```solidity
    function testCall() public {
        address addr = address(simple);
        bytes4 selector = bytes4(keccak256("setValue(uint256)"));
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, selector) // 先放置函数选择器
            mstore(add(ptr, 0x4), 888) // 紧接着是参数
            let success := call(
                gas(), // gas
                addr, // to
                0, // value
                ptr, // input
                0x24, // input size
                ptr, // output
                0 // output size
            )
        }

        uint256 result; // = simple.getValue();
        selector = bytes4(keccak256("getValue()"));
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, selector) // 先放置函数选择器, 没有参数
            let success := call(
                gas(), // gas
                addr, // to
                0, // value
                ptr, // input
                0x4, // input size
                ptr, // output
                0x20 // output size
            )
            result := mload(ptr)
        }

        assertTrue(result == 888, "result should be 888");
    }
```



## callcode(g, a, v, in, insize, out, outsize)

和`call`类似，只不过，上下文使用的是调用者的上下文

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;

contract SimpleContract {
    uint256 private value; // slot 0

    function getValue() public view returns (uint256) {
        return value;
    }

    function setValue(uint256 v) public {
        value = v;
    }
}

contract YulDemoContract {
    uint256 private value_0; // slot 0

    function SetV0(uint256 value) public {
        value_0 = value;
    }

    function GetV0() public view returns (uint256) {
        return value_0;
    }
    
    function CallCode(address addrOfSimpleContract, uint256 value) public{
        bytes4 selector = bytes4(keccak256("setValue(uint256)"));
        bool success;
        assembly{
            let ptr := mload(0x40)
            mstore(ptr, selector)
            mstore(add(ptr, 0x4), value)
            //使用的是调用者的上下文，所以本合约的value_0会被设值，
            //而simpleContract中的不会
            success := callcode(
                gas(),
                addrOfSimpleContract,
                0,
                ptr,
                0x24,
                ptr,
                0
            )
        }

        require(success, "call code failed");
    }
}
```

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;

import "forge-std/Test.sol";
import "../src/yuldemo.sol";

contract YulDemoTest is DSTest {
    YulDemoContract demo;
    SimpleContract simple;
    
    function testCallCode() public {
        demo.CallCode(address(simple), 100);
        // console2.logUint(demo.GetV0());
        assertTrue(demo.GetV0() == 100, "result should be 100");
    }
}
```



## delegatecall(g, a, in, insize, out, outsize)

和`callcode`类似，但保留了`caller`和`callvalue`

## staticcall(g, a, in, insize, out, outsize)

等同于 `call(g, a, 0, in, insize, out, outsize)` 但其不允许改变虚拟机状态，相当于是调用`pure`或`view`函数



