# 更新日志 (Changelog)

所有 Starlight 项目的重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划添加
- 字符串插值的完整实现
- 运算符重载的完整实现
- 扩展函数
- 异步/等待语法
- 泛型系统

## [0.3.0-dev] - 2025-01-21

### ⭐ 新增
- **Lambda 表达式**: 支持匿名函数和闭包
  - 单行 Lambda: `(x) => x * 2`
  - 多行 Lambda: `(x, y) => { ... }`
  - 类型推断支持
  - Java 8+ Lambda 代码生成
- **Lambda 解析器**: 在 parser.py 中添加 `Lambda` AST 节点
- **Lambda 代码生成**: JVM 后端生成 Java Lambda 表达式
- **新示例文件**:
  - `examples/lambda_demo.sl` - Lambda 表达式完整示例
  - `examples/string_interpolation.sl` - 字符串插值语法设计
  - `examples/operator_overloading.sl` - 运算符重载语法设计
  - `examples/v03_features.sl` - v0.3.0 所有新特性综合展示
- **新演示程序**: `demo_v03.py` - 展示 v0.3.0 新特性

### 📝 文档
- 添加 `VERSION.md` - 版本历史和规划
- 添加 `CHANGELOG.md` - 本文件
- 更新 `README.md` - 添加 Lambda 表达式文档
- 更新版本号到 v0.3.0-dev

### 🔧 改进
- 优化 Parser 以支持更复杂的表达式
- 改进 JVM 后端的表达式生成逻辑

## [0.2.0-alpha] - 2025-01-21

### ⭐ 新增
- **数据类 (Data Classes)**: 简化数据类定义
  - 自动生成字段和构造函数
  - 支持方法定义
  - 单行方法语法: `fun isAdult(): boolean = age >= 18`
- **模式匹配 (Pattern Matching)**: 强大的模式匹配表达式
  - `match` 表达式支持
  - 字面量模式匹配
  - 通配符模式 `_`
  - 单行和多行匹配体
- **类型推断**: 智能的返回类型推断
  - 自动推断函数返回类型
  - 基于 return 语句的类型推断
  - 算术和字符串操作类型推断
- **单行函数语法**: `fun add(a, b) = a + b`
- **`fun` 关键字**: 作为 `func` 的别名

### 🔧 改进
- 修复函数调用代码生成问题
- 优化 JVM 后端类型转换逻辑
- 改进 JavaScript 后端代码质量
- 完善语法分析器的错误处理

### 📝 文档
- 创建完整的 README.md
- 添加语言规范文档
- 添加开发进度文档
- 整合所有说明文档

### 🧹 清理
- 删除所有测试文件
- 优化项目结构
- 清理零散文件

## [0.1.0-mvp] - 2024-09

### ⭐ 新增
- **词法分析器 (Lexer)**: 完整的 Token 识别
  - 关键字识别
  - 运算符识别
  - 字面量解析
  - 注释处理
- **语法分析器 (Parser)**: 递归下降解析
  - 表达式解析
  - 语句解析
  - AST 构建
- **语义分析器**: 符号表和作用域管理
  - 变量声明检查
  - 类型检查
  - 作用域管理
- **JVM 后端**: Java 代码生成
  - 基本语句生成
  - 表达式生成
  - 函数定义生成
- **JavaScript 后端**: ES6 模块生成
  - 基本语句生成
  - 表达式生成
  - 模块导出
- **基础类型系统**: int, float, string, boolean
- **示例程序**: 7 个示例程序

### 📝 文档
- 初始 README
- 语言设计文档
- 项目总结文档

---

## 版本说明

### 版本号格式
- **主版本号 (Major)**: 不兼容的 API 变更
- **次版本号 (Minor)**: 向下兼容的功能性新增
- **修订号 (Patch)**: 向下兼容的问题修正

### 版本状态
- **dev**: 开发中版本
- **alpha**: 内部测试版本
- **beta**: 公开测试版本
- **rc**: 发布候选版本
- **stable**: 稳定发布版本

### 标签说明
- ⭐ **新增 (Added)**: 新功能
- 🔧 **改进 (Changed)**: 对现有功能的变更
- 🗑️ **弃用 (Deprecated)**: 即将移除的功能
- ❌ **移除 (Removed)**: 已移除的功能
- 🐛 **修复 (Fixed)**: Bug 修复
- 🔒 **安全 (Security)**: 安全性相关变更
- 📝 **文档 (Documentation)**: 文档相关变更
- 🧹 **清理 (Cleanup)**: 代码清理和重构

---

**Starlight** - 让编程更简洁，让世界更连接 ✨

