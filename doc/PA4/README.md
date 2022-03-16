# Programing Assignment IV 文档

<!-- TOC -->

- [Lab2 实验文档](#lab4-实验文档)
    - [0. 基础知识](#0-基础知识)
        - [0.1 标准库定义](#01-标准库定义)
        - [0.2 RISCV基本语法](#02-RISCV基本语法)
        - [0.3 后端介绍](#03-后端介绍)

        - [1. 实验要求](#1-实验要求)
            - [1.1 目录结构](#11-目录结构)
            - [1.2 编译、运行和验证](#12-编译运行和验证)
            - [1.3 提交要求和评分标准](#13-提交要求和评分标准)

<!-- /TOC -->

在 CodeGen 中，我们需要从 Light IR 生成后端代码，LLVM IR 仅需要简单的转换指令、函数调用指定和寄存器分配就可以了。这也是为什么LLVM IR这么风靡的原因，很简单的对任意体系结构的代码生成。LLVM自己的实现可以参考[源码这里](llvm/include/llvm/IR/IntrinsicsRISCV.td).

## 标准库定义

为了使

### 1.1 目录结构

### 1.1 目录结构

详见[common/structure.md](./doc/common/structure.md)
### 1.2 主要工作

1. 阅读[LightIR 核心类介绍](../common/LightIR.md)
2. 阅读[实验框架](#1-实验框架)，理解如何使用框架以及注意事项
3. 修改 [chocopy_lightir.cpp](../../src/ir-optimizer/chocopy_lightir.cpp) 来实现自动 IR 产生的算法，使得它能正确编译任何合法的 ChocoPy 程序
4. 在 `report.md` 中解释你们的设计，遇到的困难和解决方案
5. 由**队长**在 `contribution.md` 中解释每位队员的贡献，并说明贡献比例

#### 1.2.1  几点说明
由于 LLVM IR 是强类型的
有很多部分和伯克利生成的代码不太一样
1. char* 还是 .string
2. activation record 不使用 frame pointer 回滚 function local 变量。
3. 

### 1.3 Bonus

1. 完成基本Pass[2 * 5pts]
2. 完成优化Pass[10 * 5pts]

### 1.4 编译、运行和验证

* 编译

  若编译成功，则将在 `./[build_dir]/` 下生成 `ir-optimizer` 命令。

* 运行

  本次实验的 `ir-optimizer` 命令使用命令行参数来完成编译和运行。

  ```shell
  $ cd chocopy
  $ ./build/ir-optimizer test.py -run # 直接用clang编译器编译到elf给qemu执行。
  $ ./build/ir-optimizer test.py -emit # 输出。
  $ ./build/ir-optimizer test.py -assem # 输出汇编。
  $ ./build/ir-optimizer test.py -pass [PassName] # 运行pass。
  <以上的选项可以同时使用>
  ```

  通过灵活使用重定向，可以比较方便地完成各种各样的需求，请同学们务必掌握这个 shell 功能。

* 验证

  本次试验测试案例较多，为此我们将这些测试分为两类：

    1. sample: 这部分测试均比较简单且单纯，适合开发时调试。
    2. fuzz: 由fuzzer生成的正确的python文件，此项不予开源。
    3. student: 这部分由同学提供。

  我们使用python中的 `json.load()` 命令进行验证。将自己的生成结果和助教提供的 `xxx.typed.ast` 进行比较。

  ```shell
  $ python3 ./duipai.py --pa 3
  # 如果结果完全正确，则全 PASS，且有分数提示，一个正确的case 1 pts，此项评分按比例算入总评。选择chocopy的同学会在project部分分数上*1.2计入总评。
  # 如果有不一致，则会汇报具体哪个文件哪部分不一致，且有详细输出。
  ```

  **请注意助教提供的`testcase`并不能涵盖全部的测试情况，完成此部分仅能拿到基础分，请自行设计自己的`testcase`进行测试。**
  