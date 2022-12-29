---
key: mapping
desc: mapping
---

```solidity
mapping(T1 => T2) mymap
```



> mapping 不存在length
>
> mapping 无法 iterate (可以将mapping进行封装而实现iterable)
>
> 不能删除键值对, delete myMap[key] 只是将其重置为默认值

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Temp {
    mapping(uint256 => uint256) map;

    function insertToMap(uint256 _key, uint256 _value) public {
        //key不存在则插入， 存在则更新
        map[_key] = _value;
    }

    function getFromMap(uint256 _key) public view returns (uint256) {
        //获取值， 如果key不存在则会返回value的默认值
        return map[_key];
    }

    function deleteFromMap(uint256 _key) public {
        //无论key是否存在，都是将map[_key]重置为默认值
        delete map[_key];
    }
}

```

官方文档

https://docs.soliditylang.org/en/v0.8.17/types.html?highlight=delete#mapping-types



## key 和value允许的类型

<img src="https://github.com/yinhui1984/imagehosting/blob/main/images/1672293665096381000.jpg?raw=true" alt="image" style="zoom:50%;" />

### Iterable Mappings

https://docs.soliditylang.org/en/v0.8.17/types.html#iterable-mappings