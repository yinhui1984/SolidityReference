---
key: assert
desc: 断言
---

```solidity
assert(bool condition)
```



如果条件为 `false`，则中止执行并恢复状态变化（主要用于代码内部错误）。

并且, 错误发生后会消耗掉剩余`gas`, 不会归还剩余`gas`

