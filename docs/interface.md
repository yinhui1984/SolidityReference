---
key: interface
desc: 接口
---

```solidity
interface IXXX{
	
}
```



## 知识点

+ 接口没有函数实现, 只有定义 (编译接口, 其只有ABI, 没有Bytecode)

+ 如果一个合约只实现了接口的一部分, 那么这个合约必须声明为`abstract`

+ 接口中的函数默认隐式声明为`virtual` 

+ 定义在接口内的函数只能被声明为外部函数(`external`)。它们不能被定义为公共的、内部的或私有的。但实现接口的合约,在覆盖函数时可以将`external`改为`public`

  ```solidity
  interface IGreetor {
      function sayHi() external pure returns (string memory);
  }
  contract You is IGreetor {
      // external and public will be ok both.
      //function sayHi() external pure returns (string memory) {
      //    return "hi, You";
      //}
      function sayHi() public pure returns (string memory) {
          return "hi, You";
      }
  }
  ```

  

+ 从0.8.8版本开始, 除非在多个基类中定义了同名函数，否则在覆盖接口函数时不需要使用 `override` 关键字。
  在多个基类中定义了同名函数时, 使用 `override` 关键字来明确指定覆盖
  https://docs.soliditylang.org/en/v0.8.13/contracts.html#function-overriding

  ```solidity
  // SPDX-License-Identifier: MIT
  pragma solidity ^0.8.8;
  
  interface IGreetor {
      function sayHi() external pure returns (string memory);
  }
  
  contract Presenter {
      function sayHi() external pure virtual returns (string memory) {
          return "hi, i am Presenter";
      }
  }
  
  contract You is IGreetor {
      function sayHi() external pure returns (string memory) {
          return "hi, You";
      }
  }
  
  contract Me is IGreetor, Presenter {
      function sayHi()
          external
          pure
          override(IGreetor, Presenter)
          returns (string memory)
      {
          return "hi, it's me";
      }
  }
  
  ```

+ 接口内部**可以**声明枚举,结构体, 事件 并且可以被外部合约访问.
    但**不能**定义状态变量,常量,modifier, 构造器
```solidity
 interface Switch {
    enum Status { ON, OFF }
}
contract FuseBox {
    Switch.Status room;
    Switch.Status kitchen;
}
```

+ 接口可以继承接口, 但不能继承合约

+ 接口里的函数可以重载

  ```solidity
  interface ICountry {
      function greetings() external pure returns (string memory);
    
      function greetings(string memory _name) 
          external 
          pure 
          returns (string memory);
  }
  ```
  
  