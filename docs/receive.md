---
key: receive
desc: 接收以太的函数
---

一个合约最多可以有一个 `receive` 函数， 使用 `receive() external payable { ... }` 来声明。（没有 `function` 关键字）。 这个函数不能有参数，不能返回任何东西，必须具有 `external` 的可见性和 `payable` 的状态可变性。 它可以是虚拟的，可以重载，也可以有修饰器。

receive 函数是在调用合约时执行的，<u>并带有空的 calldata</u>。 这是在纯以太传输（例如通过 `.send()`或 `.transfer()` ）时执行的函数。 如果不存在这样的函数，但存在一个 payable 类型的 [fallback函数](https://docs.soliditylang.org/zh/latest/contracts.html#fallback-function)， 这个 fallback 函数将在纯以太传输时被调用。 如果既没有直接接收以太（receive函数），也没有 payable 类型的 fallback 函数， 那么合约就不能通过不代表支付函数调用的交易接收以太币，还会抛出一个异常

在最坏的情况下， `receive` 函数只有2300个气体可用（例如当使用 `send` 或 `transfer` 时）， 除了基本的记录外，几乎没有空间来执行其他操作。以下操作的消耗气体将超过2300气体的规定：

- 写入存储
- 创建合约
- 调用消耗大量 gas 的外部函数
- 发送以太币

>**没有接收以太币功能的合约可以作为 coinbase交易（又称 *矿工区块奖励*）的接收者 或作为 `selfdestruct` 的目的地接收以太币。**
>
>合约不能对这样的以太币转移做出反应，因此也不能拒绝它们。 这是EVM的一个设计选择，Solidity无法绕过它。
>
>这也意味着 `address(this).balance` 可以高于合约中 实现的一些手工记帐的总和（即在接收以太函数中更新的累加器）





## receive()和fallback()

`receive()` 函数

- `receive()` 是一个特殊的函数，没有参数，也没有返回值。
- 它在合约接收以太坊且调用数据为空（即纯以太坊转账）时被调用。

`fallback()` 函数

- `fallback()` 函数也是一个特殊的函数，没有名称，但可以接受以太坊。
- 它在合约接收以太坊但调用数据非空，或者没有匹配到任何函数时被调用

### 调用逻辑

当以太坊发送到一个合约时，以下规则决定了是调用 `receive()` 还是 `fallback()`：

1. **如果调用数据为空**：
   - 如果合约中定义了 `receive()` 函数，则调用 `receive()`。
   - 如果没有定义 `receive()` 函数，但定义了 `fallback()` 函数，则调用 `fallback()`。
2. **如果调用数据非空**：
   - 如果调用数据匹配某个函数的签名，则调用该函数。
   - 如果调用数据不匹配任何函数的签名，则：
     - 如果定义了 `fallback()` 函数，则调用 `fallback()`。
     - 如果没有定义 `fallback()` 函数，交易将失败



## 特殊情况下接收以太

### 矿工区块奖励（Coinbase 交易）

在创建新区块时，矿工会获得区块奖励，这通常涉及将新创建的以太币发送到矿工指定的地址。如果这个地址是一个智能合约地址，并且该合约包含 `receive()` 或 `fallback()` 函数：

- **没有调用数据**：如果合约包含 `receive()` 函数，将调用该函数。如果没有 `receive()` 函数，将调用 `fallback()` 函数（如果存在）。
- **没有** `receive()` 和 `fallback()`：如果合约不包含这两个函数，矿工仍然可以接收区块奖励，但合约将<u>无法对这些资金进行操作</u>。


ChatGPT

确实，您提到的是两种特殊情况，它们涉及以太坊的接收方式，尤其是在使用 `receive()` 和 `fallback()` 函数的合约中。这些情况包括矿工区块奖励（Coinbase 交易）的接收以及作为 `selfdestruct` 操作的目的地接收以太币。

### 矿工区块奖励（Coinbase 交易）

在创建新区块时，矿工会获得区块奖励，这通常涉及将新创建的以太币发送到矿工指定的地址。如果这个地址是一个智能合约地址，并且该合约包含 `receive()` 或 `fallback()` 函数：

- **没有调用数据**：如果合约包含 `receive()` 函数，将调用该函数。如果没有 `receive()` 函数，将调用 `fallback()` 函数（如果存在）。
- **没有 `receive()` 和 `fallback()`**：如果合约不包含这两个函数，矿工仍然可以接收区块奖励，但合约将无法对这些资金进行操作。

### `selfdestruct` 接收以太币

`selfdestruct` 函数用于销毁合约，并将合约中所有剩余的以太币发送到指定的地址。如果 `selfdestruct` 的目的地是另一个合约地址，这个过程将忽略该合约的 `receive()` 或 `fallback()` 函数，直接将以太币发送到该地址。

- 这意味着即使目标合约没有实现 `receive()` 或 `fallback()` 函数，它仍然可以接收通过 `selfdestruct` 发送的以太币。
- 从 `selfdestruct` 接收以太币是一个无法阻止或拦截的过程，即使目标合约不打算接收以太币

> "selfdestruct" deprecated in Solidity 0.8.18
>
> "selfdestruct" has been deprecated. The underlying opcode will eventually undergo breaking changes, and its use is not recommended.
>
> 当目前为止,只会收到一个编译警告, 但仍然可用