---
key: array
desc: 数组
---



## 定义方式

### 动态大小数组

```solidity
uint[] public arr;
uint[] public arr2 = [1,2,3];
```

### 固定大小数组

```solidity
uint[10] public myarr; //全部为默认值
uint[10] public myarr2 = [9]; //myarr2[0]为9 , 其他为默认值
```



## 操作

https://docs.soliditylang.org/en/v0.8.17/types.html?highlight=array#array-members

### push

```solidity
//对于动态大小数组和bytes (not string),进行append, 长度增加1
arr.push(i); //将值push到末尾
arr.push(); //将默认值push到末尾
```

### pop

```solidity
//对于动态大小数组和bytes (not string),删除最后一个元素, 长度减少1
//pop不会返回弹出的值
//被pop的元素的值会被重置为默认值
arr.pop();
```



### length

```solidity
uint256 len = arr.length;
```



### delete

```solidity
//重置 arr[index]的值为默认值
delete arr[index];
```



### 切片



```solidity
//其中start和end是导致uint256类型的表达式（或隐含地可转换为uint256）。分片的第一个元素是x[start]，最后一个元素是x[end - 1]。
arr[start:end]
```

如果start大于end或者end大于数组的长度，就会产生一个异常。

start和end都是可选的：start默认为0，end默认为数组的长度。

切片没有任何成员。它们可以隐含地转换为其底层类型的数组并支持索引访问。索引访问在底层数组中不是绝对的，而是相对于分片的开始。

切片没有类型名，这意味着任何变量都不能将阵列片作为类型，它们只存在于中间表达式中。

```solidity
function forward(bytes calldata payload) external {
        bytes4 sig = bytes4(payload[:4]);
        //...
}
```



## js 获取值

非标准玩法 (标准玩法是合约中应该提供一个get函数)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Temp {
    uint256[3] public fixedArray2 = [9, 8, 7];
}

```

```js
const Temp = artifacts.require("Temp");

contract("Temp", function (/* accounts */) {
  it("test xxx", async function () {
    let instance = await Temp.deployed();
    //通过index访问
    let v = await instance.fixedArray2(1);
    //输出 8
    console.log(v.toNumber());
  });

});
```



## 风险: 悬垂引用(Dangling References)

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0 <0.9.0;

contract C {
    uint[][] s;

    function f() public {
        // Stores a pointer to the last array element of s.
        uint[] storage ptr = s[s.length - 1];
        // Removes the last array element of s.
        s.pop();
        // Writes to the array element that is no longer within the array.
        ptr.push(0x42);
        // Adding a new element to ``s`` now will not add an empty array, but
        // will result in an array of length 1 with ``0x42`` as element.
        s.push();
        assert(s[s.length - 1][0] == 0x42);
    }
}
```

悬垂引用（Dangling References）是指引用的对象已经被删除或者重新分配了内存，但引用本身还存在的情况。这种情况下，引用指向的内存地址可能被其他内容覆盖，导致引用指向错误的内容。

在上面的代码中，"ptr" 变量是一个指向 "s" 数组的最后一个元素的指针。但是在 "f" 函数的第二行，我们使用 "pop" 函数删除了 "s" 数组的最后一个元素。这意味着 "ptr" 指针指向的内存地址可能被重新分配，或者被其他内容覆盖。

在这种情况下，如果你使用 "ptr" 指针来访问或修改数据，可能会导致错误的结果。因此，在上面的代码中存在悬垂引用的风险。
