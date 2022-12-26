---
key: revert
desc: 回滚
---

```solidity
revert()
```

```solidity
revert(string memory message)
```



回滚操作是指在执行合约代码时，撤销已执行的修改，并将交易失败标记为错误。

你可以使用 `revert` 函数来执行回滚操作。例如，你可以使用 `revert()` 函数来回滚所有已执行的修改，使用 `revert("Error message")` 函数来回滚所有已执行的修改，并返回一条错误信息。