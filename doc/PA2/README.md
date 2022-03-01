# Programing Assignment II 文档

<!-- TOC -->

- [Lab2 实验文档](#lab2-实验文档)
    - [0. 基础知识](#0-基础知识)
        - [0.1 类型语义](#01-类型语义)
        - [0.2 函数语义](#02-函数语义)
        - [0.3 类语义](#03-类语义)

        - [1. 实验要求](#1-实验要求)
            - [1.1 目录结构](#11-目录结构)
            - [1.2 编译、运行和验证](#12-编译运行和验证)
            - [1.3 提交要求和评分标准](#13-提交要求和评分标准)

<!-- /TOC -->

在本次实验中需要使用`Visitor Pattern`完成对程序的 Declaration Analysis 和 Type Checker Analysis。 Declaration的结果以 Symbol table 的形式传给Type
Checker继续检查。从而使`Chocopy`的LSP没有语义错误。

## 0. 基础知识

Declaration 检查众所周知是一个依赖环境的检查，在python中的变量有四个作用域

| 作用域            | 英文解释                      | 英文简写 |
|----------------|---------------------------|------|
| 局部作用域（函数内）     | Local(function)           | L    |
| 外部嵌套函数作用域      | Enclosing function locals | E    |
| 函数定义所在模块作用域    | Global(module)            | G    |
| python内置模块的作用域 | Builtin                   | B    |

在访问变量时，先查找本地变量，然后是包裹此函数外部的函数内的变量，之后是全局变量 最后是內建作用域内的变量 即： L –> E -> G -> B

Python 支持嵌套定义函数，每次进入函数时需要进入函数本地变量的scope，同时对外部的E/G/B所在定义aware，不能重名，如有调用需要指向外部的symbol

Type Checker 检查

### 0.1 类型语义

对类型语义，最先需要做的是symbol table的建立，在有nested函数及nonlocal、global变量的语言当中尤为重要。在nested 函数调用中

## 1. 实验要求

### 1.1 目录结构

#### Declaration 类定义
