---
key: new, create, create2
desc: 合约创建
---

有几种不同的方法可以从现有的智能合约创建智能合约。

一种方法是在 Solidity 中使用 `new` 关键字。 Solidity 中的 `new` 关键字用于创建智能合约的新实例。

还有的方法是使用低级函数`create`或`create2` 

## 在 智能合约函数中使用 `new`关键字将导致：

+ 部署一个新的合约
+ 初始化状态变量
+ 执行新合约的构造函数
+ 将新合约的nonce值设置为1
+ 返回给调用者的新合约实例的地址



> 新合约的地址是如何被计算出来的?
>
> 根据sender地址和sender的nonce值
>
> ```solidity
> new_contract_address = keccak256(rlp.encode([sender_address, nonce]))[12:]
> // [12:]表示取哈希值的最后20字节。
> ```
>
> 1. **地址**：取合约创建者（发送者）的以太坊地址。
> 2. **Nonce**：取发送者账户的nonce值。注意，在以太坊中，nonce是发送者发起的交易数，对于合约账户，nonce从1开始计数。
> 3. **组合和散列**：将发送者的地址和nonce组合起来，然后使用Keccak-256哈希算法（以太坊使用的加密哈希函数）进行散列。具体来说，先将发送者的地址转换为20字节的形式，然后将nonce转换为RLP（递归长度前缀）编码格式，这是以太坊用于编码结构化数据的一种方式。然后将这两部分数据连接起来，对结果进行Keccak-256散列。
> 4. **取哈希的最后20字节**：由于以太坊地址是20字节长度，因此从散列值的最后20字节中提取出来，这就是新创建的合约的地址。
>
> 这种方法确保了每个新创建的合约都有一个独一无二的地址，因为每次交易后发送者的nonce都会增加，所以即使同一个账户多次部署相同的合约，每次得到的合约地址也会不同。



## 成功使用`new`的前提

+ 创建新合约的代码在执行前就已经知道了
+ 新合约的地址是由创建合约的地址计算出来的。
+ 创建一个新的合约需要一个gas费用，以完成该操作



## Use case

有很多用例需要一个智能合约来创建其他合约。`new`关键字对于保持你的应用程序的通用性很有用。作为一个例子，自动做市商（AMM），如Uniswap和Pancake Swap，使用`new`关键字来创建交易对。阅读[这里](https://cryptomarketpool.com/how-do-the-uniswap-solidity-smart-contracts-work/)，了解更多关于Ethereum上的Uniswap solidity智能合约。

创建其他合约的合约通常被称为工厂合约(**factory contracts**)。作为一个例子，Uniswap工厂合约被用来创建交易对。此外，关于Uniswap工厂合约的信息可以在[这里](https://docs.uniswap.org/protocol/reference/core/interfaces/IUniswapV3Factory)找到。



## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

//账户
contract UserAccount {
    address public company;
    address public user;
    string public name;

    constructor(address _user, string memory _name) payable {
        company = msg.sender;
        user = _user;
        name = _name;
    } 

}

// 下面的AccountFactory合约将部署上面UserAccount合约中的代码
contract AccountFactory {
    // 状态变量数组，用于跟踪使用该合约创建的账户。
    UserAccount[] public useraccounts;


    // 这个函数需要两个参数。 一个用户的帐号和一个名字
    function CreateUserAccount(address _user, string memory _name) external payable{
        // new关键字用于创建一个新的合约

        // 如果要发生ether到新合约,则使用UserAccount{value: "amount"}(_user, _name);
        UserAccount account = new UserAccount(_user, _name);
        useraccounts.push(account);
    }

}
```



> 官方示例:
>
> https://docs.soliditylang.org/en/v0.8.9/control-structures.html?highlight=new%20keyword#creating-contracts-via-new





## create

```
create(v, p, n)  
//create new contract with code mem[p…(p+n)) and send v wei and return the new address; returns 0 on error
```

v: 表示创建时发送到合约的wei数量

p: 表示指向creation code的指针位置,节码通常是通过Solidity的`type(Contract).creationCode`获取，或者可以是任何其他有效的EVM字节码

n: 表示creation code的长度,它告诉`create`函数有多少字节的数据需要从提供的字节码中复制来创建新合约

返回值为创建的新合约的地址,如果创建失败则返回`0x0`

示例:

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
```

> 如果要创建的合约的构造函数带有参数, 则传递的createCode需要带有参数信息

示例:

```solidity
contract HelloContractWithArgs {

    string private greetings;
    constructor(string memory _greetings) {
        greetings = _greetings;
    }

    function hello() public view returns (string memory) {
        return greetings;
    }
}

contract NewCreateDemo{
	    function CreateHelloContractWithArgs(string calldata greetings) public returns (address) {
        bytes memory creationCode = type(HelloContractWithArgs).creationCode;
        bytes memory creationCodeWithArgs = abi.encodePacked(creationCode, abi.encode(greetings));
        address addr;

        assembly {
            addr := create(0, add(creationCodeWithArgs, 0x20), mload(creationCodeWithArgs))
        }

        require(addr != address(0), "create failed");

        return addr;
    }
```

## create2

```
create2(v, p, n, s)
// create new contract with code mem[p…(p+n)) at address keccak256(0xff . this . s . keccak256(mem[p…(p+n))) and send v wei and return the new address, where 0xff is a 1 byte value, this is the current contract’s address as a 20 byte value and s is a big-endian 256-bit value; returns 0 on error
```

v: 同create

p:  同create

n: 同create

s: `bytes32`类型, 一个256位的哈希值，用于影响新合约的地址。通过改变`salt`，即使使用相同的部署字节码和创建者地址，也可以生成不同的合约地址。比如`bytes32 salt = bytes32(keccak256(abi.encodePacked("my_salt")));` 或 `bytes32 salt = bytes32(0x1234567890123456789012345678901234567890123456789012345678901234);`

返回值: 同create



当创建一个合约时，合约的地址是由创建合约的地址和一个计数器计算出来的，这个计数器在每次创建合约时都会增加。

如果你指定了`salt`的选项（一个字节32的值），那么合约创建将使用不同的机制来得出新合约的地址。

它将从创建合约的地址、给定的`salt`值、创建合约的（creation）bytecode和构造器参数中计算出地址。

<u>**特别是，计数器（"nonce"）不被使用**。</u>这允许在创建合约时有更多的灵活性。你能够在新合约被创建之前推导出它的地址。此外，在创建合约的同时创建其他合约的情况下，你也可以依靠这个地址。

这里的主要用例是作为链外互动的judges的合约，只有在有争议的时候才需要创建。

>在salt creation方面，有一些特殊性。一个合约在被销毁后可以在同一地址重新创建。然而，新创建的合约有可能有不同的部署字节码，即使创建字节码是相同的（这是一个要求，因为否则地址会改变）。这是由于编译器可以查询两次创建之间可能发生变化的外部状态，并在存储之前将其纳入部署的字节码中。

举例:

```solidity
contract HelloContractWithArgs {

    string private greetings;
    constructor(string memory _greetings) {
        greetings = _greetings;
    }

    function hello() public view returns (string memory) {
        return greetings;
    }
}


contract NewCreateDemo{
	    function Create2HelloContractWithArgs(string calldata greetings,  bytes32 salt) public returns (address) {

        // 方式1

        // bytes memory creationCode = type(HelloContractWithArgs).creationCode;
        // bytes memory CreationCodeWithArgs = abi.encodePacked(creationCode, abi.encode(greetings));
        // address addr;

        // assembly {
        //     addr := create2(0, add(CreationCodeWithArgs, 0x20), mload(CreationCodeWithArgs), salt)
        // }


        // 方式2
        address addr = address(new HelloContractWithArgs{salt: salt}(greetings));
        
        
        require(addr != address(0), "create failed");
        return addr;
    }
```



> 既然create2的优点是可以预先计算出地址, 那地址是如何计算的?
>
> ```solidity
> keccak256( 0xff ++ deploying_address ++ salt ++ keccak256(init_code))[12:]
> ```
>
> - `0xff`：一个固定的前缀。
> - `deploying_address`：部署合约的地址, 就是使用了create2代码的合约的地址。
> - `salt`：一个`bytes32`值，用于影响生成的地址。
> - `keccak256(init_code)`：新合约的初始化代码的Keccak-256哈希值。
> - `[12:]`：取哈希结果的最后20个字节作为地址。

对于上面的地址可以如下计算出部署地址

```solidity
string memory greetings = "Hello World With Args (Create2)";
bytes memory creationCodeWithArgs = abi.encodePacked(
            type(HelloContractWithArgs).creationCode,
            abi.encode(greetings)
        );
address predictAddress = address(
            (
                uint160(
                    uint256(
                        keccak256(
                            abi.encodePacked(
                                bytes1(0xff),
                                // 注意这里地址是谁使用的create2，就是谁的地址
                                address(newDemo), 
                                salt,
                                keccak256(creationCodeWithArgs)
                            )
                        )
                    )
                )
            )
        );
```





## 完整的示例代码

### new_create_demo.sol

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;


contract HelloContract {
    function hello() public pure returns (string memory) {
        return "Hello World";
    }
}

contract HelloContractWithArgs {

    string private greetings;
    constructor(string memory _greetings) {
        greetings = _greetings;
    }

    function hello() public view returns (string memory) {
        return greetings;
    }
}

contract NewCreateDemo{

    function NewHelloContract() public returns (address) {
        HelloContract hello = new HelloContract();
        return address(hello);
    }

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

    function CreateHelloContractWithArgs(string calldata greetings) public returns (address) {
        bytes memory creationCode = type(HelloContractWithArgs).creationCode;
        bytes memory creationCodeWithArgs = abi.encodePacked(creationCode, abi.encode(greetings));
        address addr;

        assembly {
            addr := create(0, add(creationCodeWithArgs, 0x20), mload(creationCodeWithArgs))
        }

        require(addr != address(0), "create failed");

        return addr;
    }

    function Create2HelloContractWithArgs(string calldata greetings,  bytes32 salt) public returns (address) {

        // 方式1

        bytes memory creationCode = type(HelloContractWithArgs).creationCode;
        bytes memory CreationCodeWithArgs = abi.encodePacked(creationCode, abi.encode(greetings));
        address addr;

        assembly {
            addr := create2(0, add(CreationCodeWithArgs, 0x20), mload(CreationCodeWithArgs), salt)
        }


        // 方式2
        // address addr = address(new HelloContractWithArgs{salt: salt}(greetings));
        
        
        require(addr != address(0), "create failed");
        return addr;
    }

}
```



### new_create_demo.t.sol

```solidity
// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.11;

import "forge-std/Test.sol";
import "../src/new_create_demo.sol";

contract NewDemoTest is Test {
    NewCreateDemo newDemo;
    HelloContract hello;
    HelloContractWithArgs helloWithArgs;

    function setUp() public {
        vm.createSelectFork("theNet");
        newDemo = new NewCreateDemo();
    }

    function testNewHelloContract() public {
        address helloAddr = newDemo.NewHelloContract();
        hello = HelloContract(helloAddr);
        console2.log(hello.hello());
    }

    function testCreateHelloContract() public {
        address helloAddr = newDemo.CreateHelloContract();
        hello = HelloContract(helloAddr);
        console2.log(hello.hello());
    }

    function testCreateHelloContractWithArgs() public {
        address helloAddr = newDemo.CreateHelloContractWithArgs(
            "Hello World With Args"
        );
        helloWithArgs = HelloContractWithArgs(helloAddr);
        console2.log(helloWithArgs.hello());
    }

    function testCreate2HelloContractWithArgs() public {
        string memory greetings = "Hello World With Args (Create2)";
        bytes32 salt = bytes32(keccak256(abi.encodePacked("my_salt")));

        address helloAddr = newDemo.Create2HelloContractWithArgs(
            greetings,
            salt
        );
        helloWithArgs = HelloContractWithArgs(helloAddr);
        console2.log(helloWithArgs.hello());

        console2.logAddress(helloAddr);

        bytes memory creationCodeWithArgs = abi.encodePacked(
            type(HelloContractWithArgs).creationCode,
            abi.encode(greetings)
        );

        address predictAddress = address(
            (
                uint160(
                    uint256(
                        keccak256(
                            abi.encodePacked(
                                bytes1(0xff),
                                // 注意这里地址是谁使用的create2，就是谁的地址
                                address(newDemo), 
                                salt,
                                keccak256(creationCodeWithArgs)
                            )
                        )
                    )
                )
            )
        );
        console2.logAddress(predictAddress);
        assertTrue(predictAddress == helloAddr);

        address helloAddrUpgraded = newDemo.Create2HelloContractWithArgs("[Upgraded] Hello World With Args (Create2)", salt);
        assertFalse(helloAddrUpgraded == helloAddr);
    }
}

```

