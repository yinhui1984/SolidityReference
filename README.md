# SolidityReference
 Solidity参考文档

鉴于Solidity官方文档有些混乱, 翻阅和搜索起来很费劲, 这里将实践中遇到的知识点整理成md文档, 并提供一个命令行程序进行搜索

## 用法

```shell
~/Doc/github/SolidityReference ❯ ./solref.py
usage: solref.py [-h] [-l] [keyword]

Search and open solidity reference docs.

positional arguments:
  keyword     keyword to search

options:
  -h, --help  show this help message and exit
  -l, --list  list all keywords
```



比如, 搜索关键字`abi`

```
~/Doc/github/SolidityReference ❯ ./solref.py abi
Found multiple matches:

0: abi.encodePacked               ABI紧打包编码函数
1: abi.encode                     ABI编码函数
2: abi.encodeCall                 将函数调用进行ABI编码
3: abi.encodeWithSignature        函数签名和参数编码
4: abi.decode                     使用提供的类型对ABI编码的数据进行解码
5: abi.encodeWithSelector         函数选择器和参数编码

Please select one:

```



## 新建文档

在`./docs`目录下添加xxx.md

在md头部添加 YAML front matter

YAML front matter 是 Markdown 文件的一种特殊格式，它可以在 Markdown 文件的开头添加一些额外的元数据，例如文章的标题、作者、日期等。

```
---
key: 关键字
desc: 描述文本
---
```

