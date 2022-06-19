# ChocoPy PA1

Compile the python 3.6 front-end code to AST tree. [Start from using docker](./doc/common/build.md) and see the [doc](./doc/PA1/README.md).

# writeup

#### 词法分析

Python 是缩进敏感的语言，所以需要特别注意空白字符的处理。

在 flex 中，我使用了默认环境和 `<code>` 环境，来让词法生成器有“状态”，较好地处理了缩进。

由于字符串常量的规则比较简单，直接使用正则 `(\"([ -!#-\[\]-~]|(\\(n|t|\\|\")))*\")` 匹配即可。

#### 语法分析

主要问题在于如何排查 shift-reduce confict。

可以通过重写表达式，标定优先级和结合律解决。

考虑到 Python if expr 比较特殊，我重写了一些表达式文法保证优先级正确。
