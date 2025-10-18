# 贡献指南

欢迎为 Starlight 编程语言项目做出贡献！本指南将帮助你了解如何参与项目开发。

## 🚀 快速开始

### 1. Fork 和 Clone
```bash
# Fork 本项目到你的 GitHub 账户
# 然后克隆你的 fork
git clone https://github.com/你的用户名/starlight.git
cd starlight
```

### 2. 设置开发环境
```bash
# 安装 Python 3.8+ (用于编译器原型)
python3 --version

# 安装 Rust (用于最终编译器实现)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 Node.js (用于 JS 后端测试)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
```

### 3. 运行测试
```bash
# 测试编译器原型
python3 compiler/lexer.py
python3 compiler/parser.py
python3 compiler/main.py examples/hello_world.sl --tokens
python3 compiler/main.py examples/hello_world.sl --ast
```

## 📋 开发流程

### 1. 创建分支
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 编写代码
- 遵循项目的代码风格
- 添加适当的注释和文档
- 确保代码可读性和可维护性

### 3. 测试你的更改
```bash
# 运行所有测试
python3 -m pytest tests/

# 测试特定功能
python3 compiler/main.py examples/your_test.sl --ast
```

### 4. 提交更改
```bash
git add .
git commit -m "feat: 添加新功能描述"
# 或
git commit -m "fix: 修复问题描述"
```

### 5. 推送并创建 Pull Request
```bash
git push origin feature/your-feature-name
```

## 🎯 贡献领域

### 编译器开发
- **词法分析器**: 扩展 Token 类型，支持更多语法特性
- **语法分析器**: 完善 AST 节点，支持复杂语法结构
- **语义分析**: 类型检查、作用域分析
- **代码生成**: JVM、JavaScript、WebAssembly 后端

### 标准库
- **基础类型**: String、Array、Map、Set
- **I/O 操作**: 文件读写、网络请求
- **日期时间**: 跨平台时间处理
- **数学库**: 基础数学运算

### 工具链
- **VS Code 插件**: 语法高亮、代码补全、错误诊断
- **命令行工具**: 编译、构建、测试
- **包管理器**: 依赖管理、版本控制

### 文档和教程
- **语言规范**: 语法定义、语义说明
- **教程**: 从入门到高级的使用指南
- **示例**: 各种应用场景的代码示例
- **最佳实践**: 性能优化、代码组织

## 📝 代码规范

### Python 代码 (编译器原型)
```python
# 使用类型注解
def parse_expression(self) -> Optional[Expression]:
    """函数文档字符串"""
    # 清晰的变量命名
    current_token = self.tokens[self.position]
    
    # 适当的错误处理
    if not current_token:
        raise SyntaxError("Unexpected end of input")
```

### Starlight 代码
```sl
// 使用清晰的函数命名
func calculateTotal(items: [Item]) -> Decimal {
    // 类型注解
    let total: Decimal = 0.0
    
    // 函数式编程风格
    return items.reduce(total, (acc, item) => acc + item.price)
}
```

### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
feat: 添加新的语言特性
fix: 修复编译器错误
docs: 更新文档
style: 代码格式调整
refactor: 重构代码结构
test: 添加测试用例
chore: 构建工具更新
```

## 🧪 测试指南

### 单元测试
```python
import unittest
from compiler.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        lexer = Lexer('func hello() {}')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.FUNC)
```

### 集成测试
```bash
# 测试完整编译流程
python3 compiler/main.py examples/hello_world.sl --target=jvm
python3 compiler/main.py examples/hello_world.sl --target=js
```

### 性能测试
```python
import time

def benchmark_lexer():
    source = load_large_source_file()
    
    start_time = time.time()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    end_time = time.time()
    
    print(f"Lexed {len(source)} characters in {end_time - start_time:.3f}s")
```

## 🐛 报告问题

### Bug 报告模板
```markdown
**Bug 描述**
简洁描述遇到的问题

**重现步骤**
1. 创建文件 `test.sl`
2. 运行命令 `jstarc test.sl --target=js`
3. 观察错误输出

**预期行为**
描述期望的正确行为

**实际行为**
描述实际发生的错误

**环境信息**
- 操作系统: macOS 13.0
- Python 版本: 3.9.7
- 编译器版本: 0.1.0

**附加信息**
任何其他相关信息
```

### 功能请求模板
```markdown
**功能描述**
详细描述希望添加的功能

**使用场景**
解释为什么需要这个功能

**实现建议**
如果有实现想法，请提供

**替代方案**
考虑过的其他解决方案
```

## 💬 社区交流

### 讨论渠道
- **GitHub Discussions**: 功能讨论、设计决策
- **Discord**: 实时交流、快速问答
- **邮件列表**: 正式讨论、公告

### 行为准则
我们承诺为每个人提供友好、安全、包容的环境：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员保持同理心

## 🏆 贡献者认可

### 贡献者类型
- **代码贡献**: 实现功能、修复 Bug
- **文档贡献**: 编写教程、更新规范
- **测试贡献**: 编写测试、报告问题
- **社区贡献**: 回答问题、推广项目

### 认可方式
- 在 README 中列出贡献者
- 在发布说明中提及重要贡献
- 授予 GitHub 贡献者徽章
- 邀请参与项目决策

## 📚 学习资源

### 编译器开发
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [LLVM Tutorial](https://llvm.org/docs/tutorial/)
- [Modern Compiler Implementation in ML](https://www.cs.princeton.edu/~appel/modern/)

### 编程语言设计
- [Programming Language Pragmatics](https://www.cs.rochester.edu/~scott/pragmatics/)
- [Types and Programming Languages](https://www.cis.upenn.edu/~bcpierce/tapl/)

### 相关项目
- [Kotlin](https://github.com/JetBrains/kotlin)
- [TypeScript](https://github.com/Microsoft/TypeScript)
- [Rust](https://github.com/rust-lang/rust)

## 📞 联系方式

- **项目维护者**: team@starlight.io
- **技术问题**: tech@starlight.io
- **社区管理**: community@starlight.io

感谢你的贡献！让我们一起打造更好的 Starlight 编程语言！ ✨
