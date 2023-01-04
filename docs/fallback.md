---
key: fallback
desc: 回退函数
---

```solidity
fallback() external payable{
}

//fallback 可选性地接受bytes作为输入和输出。
fallback(bytes calldata data) external payable returns (bytes memory) {
  
}
```





`fallback`是一个特殊的函数，在以下情况下被执行，即

+ 一个不存在的函数被调用

  或

+ 以太被直接发送至一个合约，但receive()不存在或msg.data不是空的时候

  

当被transfer或send调用时，fallback有2300的气体限制。



更多的,参考这里:

 https://solidity-by-example.org/fallback/

https://yinhui1984.github.io/solidity_fallback_receive_function/