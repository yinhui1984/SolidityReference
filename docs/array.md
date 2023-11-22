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





## 存储(storage)

参考这篇文章 https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/

总的说来, 固定大小的数组, 按照器声明的位置和大小,存储在固定的slot上

动态大小的数组, 声明位置对应的slot存储的是数组的大小, 数据的实际存储位置的起始位置是slot编号的hash值,然后进行的连续存储.

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

>Index range access is only supported for dynamic calldata arrays.
>
>仅仅支持动态的calldata数组



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
				 // 仅仅支持动态的calldata数组
        bytes4 sig = bytes4(payload[:4]);
        //...
}
```

比如下面这个存在错误:

```solidity
contract ArrayDemo {
    uint[] dynamicArray = [9, 99, 999];

    // 语法错误：Index range access is only supported for dynamic calldata arrays
    function SliceDynamicArray(
        uint start,
        uint end
    ) public view returns (uint[] memory) {
        return dynamicArray[start:end];
    }
}
```

如果需要这个功能,就只能这样:

```solidity
contract ArrayDemo {
    uint[] dynamicArray = [9, 99, 999];

    function SliceDynamicArray(uint start, uint end) public view returns (uint[] memory) {
        require(end > start, "Invalid index range");
        require(end <= dynamicArray.length, "End index out of bounds");

        uint[] memory slicedArray = new uint[](end - start);
        for (uint i = start; i < end; i++) {
            slicedArray[i - start] = dynamicArray[i];
        }

        return slicedArray;
    }
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
pragma solidity ^0.8.10;

contract DanglingReferenceDemo {
    struct MyStruct {
        uint data;
    }

    MyStruct[] public myStructs;

    function createStruct() public {
        MyStruct memory myStruct = MyStruct({data: 123});
        myStructs.push(myStruct);
    }

    function deleteStruct(uint index) public {
        delete myStructs[index];
    }

    function getStructData(uint index) public view returns (uint) {
        MyStruct storage myStruct = myStructs[index];
        return myStruct.data;
    }
}

```

悬垂引用（Dangling References）是指引用的对象已经被删除或者重新分配了内存，但引用本身还存在的情况。这种情况下，引用指向的内存地址可能被其他内容覆盖，导致引用指向错误的内容。

在这个合约中，有三个函数：

1. `createStruct`: 创建一个新的结构体并将其添加到`myStructs`数组中。
2. `deleteStruct`: 删除`myStructs`数组中指定索引的结构体。
3. `getStructData`: 返回`myStructs`数组中指定索引的结构体数据。

悬垂引用的风险出现在`deleteStruct`函数中。当调用`delete`关键字删除数组中的一个元素时，该元素的内容被重置为其类型的默认值，但数组的长度保持不变。这意味着即使结构体被删除，数组中仍然保留着一个指向其原始内存位置的槽位。

如果在调用`deleteStruct`之后，再调用`getStructData`来访问同一索引的数据，这时你将访问一个已经被删除的结构体。这就是一个悬垂引用的例子，因为`myStruct`变量在`getStructData`函数中仍然引用着被删除元素的地址。但由于该元素已被删除，其数据不再可靠，可能包含错误或不可预测的值。

为了避免这种情况，合约应该在删除元素后更新其引用，或者在访问任何元素之前检查它的有效性。在Solidity中处理动态数组时，这是一个需要特别注意的安全考虑。



要避免悬垂引用的问题，您需要确保在删除数组元素后，不再访问被删除的元素。在Solidity中，删除数组元素通常意味着将元素设置为其类型的默认值，但不会缩短数组的长度。为了安全地处理数组元素的删除，您可以采用以下两种方法之一：

1. **移动数组最后一个元素到被删除元素的位置**：这种方法在删除元素后保持数组的紧凑性，但会改变元素的顺序。

   ```solidity
   pragma solidity ^0.8.10;
   
   contract DanglingReferenceDemo {
       struct MyStruct {
           uint data;
           bool isValid;
       }
   
       MyStruct[] public myStructs;
   
       function createStruct() public {
           MyStruct memory myStruct = MyStruct({data: 123, isValid: true});
           myStructs.push(myStruct);
       }
   
       function deleteStruct(uint index) public {
           require(index < myStructs.length, "Index out of bounds");
           myStructs[index] = myStructs[myStructs.length - 1];
           myStructs.pop(); // Removes the last element
       }
   
       function getStructData(uint index) public view returns (uint) {
           require(index < myStructs.length, "Index out of bounds");
           require(myStructs[index].isValid, "Struct is not valid");
           return myStructs[index].data;
       }
   }
   
   ```

2. **简单地标记元素为已删除**：在这种方法中，您不实际从数组中移除元素，而是将其标记为无效或已删除，这种方法不会影响数组的顺序，但可能会导致数组中有一些无用的元素。

   ```solidity
   pragma solidity ^0.8.10;
   
   contract DanglingReferenceDemo {
       struct MyStruct {
           uint data;
           bool isValid;
       }
   
       MyStruct[] public myStructs;
   
       function createStruct() public {
           MyStruct memory myStruct = MyStruct({data: 123, isValid: true});
           myStructs.push(myStruct);
       }
   
       function deleteStruct(uint index) public {
           require(index < myStructs.length, "Index out of bounds");
           myStructs[index].isValid = false; // 标记为已删除
       }
   
       function getStructData(uint index) public view returns (uint) {
           require(index < myStructs.length, "Index out of bounds");
           require(myStructs[index].isValid, "Struct is not valid"); // 检查元素是否有效
           return myStructs[index].data;
       }
   }
   
   ```

   这种方法的优点是它保持了数组元素的顺序，但可能导致数组中有一些“空洞”，即无效的元素。在处理大量数据时，这可能导致资源浪费。
