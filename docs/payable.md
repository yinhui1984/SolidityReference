---
key: payable
desc: payable关键字
---



## 含义

`payable` 可以用于修饰:

+ 地址: `address payable addr` 表示该地址可以接受Ether
+ 函数(包括构造函数): `function xxx public payable{}` :表示可以通过改函数向对应的合约地址发生Ether, Ether的发送方是`msg.sender`, Ether的数量是`msg.value` (单位wei)



## 容易混淆的点

### 调用payable函数向合约发送ether

当合约有一个payable函数, 比如

```solidity
    function donate() public payable {
        emit EtherReceived(msg.sender, msg.value);
    }
```

外部调用该函数向合约地址发送ether时, 合约是**不需要**`receive`或 `fallback`函数的

比如

```js
    await instance.donate({
      from: accounts[0],
      value: 10000
    })
```

 ### 直接向合约地址发送ether

直接向合约地址发送ether时, 比如

```js
    await web3.eth.sendTransaction({
      from: accounts[0],
      to: instance.address,
      value: 10000
    })
```

这时合约**需要**`receive`或 `fallback`函数的



## 举例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PayableDemo {
    address payable public owner;
    event EtherReceived(address from, uint256 amount);
    event EtherWithdraw(address to, uint256 amount);

    constructor() {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    function donate() public payable {
        emit EtherReceived(msg.sender, msg.value);
    }

    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        //注意： owner是 payable的
        (bool ok, ) = owner.call{value: balance}("");
        require(ok, "Failed to withdraw");
        emit EtherWithdraw(owner, balance);
    }

    // receive()是为了能够直接向合约地址发送ether
    receive() external payable {}
}

```

```js
const PayableDemo = artifacts.require("PayableDemo");

contract("PayableDemo", function (/* accounts */) {
  it("should assert true", async function () {
    let instance = await PayableDemo.deployed();
    let accounts = await web3.eth.getAccounts();

    //调用payable函数发送ether， 合约不需要receive函数
    await instance.donate({
      from: accounts[1],
      value: 10000
    })

    let balance = await web3.eth.getBalance(instance.address);
    assert.equal(balance, 10000, "Balance should be 10000 wei");

    //直接向合约地址发送ether,合约需要receive函数
    await web3.eth.sendTransaction({
      from: accounts[1],
      to: instance.address,
      value: 10000
    })
    balance = await web3.eth.getBalance(instance.address);
    assert.equal(balance, 20000, "Balance should be 20000 wei");


    await instance.withdraw();
    balance = await web3.eth.getBalance(instance.address);
    assert.equal(balance, 0, "Balance should be 0 wei");
  });
});

```



```

  Contract: PayableDemo
    ✔ should assert true (97ms)

    Events emitted during test:
    ---------------------------

    PayableDemo.EtherReceived(
      from: 0x8F3b7a4aC286dfF354534Cc875028A8Eb235aFc4 (type: address),
      amount: 10000 (type: uint256)
    )

    PayableDemo.EtherWithdraw(
      to: 0x6bb44376acF37ee3cEb584289f4B9B037c8f6a7D (type: address),
      amount: 20000 (type: uint256)
    )


    ---------------------------
```

