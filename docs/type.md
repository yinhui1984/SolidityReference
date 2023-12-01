---
key: type,name,creationCode,runtimeCode,interfaceId,min,max
desc: 类型信息获取
---

>目前只支持合约,整数和接口类型

https://docs.soliditylang.org/zh/latest/units-and-global-variables.html#meta-type



表达式 `type(X)` 可以用来检索关于 `X` 类型的信息。 目前，对这一功能的支持是有限的（ `X` 可以是合约类型或整数型），但在未来可能会扩展。

以下是合约类型 `C` 的可用属性：

- `type(C).name`

  合约的名称。

- `type(C).creationCode`

  内存字节数组，包含合约的创建字节码。 可以在内联程序中用来建立自定义的创建程序， 特别是通过使用 `create2` 操作码。 这个属性 **不能** 在合约本身或任何派生合约中被访问。 它会导致字节码被包含在调用站点的字节码中，因此像这样的循环引用是不可能的。

  ```solidity
  contract HelloContract {
      function hello() public pure returns (string memory) {
          return "Hello World";
      }
  }
  
  contract NewCreateDemo{
  
   
      function CreateHelloContract() public returns (address) {
          bytes memory creationCode = type(HelloContract).creationCode;
          address addr;
  
          assembly {
              // Yul的create函数，参数分别是：value，code的起始位置，code的长度
              // creationCode是一个指向内存某个位置的指针（这里是指向bytes动态数组位置）
              // 0x20 是因为前面0x20个字节(也就是32个字节)是指针的长度，
              // 因为存储动态长度数据（如字节数组）时，会在数据本身之前存储一个32字节的长度前缀。这个长度前缀表示数据的长度
              // 所以add(creationCode, 0x20) 是指针指向数据的位置（跳过长度前缀，数据的实际位置）
              // mload(xxx)读取指针指向的数据，其返回xxx位置开始的32个字节的数据，也就是creationCode指针指向的数据的前32个字节，也就是长度前缀
              // 所以mload(creationCode)就返回了creationCode的长度
              addr := create(0, add(creationCode, 0x20), mload(creationCode))
          }
  
          // 如果创建失败，create会返回0x0地址
          require(addr != address(0), "create failed");
  
          return addr;
      }
  
  }
  ```

  

- `type(C).runtimeCode`

  内存字节数组，包含合约运行时的字节码。 通常是由 `C` 的构造函数部署的代码。 如果 `C` 有一个使用内联汇编的构造函数，这可能与实际部署的字节码不同。 还要注意的是，库合约在部署时修改其运行时字节码，以防止常规调用。 与 `.creationCode` 相同的限制也适用于这个属性。



>runtimeCode 与 creationCode的比较
>
>https://medium.com/authereum/bytecode-and-init-code-and-runtime-code-oh-my-7bcd89065904
>
>https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-ii-creation-vs-runtime-6b9d60ecb44c/

除了上述属性外，以下属性对接口类型 `I` 可用：

- `type(I).interfaceId`:

  一个 `bytes4` 值，是包含给定接口 `I` 的 [EIP-165](https://eips.ethereum.org/EIPS/eip-165) 接口标识符。 这个标识符被定义为接口本身定义的所有函数选择器的 `XOR`，不包括所有继承的函数。

以下属性可用于整数类型 `T`：

- `type(T).min`

  类型 `T` 所能代表的最小值。

- `type(T).max`

  类型 `T` 所能代表的最大值。