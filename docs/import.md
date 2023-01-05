---
key: import, as, using...for...
desc: 导入
---

## 本地导入

```
.
├── A.sol
└── B.sol
```

```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//导入本地路径下的文件
import "./B.sol";

contract A {}

```



## 远程导入

以openzeppelin`Strings`为例

### 在remix中

```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//方式1
//Remix, GOOD:
import "@openzeppelin/contracts/utils/Strings.sol";

//方式2
//Remix, GOOD:
//import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/utils/Strings.sol";

//方式3
//Remix, GOOD:
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/a28aafdc85a592776544f7978c6b1a462d28ede2/contracts/utils/Strings.sol";

contract A {
    using Strings for uint256;
    function numberToHexString(uint256 _num) public pure returns(string memory)
    {
        return _num.toHexString();
    }
}
```



### 在truffle项目中 (truffle compile)

> 前提: 需要先在项目中先使用 `npm` 安装
>
> 比如 `npm i @openzeppelin/contracts`
> 

```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//方式1
//truffle compile, GOOD:
import "@openzeppelin/contracts/utils/Strings.sol";

//方式2
//truffle compile, GOOD:
//import "../node_modules/@openzeppelin/contracts/utils/Strings.sol";

//方式3
//truffle compile, ERROR:
//import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/utils/Strings.sol";

//方式4
//truffle compile, ERROR:
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/a28aafdc85a592776544f7978c6b1a462d28ede2/contracts/utils/Strings.sol";

contract A {
    using Strings for uint256;

    function numberToHexString(uint256 _num)
        public
        pure
        returns (string memory)
    {
        return _num.toHexString();
    }
}

```



### solc (/usr/local/bin/solc)

`solc` 不能`import`远程的文件

所以可以采取下面这些方式复制到本地:

+ 使用`npm`, 比如 `npm i @openzeppelin/contracts`
+ 使用`git clone` 或下载

然后使用本地导入的方式进行导入, 比如

```solidity
//solc, GOOD:
import "../node_modules/@openzeppelin/contracts/utils/Strings.sol";
```



> 如果代码中就是要使用`import "@openzeppelin/contracts/utils/Strings.sol";` 这种形式, 而你又不想修改代码, 那么可以通过在运行`solc`编译器时添加路径映射的方式进行编译
>
> ```shell
> solc @openzeppelin=`pwd`/node_modules/@openzeppelin/  ./contracts/A.sol 
> ```



```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//方式1
//solc, GOOD:
//但是编译时要加路径指示：
// solc @openzeppelin=`pwd`/node_modules/@openzeppelin/  ./contracts/A.sol --abi --bin
//import "@openzeppelin/contracts/utils/Strings.sol";

//方式2
//solc, GOOD:
import "../node_modules/@openzeppelin/contracts/utils/Strings.sol";

//方式3
//solc, ERROR:
//import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/master/contracts/utils/Strings.sol";

//方式4
//solc, ERROR:
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/a28aafdc85a592776544f7978c6b1a462d28ede2/contracts/utils/Strings.sol";

contract A {
    using Strings for uint256;

    function numberToHexString(uint256 _num)
        public
        pure
        returns (string memory)
    {
        return _num.toHexString();
    }
}


```



#### 方式2, git clone 或下载 到本地

然后本地导入



## 部分导入

```
.
├── A.sol
└── B.sol
```



```solidity
//SPDX-License-Identifier: MIT

//B.sol

pragma solidity ^0.8.7;

contract TheB {}

contract TheAnotherB {}

```



```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//导入本地路径下的文件的一部分
import {TheAnotherB} from "./B.sol";

contract A {
    //ERROR: Identifier not found or not unique.
    //TheB  private b;

    //GOOD:
    TheAnotherB private b;
}

```



## 别名 `as`

```solidity
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

//导入本地路径下的文件的部分并重命名
import {TheAnotherB as B} from "./B.sol";

contract A {
    //ERROR: Identifier not found or not unique.
    //TheB  private b;

    //ERROR: Identifier not found or not unique.
    //TheAnotherB private b;

    //GOOD:
    B private b;
}

```

