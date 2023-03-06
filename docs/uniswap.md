---
key: uniswap
desc: 一种用于交换加密货币的分散金融协议
---



## 名词解释

+ Uniswap lab: 开发Uniswap协议的公司，同时也开发了网络界面。
+ Uniswap Protocol: 一套持久的、**不可升级**的智能合约，共同创建了一个自动做市商，该协议促进了以太坊区块链上ERC-20代币的点对点做市和交换。
+ [Uniswap Interface:](https://app.uniswap.org/#/swap) 一个网络界面，允许与Uniswap协议轻松互动。该界面只是人们与Uniswap协议互动的众多方式之一。
+ Uniswap Governance: 用于管理Uniswap协议的治理系统，由UNI代币启用。



## uniswap 协议

https://docs.uniswap.org/concepts/uniswap-protocol

Uniswap协议是一个点对点系统，旨在交换以太坊区块链上的加密货币（ERC-20代币）。该协议被实现为一套持久的、不可升级的智能合约；旨在优先考虑抗审查、安全、自我监护，并在没有任何可信任的中介机构可能选择性地限制访问的情况下运作。



uniswap使用自动做市商（AMM, Auto Market Making），有时被称为恒定功能做市商，来代替订单簿(order book)。

**AMM用两种资产的流动性池取代了订单簿市场上的买卖订单，这两种资产都是相对于对方的价值。当一种资产被交易为另一种资产时，两种资产的相对价格就会发生变化，两种资产的新市场价格就会确定**。在这种动态中，买方或卖方直接与资金池进行交易，而不是与其他各方留下的具体订单进行交易。



### uniswap V1

交易是针对智能合约或流动性池的，一个数学公式决定了资产的价格。流动性提供者向帮助做市的池子增加流动性。

在Uniswap流动性池中，交易资产对的比例应该是恒定的。其数学表达式为

```
X * Y = K

X :第一种资产的储备

Y : 第二中资产的储备
```

流动性提供者应以K的方式增加流动性，使其不发生变化。

![https://miro.medium.com/max/1050/1*CLjUpP1efeDdXeU-dJRBJw.png](https://miro.medium.com/max/1050/1*CLjUpP1efeDdXeU-dJRBJw.png)

Uniswap v1只支持ETH-ERC 20对的互换。如果用户希望将USDC换成DAI，第一步是将USDC换成ETH，然后兑换ETH-DAI，得到DAI。Uniswap v1还促进了LP代币的概念。当流动性提供者（LPs）向任何池子增加流动性时，他们会收到代表增加的流动性的LP代币。然后，这些LP代币可以被押注或燃烧，以赎回奖励。为了奖励流动性提供者，会产生0.3%的交易费。



### uniswap V2

Uniswap v1的主要缺点是 "ETH桥接 "问题，即缺乏ERC20-ERC20代币池。这导致了当用户想要交换一个ERC20代币时，成本上升和高滑点(high slippage)

Uniswap v2在用户界面和体验上比v1好得多。同时，它通过引入ERC20-ERC20池的概念，消除了ETH桥接的问题。另一个重要的区别是在核心合约中使用wrapped ETH，而不是原生ETH。然而，交易者可以通过辅助合约使用ETH。

![https://miro.medium.com/max/1050/1*HeCiFcK_4LjKmK14Iy37BQ.png](https://miro.medium.com/max/1050/1*HeCiFcK_4LjKmK14Iy37BQ.png)

Uniswap v2的闪电互换(`FlashSwap`)概念允许用户提取任何数量的ERC20代币，而不需要预先付款。但他们可以为提取的代币付款，或支付一部分并归还其余部分，或归还所有提取的代币。这些事情可以在交易执行结束时进行。

Uniswap v2还引入了协议费。社区治理在开启/关闭这项费用方面起着至关重要的作用。0.3%的交易费中的0.05%的协议费将被保留给塑造网络路线图的Uniswap平台的发展。



### uniswarp V3

Uniswap v3旨在超越基于稳定币的AMM和集中式交易所，提供更好的资本效率和准确性，更灵活的收费结构，以及流动性提供者根据自己的喜好建立独特的价格曲线的能力。Uniswap v3还允许LPs在自定义的价格范围内集中他们的资本，增强所需价格的流动性，并在市场超出LP指定的价格范围时自动从池中移除流动性。Uniswap v3的收费结构是由社区管理的，包括三个不同的收费等级。