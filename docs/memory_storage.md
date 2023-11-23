---
key: memory, storage
desc: memory and storage
---



# memory and storage



## 解释

在Solidity编程语言中，内存和存储是用于存储变量的两种不同类型的数据位置。

memory是一个临时的数据位置，用于在一个函数的执行过程中存储数值。它可以被认为是计算机的RAM，当程序运行时，数据被暂时储存在那里。内存变量是使用Solidity中的`memory`关键字创建的，一旦其对应的函数完成执行，它们就会被清除。

另一方面，storage是指以太坊区块链上的持久性数据存储。存储变量在交易之间持续存在，即使在合约终止后也仍然存储在链上。它们可以被认为类似于你电脑上的硬盘空间，在那里保存着像文件或文档这样的永久信息。

> storage 相当于一个指向实际存储位置的指针

Solidity使用一个抽象的键值映射结构，称为 "storage"，允许开发人员在智能合约的状态变量中永久存储复杂的结构，如数组或结构（直到明确删除）。

关于Solidity中的存储使用，需要注意的一件事是gas成本--它比内存需要更多的gas，因为写入它涉及到更新区块链状态，这需要花费金钱（ether）。

为了在处理大量结构化数据时优化gas消耗，开发人员经常在函数中使用内存进行临时操作，然后在特定的时间间隔内将其提交到永久存储中，而不是直接将每个变化立即写入链中。





## example

```solidity
// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.10;

contract MyContract {

    // address : key : content
    mapping(address=>mapping(uint256 => string) )data;


    function getData(address addr, uint256 key) public view  returns(string memory) {
        return data[addr][key];
    }

    function setData(address addr, uint256 key, string memory content) public{
        //storage 相当于一个指向硬盘存储位置的指针
        mapping(uint256 => string) storage dd = data[addr];
        //更新了storage变量， 事件存储也会更新
        dd[key] = content;
    }


    function test() external{
        setData(address(this), 0, "haha");
    }

}

```

