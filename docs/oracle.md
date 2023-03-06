---
key: oracle
desc: 预言机
---

官方教程 https://ethereum.org/zh/developers/docs/oracles/





### 安全性

https://ethereum.org/zh/developers/docs/oracles/#security

预言机的安全性等同于其数据源。 如果一个去中心化应用程序使用 Uniswap 作为其以太币/DAI 价格的预言机，攻击者就可以在 Uniswap 上篡改价格，以操纵该去中心化应用程序对当前价格的理解。 如何对付这个隐患的示例包括[一种推送系统](https://developer.makerdao.com/feeds/)，如 MakerDAO 所使用的推送系统。它会将来自若干外部数据源的价格数据进行比对，而不是仅仅依靠单一来源。

## 预言机服务

- [Chainlink](https://chain.link/)
- [Witnet](https://witnet.io/)
- [Provable](https://provable.xyz/)
- [Paralink](https://paralink.network/)
- [Dos.Network](https://dos.network/)

## 示例

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";

//更正式的，你应该安装smartcontractkit来使用这个接口
//forge install smartcontractkit/chainlink-brownie-contracts --no-commit
//forge remappings > remappings.txt
interface AggregatorV3Interface {
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

contract ChainlinkPriceOracle {
    AggregatorV3Interface internal priceFeed;

    constructor() {
        // ETH / USD
        priceFeed = AggregatorV3Interface(
            0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
        );
    }

    function getLatestPrice() public view returns (int256) {
        (
            uint80 roundID,
            int256 price,
            uint256 startedAt,
            uint256 timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        // for ETH / USD price is scaled up by 10 ** 8
        return price / 1e8;
    }
}

contract ChainlinkPriceOracleTest is Test {
    ChainlinkPriceOracle cpo;

    function setUp() public {
        vm.createSelectFork("https://rpc.ankr.com/eth");
        cpo = new ChainlinkPriceOracle();
    }

    function testGetPrice() public {
        int256 price = cpo.getLatestPrice();
        assertGe(price, 0);
        console2.log(price);
    }
}


```



## 创建一个简单的预言机的示例

https://medium.com/@pedrodc/implementing-a-blockchain-oracle-on-ethereum-cedc7e26b49e



更多的

https://www.paradigm.xyz/2020/11/so-you-want-to-use-a-price-oracle

