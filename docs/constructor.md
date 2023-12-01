---
key: constructor, is, super
desc: 合约构造器 与 继承
---

## 构造器

```solidity
contract X {
    string public name;

    constructor(string memory _name) {
        name = _name;
    }
}
contract Y {
    string public text;

    constructor(string memory _text) {
        text = _text;
    }
}
```

### 如何调用父合约的构造器:

方式1:

```solidity
// Pass the parameters here in the inheritance list.
contract B is X("Input to X"), Y("Input to Y") {

}
```

方式2:

```solidity
contract C is X, Y {
    // Pass the parameters here in the constructor,
    // similar to function modifiers.
    constructor(string memory _name, string memory _text) X(_name) Y(_text) {}
}
```

### 构造器调用顺序

>无论子合约的构造函数中列出的父合约的顺序如何，父构造函数总是按照继承的顺序被调用。 (按照 is 时的书写顺序)

```solidity
// Order of constructors called:
// 1. X
// 2. Y
// 3. D
contract D is X, Y {
    constructor() X("X was called") Y("Y was called") {}
}

// Order of constructors called:
// 1. X
// 2. Y
// 3. E
contract E is X, Y {
    constructor() Y("Y was called") X("X was called") {}
}
```



## 继承

+ Solidity 支持多重继承。合约可以通过使用 `is `关键字来继承其他契约。

+ 将被一个子合约覆盖的函数必须被声明为`virtual`。

+ 要覆盖一个父合约的函数必须使用关键字`override`。

+ 继承的顺序很重要。

+ 继承必须从“最基础”到“最派生”的顺序进行。所谓“最基础”的合约是指最基本的合约，没有任何继承关系，而“最派生”的合约是指继承了一些其他合约的合约。 (例如，如果合约 A 是最基础的合约，那么合约 B 就是从 A 中继承的，所以 B 是比 A 更派生的。如果合约 C 又从 B 中继承，那么 C 就是比 A 和 B 更派生的。)



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/* Graph of inheritance
    A
   / \
  B   C
 / \ /
F  D,E

*/

contract A {
    //要声明为virtual以便被子合约override
    function foo() public pure virtual returns (string memory) {
        return "A";
    }
}

// 使用 'is' 关键字进行继承
contract B is A {
    // 使用 override 覆盖 父合约中的函数, 并使用 virtual以便被它的子合约override
    function foo() public pure virtual override returns (string memory) {
        return "B";
    }
}

contract C is A {
    // Override A.foo()
    function foo() public pure virtual override returns (string memory) {
        return "C";
    }
}

//合约可以从多个父合约中继承。
//当一个函数被调用时，它在不同的合约中被多次定义，父合约会从右到左，以深度优先的方式进行搜索。
//意思是, 如果你调用D的foo函数, 按照D,B,C的顺序搜索foo函数, 如果D中没有则在B中搜索,以此类推
contract D is B, C {
    // D.foo() returns "C"
    // super关键字调用的是最近(最右边)的父合约的函数
    function foo() public pure override(B, C) returns (string memory) {
        return super.foo();
    }
}

contract E is C, B {
    // E.foo() returns "B"
    // since B is the right most parent contract with function foo()
    function foo() public pure override(C, B) returns (string memory) {
        return super.foo();
    }
}

//继承必须从“最基础”到“最派生”的顺序进行。
//如果 A 和 B 的顺序被交换，将会抛出编译错误。(A比B更基础, B比A更派生)
contract F is A, B {
    function foo() public pure override(A, B) returns (string memory) {
        return super.foo();
    }
}

```

