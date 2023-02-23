---
key: error
desc: 自定义错误
---



https://blog.soliditylang.org/2021/04/21/custom-errors/





```solidity
//定义
// 格式 error ERROR_NAME(ARG1, ARG2, ... )
error InsufficientBalance(uint256 balance, uint256 withdrawAmount);

//抛出错误
function domething() public {
	//...
	if(xxx){
	 revert InsufficientBalance(1,2);
	}
	//..
}

```



> 在remix和hardhat中运行时, 环境会自动解析抛出的错误信息
>
> 比如
>
> ```
> revert
> 	The transaction has been reverted to the initial state.
> Error provided by the contract:
> InsufficientBalance
> Parameters:
> {
>  "balance": {
>   "value": "0"
>  },
>  "withdrawAmount": {
>   "value": "100"
>  }
> }
> ```
>
> 



使用`try...catch` 捕获error

```solidity
try myContract.domething(){

}
catch (bytes memory err){
	if (keccak256(abi.encodeWithSignature("InsufficientBalance(uint256,uint256)")) == keccak256(err)) {
             
   }
}
```

