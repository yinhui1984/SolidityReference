---
key: address
desc: 地址
---



地址类型: https://docs.soliditylang.org/zh/latest/types.html#address

地址类型成员: https://docs.soliditylang.org/zh/latest/units-and-global-variables.html#address-related



## balance

`<address>.balance` （ `uint256` ）以 Wei 为单位的 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的余额。



## code

`<address>.code` （ `bytes memory` ）在 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的代码（可以是空的）。



## codehash

`<address>.codehash` （ `bytes32` ）[地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 的代码哈希值



## transfer

```
<address payable>.transfer(uint256 amount)
```

向 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 发送数量为 amount 的 Wei，失败时抛出异常，发送 2300 gas 的矿工费，不可调节。



## send

```
<address payable>.send(uint256 amount) returns (bool)
```

向 [地址类型](https://docs.soliditylang.org/zh/latest/types.html#address) 发送数量为 amount 的 Wei，失败时返回 `false` 2300 gas 的矿工费用，不可调节。



## call

```
<address>.call(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `CALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。



## delegatecall

```
<address>.delegatecall(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `DELEGATECALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。



## staticcall

```
<address>.staticcall(bytes memory) returns (bool, bytes memory)
```

用给定的数据发出低级别的 `STATICCALL`，返回是否成功的结果和数据，发送所有可用 gas，可调节。