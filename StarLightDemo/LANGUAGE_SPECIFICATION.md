# Starlight 语言规范 v1.0

## 🎯 核心目标

**Starlight** 是一款现代编程语言，设计目标是：

1. **完美兼容 Java/Kotlin**：源码级双向兼容
2. **前后端通用**：一份源码编译到多个平台
3. **简洁高效**：比 Java 少 30% 字符，比 Kotlin 更逻辑化
4. **逻辑化编程**：支持声明式规则和推导式

## 📋 兼容级别定义

### Java 兼容性
- ✅ 直接使用 Java 类：`new ArrayList<String>()`
- ✅ 零桥接层：`import java.time.*`
- ✅ 完全兼容 Java 生态系统
- ✅ 支持所有 Java 注解和反射

### Kotlin 兼容性
- ✅ 支持 Kotlin 语法糖：`data class`、`when`、`?.`
- ✅ 空安全类型系统
- ✅ 扩展函数语法
- ✅ 协程支持

## 🎨 语法风格定义

### 核心原则
1. **静态类型 + 类型推断**
2. **分号可选，大括号保留**
3. **后置类型注解**：`name: String`
4. **逻辑化声明式扩展**

### 语法对比表

| 特性 | Java | Kotlin | Starlight |
|------|------|--------|-----------|
| 数据类 | `record` | `data class` | `data User(name: String, age: Int)` |
| 空安全 | Optional | `String?` | `String?` + 自动抬升 |
| 扩展函数 | 无 | `fun String.foo(){}` | `extend String { fun foo(){} }` |
| 主函数 | `public static void main` | 无 | `fun main()` |
| 字符串模板 | `+` | `"$name"` | `"Hello \(name)"` |
| 模式匹配 | 无 | `when` | `match` + 守卫条件 |

## 🏗️ 运行目标

### 编译目标
1. **JVM 字节码**：Java 17+ 兼容
2. **JavaScript**：ES6+ 模块
3. **WebAssembly**：基于 LLVM
4. **Native**：机器码（未来）

### 前后端通用策略
- **服务端**：编译到 JVM，直接使用 Java 生态
- **前端**：编译到 JS/WASM，封装 DOM API
- **跨平台**：`expect/actual` 机制

## 🔧 技术架构

### 编译器架构
```
源代码 → 词法分析 → 语法分析 → 语义分析 → 中间表示 → 代码生成
   ↓         ↓         ↓         ↓         ↓         ↓
  .sl     Tokens    AST     Symbol     IR      Target
```

### 后端策略
1. **基于 Kotlin 编译器前端**：复用 K2 编译器
2. **自定义 IR**：Starlight IR → 目标代码
3. **注解处理器**：支持 kapt，Spring 直接可用

## 📚 标准库设计

### 核心库
- 基本类型、字符串、集合
- 并发、IO、网络
- 日期时间、数学

### 平台特定库
- **JVM**：复用 Java 标准库
- **Web**：封装 DOM/Fetch/WebWorker
- **跨平台**：`expect/actual` 声明

## 🎯 差异化特性

### 逻辑化编程扩展
1. **规则块**：`rule adult(User.age >= 18) => User.canVote = true`
2. **推导式**：`val names = for (u in users if u.age >= 18) yield u.name`
3. **自动事务**：`transaction { account1 -= 100; account2 += 100 }`

### 类型系统扩展
1. **联合类型**：`String | Int`
2. **交集类型**：`String & Serializable`
3. **类型别名**：`type UserId = String`

## 📊 性能承诺

| 平台 | 性能指标 |
|------|----------|
| JVM | 生成的 `.class` 与手写 Java 1:1 |
| JS | HelloWorld ≤ 8 KB（gzip） |
| WASM | 基于 LLVM，无 GC 依赖 |

## 🔄 版本管理

### 语法版本化
```starlight
@version("1.3")
package com.example

// 新语法特性
```

### 兼容性策略
- 向后兼容：旧代码无需修改
- 渐进式升级：新特性可选启用
- 自动化测试：每天跑官方测试集

## 📋 实施路线图

### Phase 1: 基础完善 (已完成)
- ✅ 编译器框架
- ✅ JVM/JS 后端
- ✅ 基本语法

### Phase 2: 语法标准化 (进行中)
- 🔄 EBNF 语法规范
- 🔄 兼容层设计
- 🔄 语法糖实现

### Phase 3: 高级特性 (计划中)
- ⏳ 逻辑化扩展
- ⏳ 类型系统扩展
- ⏳ 编译管线优化

### Phase 4: 工具链 (计划中)
- ⏳ LSP 服务器
- ⏳ Gradle 插件
- ⏳ IDE 支持

---

**Starlight** - 让 Java 和 JavaScript 世界无缝连接 ✨

*版本: 1.0*  
*更新日期: 2024年1月*
