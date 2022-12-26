---
key: require
desc: 条件检查
---



```solidity
require(bool condition)
```

```solidity
require(bool condition, string memory message)
```

如果条件为 `false`，则中止执行**并恢复状态变化**（主要用于错误的输入或外部组件的错误） (同时提供错误信息)

当错误发生时, 与`assert`不同, 其会归还剩余`gas`

