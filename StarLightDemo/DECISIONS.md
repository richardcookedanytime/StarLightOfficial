# Starlight 关键决策文档

本文档记录 Starlight 编程语言项目的关键设计决策，包括决策背景、选项分析和最终选择。

## 🎯 核心决策

### 1. 宏/注解处理器 ✅ **引入**

**决策**: 引入宏系统和注解处理器

**背景**: 现代编程语言需要元编程能力来简化代码生成、减少样板代码、提供编译时检查。

**选项分析**:
- **选项 A**: 不引入宏系统
  - ✅ 简单实现
  - ❌ 缺少元编程能力
  - ❌ 需要大量样板代码
  - ❌ 无法提供编译时优化

- **选项 B**: 引入简单注解处理器
  - ✅ 与 Java 生态系统兼容
  - ✅ 实现相对简单
  - ❌ 功能有限

- **选项 C**: 引入完整宏系统 + 注解处理器
  - ✅ 强大的元编程能力
  - ✅ 灵活的代码生成
  - ✅ 编译时计算和优化
  - ✅ 与 Java 注解系统兼容
  - ❌ 实现复杂度高

**最终选择**: **选项 C** - 完整宏系统 + 注解处理器

**理由**:
1. **生态兼容**: 与 Java 注解系统无缝集成
2. **开发效率**: 大幅减少样板代码
3. **性能优化**: 编译时计算和代码生成
4. **扩展性**: 支持第三方库和框架集成

**实现计划**:
```sl
// 编译时注解
@Generated
@ToString
class User {
    val name: String
    val age: Int
}

// 宏系统
macro def debug(expr: Expr): Unit = {
    println(s"${expr} = ${expr.eval()}")
}

// 使用
debug(x + y) // 编译时展开为: println("x + y = " + (x + y))
```

### 2. JS 端 Tree-shaker ✅ **选择 Rollup**

**决策**: 使用 Rollup 作为 JavaScript 后端的 Tree-shaking 工具

**背景**: JavaScript 模块打包和 Tree-shaking 对减少包体积至关重要。

**选项分析**:
- **选项 A**: 自研 Tree-shaker
  - ✅ 完全控制实现
  - ✅ 针对 Starlight 优化
  - ❌ 开发周期长
  - ❌ 维护成本高
  - ❌ 功能可能不如成熟工具

- **选项 B**: 使用 Webpack
  - ✅ 功能强大
  - ✅ 生态系统丰富
  - ❌ 配置复杂
  - ❌ 包体积较大
  - ❌ 主要面向应用而非库

- **选项 C**: 使用 Rollup
  - ✅ 专为库设计
  - ✅ 强大的 Tree-shaking
  - ✅ 配置简单
  - ✅ 输出格式多样
  - ✅ 插件生态成熟
  - ❌ 功能相对简单

**最终选择**: **选项 C** - Rollup

**理由**:
1. **专业定位**: Rollup 专为库和模块设计，符合 Starlight 定位
2. **Tree-shaking**: 业界领先的 Tree-shaking 能力
3. **轻量级**: 配置简单，输出高效
4. **生态成熟**: 丰富的插件生态
5. **快速集成**: 减少开发时间，加速 MVP 发布

**实现方案**:
```javascript
// rollup.config.js
export default {
  input: 'build/starlight.js',
  output: {
    file: 'dist/starlight.min.js',
    format: 'esm',
    name: 'Starlight'
  },
  plugins: [
    resolve(),
    commonjs(),
    terser()
  ],
  external: ['java.*'] // 排除 Java 互操作代码
}
```

### 3. Native 平台支持 ✅ **优先支持 wasm32-wasi**

**决策**: 优先支持 wasm32-wasi，后续支持其他原生平台

**背景**: WebAssembly 正成为跨平台应用的标准，需要确定优先级。

**选项分析**:
- **选项 A**: 优先支持 x86_64-linux
  - ✅ 服务器部署主流平台
  - ✅ LLVM 支持成熟
  - ❌ 平台局限性大
  - ❌ 无法在浏览器运行

- **选项 B**: 优先支持 aarch64-apple-darwin
  - ✅ 苹果生态重要
  - ✅ ARM 架构趋势
  - ❌ 平台过于特定
  - ❌ 开发工具链复杂

- **选项 C**: 优先支持 wasm32-wasi
  - ✅ 跨平台兼容性最强
  - ✅ 浏览器和服务器通用
  - ✅ 安全性高（沙盒环境）
  - ✅ 生态系统快速发展
  - ✅ 性能优秀
  - ✅ 部署简单
  - ❌ 功能可能受限

**最终选择**: **选项 C** - wasm32-wasi 优先

**理由**:
1. **最大兼容性**: 一次编译，到处运行
2. **现代趋势**: WebAssembly 是未来标准
3. **安全性**: 沙盒环境提供更好的安全性
4. **性能**: 接近原生性能
5. **生态**: 快速发展，工具链完善
6. **部署**: 简单的部署模型

**实现优先级**:
1. **wasm32-wasi** (最高优先级 - 2024 Q1)
2. **x86_64-linux** (2024 Q2)
3. **aarch64-apple-darwin** (2024 Q3)
4. **x86_64-pc-windows-msvc** (2024 Q4)

## 🔧 技术决策

### 4. 编译器架构 ✅ **多阶段编译**

**决策**: 采用多阶段编译器架构

**架构设计**:
```
Source Code (.sl)
    ↓
Lexer (Token Stream)
    ↓
Parser (AST)
    ↓
Semantic Analyzer (Type-checked AST)
    ↓
IR Generator (Intermediate Representation)
    ↓
Backend Generators
    ├── JVM Backend → .class files
    ├── JS Backend → .js files (via Rollup)
    ├── WASM Backend → .wasm files (via LLVM)
    └── Native Backend → binary files (via LLVM)
```

**理由**:
- **模块化**: 每个阶段职责清晰
- **可扩展**: 易于添加新的后端
- **可维护**: 问题定位容易
- **可测试**: 每个阶段可独立测试

### 5. 类型系统 ✅ **静态类型 + 类型推断**

**决策**: 静态类型系统，支持类型推断

**特性**:
- **类型注解**: `val name: String = "Hello"`
- **类型推断**: `val name = "Hello"` (推断为 String)
- **泛型**: `List<String>`, `Map<String, Int>`
- **联合类型**: `Result<T> = Success(T) | Error(String)`
- **可选类型**: `String?` (可为 null)

**理由**:
- **安全性**: 编译时错误检测
- **性能**: 运行时类型检查开销小
- **工具支持**: IDE 更好的代码补全
- **Java 兼容**: 与 Java 类型系统兼容

### 6. 内存管理 ✅ **自动内存管理 + 可选手动控制**

**决策**: 默认自动内存管理，提供手动控制选项

**方案**:
- **JVM 后端**: 依赖 JVM GC
- **JS 后端**: 依赖 JavaScript GC
- **WASM 后端**: 可选无 GC 模式
- **Native 后端**: 可选引用计数或手动管理

**理由**:
- **易用性**: 降低学习门槛
- **性能**: 关键路径可手动优化
- **兼容性**: 适应不同平台特性
- **灵活性**: 开发者可选择合适方案

## 📊 性能目标

### 编译性能
- **词法分析**: 10,000 行/秒
- **语法分析**: 5,000 行/秒
- **语义分析**: 2,000 行/秒
- **代码生成**: 1,000 行/秒

### 运行时性能
- **JVM**: 与手写 Java 性能相当
- **JS**: 与手写 JavaScript 性能相当
- **WASM**: 接近原生性能 (80-90%)

### 包体积
- **JS 基础运行时**: ≤ 8KB (gzip)
- **WASM 基础运行时**: ≤ 50KB
- **完整标准库**: ≤ 200KB

## 🎯 成功指标

### 技术指标
- [ ] 编译器通过所有测试用例
- [ ] 生成的代码性能达标
- [ ] 包体积符合预期
- [ ] 内存使用在合理范围

### 生态指标
- [ ] GitHub Stars: 1,000+ (6 个月内)
- [ ] 社区贡献者: 50+ (1 年内)
- [ ] 第三方库: 100+ (1 年内)
- [ ] 企业采用: 10+ (1 年内)

### 用户体验指标
- [ ] 安装时间: ≤ 30 秒
- [ ] 编译时间: ≤ 10 秒 (10K 行代码)
- [ ] 学习曲线: ≤ 2 小时 (Java 开发者)
- [ ] 文档覆盖率: ≥ 90%

## 🔄 决策回顾

本文档将定期更新，记录新的决策和现有决策的变更。每个决策都应该：

1. **明确问题**: 清楚描述要解决的问题
2. **分析选项**: 列出所有可能的解决方案
3. **权衡利弊**: 客观分析每个选项的优缺点
4. **记录选择**: 说明最终选择和理由
5. **跟踪结果**: 定期评估决策效果

---

**最后更新**: 2024-01-XX  
**决策记录**: [GitHub Issues](https://github.com/starlight-lang/starlight/issues?q=is%3Aissue+label%3Adecision)
