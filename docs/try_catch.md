---
key: try, catch
desc: try...catch..
---

详细的参考官方文档:

https://docs.soliditylang.org/zh/v0.8.17/control-structures.html#try-catch






```solidity
try xxx {
	 
}catch{

}
```



> `try` 后面 (也就是上面的XXX位置)只能是
>
> + 外部函数调用(调用的其他合约的函数)
> + 合约创建



```solidity
        for (uint256 i = 0; i < 8191; i++) {
            try keeper.enter{gas: 2500000 + i}(key) {
                break;
            } catch {}
        }
```



更多的示例:

https://solidity-by-example.org/try-catch/



使用`try...catch` 捕获error: 参考error.md
