---
key: super
desc: 调用父合约中的方法或状态变量
---

```solidity
super
```



调用父合约中的方法或状态变量



参考这里 https://solidity-by-example.org/super/



> solidity是可以多重继承的



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/* Inheritance tree
   A
 /  \
B   C
 \ /
  D
*/

contract A {
    // This is called an event. You can emit events from your function
    // and they are logged into the transaction log.
    // In our case, this will be useful for tracing function calls.
    event Log(string message);

    function foo() public virtual {
        emit Log("A.foo called");
    }

    function bar() public virtual {
        emit Log("A.bar called");
    }
}

contract B is A {
    function foo() public virtual override {
        emit Log("B.foo called");
        A.foo();
    }

    function bar() public virtual override {
        emit Log("B.bar called");
        super.bar();
    }
}

contract C is A {
    function foo() public virtual override {
        emit Log("C.foo called");
        A.foo();
    }

    function bar() public virtual override {
        emit Log("C.bar called");
        super.bar();
    }
}

contract D is B, C {
    // Try:
    // - Call D.foo and check the transaction logs.
    //   Although D inherits A, B and C, it only called C and then A.
    // - Call D.bar and check the transaction logs
    //   D called C, then B, and finally A.
    //   Although super was called twice (by B and C) it only called A once.

    //合约 D 继承自 B 和 C，并覆盖了 "foo()" 函数。
    //当我们调用 D 中的 "foo()" 函数时，会先输出 "D.foo called"，然后调用 "super.foo()"。
    //"super.foo()" 会按照 B、C 的顺序搜索 "foo()" 函数，找到第一个定义的 "foo()" 函数，并执行。
    //由于在这个例子中，B、C 均覆盖了 A 中的 "foo()" 函数，(super关键字调用的是最近(最右边)的父合约的函数)
    //因此 "super.foo()" 将调用 C 中的 "foo()" 函数，而不是 B 中的 "foo()" 函数。
    //C 中的 "foo()" 函数内部又调用了 A 中的 "foo()" 函数，因此最后会输出 "A.foo called"。
    //所以将输出 D, C, A
    // !!!!!!
    //重点： D中foo函数的super链条是 super( is C) - super(is B) - super( is A)
    //从下到上，每一次 调用super时， 都在该链条中进行搜索， 如果执行过了，则执行下一个
    // D中的foo()调用super时，首先搜索到的是super( is C), 也就是C中的foo函数，
    // 此后，C中的foo函数中没有使用super,而是平台的函数调用
    function foo() public override(B, C) {
        emit Log("D.foo called");
        super.foo();
    }

    //当我们调用 D 中的 "bar()" 函数时，会先输出 "D.bar called"。然后调用 "super.bar()"。
    //由于在这个例子中，B、C 均覆盖了 A 中的 "foo()" 函数，(super关键字调用的是最近(最右边)的父合约的函数)
    //因此 "super.bar()" 将调用 C 中的 "bar()" 函数,而不是 B 中的 "bar()" 函数。
    //C 中的 "bar()" 函数内部又调用了 "super.bar()"，所以会再次按照 C、B 的顺序搜索 "bar()" 函数。
    //由于之前已经找到并调用了 C 中的 "bar()" 函数，所以此时会调用 B 中的 "bar()" 函数。
    //所以将输出 D, C, B, A
    // !!!!!!
    //重点： D中bar函数的super链条是 super( is C) - super(is B) - super( is A)
    //从下到上，每一次 调用super时， 都在该链条中进行搜索， 如果执行过了，则执行下一个
    // D中的bar()调用super时，首先搜索到的是super( is C), 也就是C中的bar函数，
    // 此后，C中的bar函数调用super时，按照 super( is C) - super(is B) - super( is A)的顺序， 这次该轮到B了
    // 此后，B中的bar函数调用super时，按照 super( is C) - super(is B) - super( is A)的顺序， 这次该轮到A了
    function bar() public override(B, C) {
        emit Log("D.bar called");
        super.bar();
    }
}

```



>solidity中的`super`类似于C#中的`base`
>
>需要注意的是，在 Solidity 中使用 "super" 关键字调用继承合约中的函数时，必须指定从哪个合约继承的函数。这是因为，Solidity 中的合约可以从多个父合约中继承，如果不指定，编译器不知道应该调用哪个合约中的函数。
>
>例如，在你的代码中，D 合约继承自 B 和 C 两个合约。如果你在 D 合约中使用 "super.foo()" 来调用 "foo()" 函数，编译器会报错，因为它不知道应该调用 B 还是 C 中的 "foo()" 函数。为了解决这个问题，你必须在 "super" 关键字后指定从哪个合约继承的函数，如 "super(B, C).foo()"。
