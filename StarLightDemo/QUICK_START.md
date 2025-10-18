# Starlight 快速开始指南

## 🚀 30 秒上手

### 1. 运行演示
```bash
# 运行完整演示
python3 working_demo.py

# 测试基础功能
python3 test_basic_only.py
```

### 2. 查看结果
```bash
# 查看生成的文件
ls build/

# 编译 Java 文件
javac build/*.java

# 运行 Java 程序
java -cp build HelloWorld
```

### 3. 打开 Web 页面
```bash
# 在浏览器中打开
open build/index.html
```

## 📝 编写 Starlight 代码

### 基本语法
```starlight
// 函数定义
fun greet(name) {
    return "Hello, " + name;
}

// 变量声明
let message = greet("World");
println(message);

// 主函数
fun main() {
    let x = 42;
    let result = add(x, 10);
    println(result);
}

// 数学运算
fun add(a, b) {
    return a + b;
}
```

### 高级特性
```starlight
// 数据类
data User(name: string, age: int) {
    fun isAdult(): boolean = age >= 18
}

// 规则系统
rule adult(User.age >= 18) => User.canVote = true

// 扩展函数
extend String {
    fun isEmail(): boolean = this.contains("@")
}

// 列表推导式
val names = [user.name | for user in users if user.isAdult()]
```

## 🛠️ 编译选项

### 命令行使用
```bash
# 编译到 Java
python3 compiler/main.py your_file.sl --target jvm

# 编译到 JavaScript
python3 compiler/main.py your_file.sl --target js

# 查看 AST
python3 compiler/main.py your_file.sl --ast

# 查看 Tokens
python3 compiler/main.py your_file.sl --tokens
```

### 程序化使用
```python
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.jvm_backend import JVMCodeGenerator

# 读取源代码
with open("your_file.sl", "r") as f:
    source = f.read()

# 词法分析
lexer = Lexer(source)
tokens = lexer.tokenize()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 代码生成
jvm_generator = JVMCodeGenerator()
java_code = jvm_generator.generate(ast, "YourClass")

# 保存结果
with open("YourClass.java", "w") as f:
    f.write(java_code)
```

## 📚 示例代码

### Hello World
```starlight
fun main() {
    println("Hello, Starlight!");
}
```

### 计算器
```starlight
fun add(a, b) {
    return a + b;
}

fun multiply(a, b) {
    return a * b;
}

fun main() {
    let x = 10;
    let y = 5;
    
    let sum = add(x, y);
    let product = multiply(x, y);
    
    println("Sum: " + sum);
    println("Product: " + product);
}
```

### Web 应用
```starlight
fun createButton() {
    let button = document.createElement("button");
    button.textContent = "Click Me!";
    return button;
}

fun handleClick() {
    console.log("Button clicked!");
    alert("Hello from Starlight!");
}

fun main() {
    let button = createButton();
    button.addEventListener("click", handleClick);
    document.body.appendChild(button);
}
```

## 🔧 故障排除

### 常见问题

1. **导入错误**
   ```bash
   # 确保在项目根目录运行
   cd /path/to/starlight
   python3 working_demo.py
   ```

2. **语法错误**
   ```starlight
   // 确保分号结尾
   let x = 42;
   
   // 确保大括号匹配
   fun test() {
       return "hello";
   }
   ```

3. **编译错误**
   ```bash
   # 检查 Python 版本
   python3 --version  # 需要 3.8+
   
   # 检查依赖
   pip install -r requirements.txt
   ```

## 📖 更多资源

- **项目文档**: [README.md](README.md)
- **语言规范**: [LANGUAGE_SPECIFICATION.md](LANGUAGE_SPECIFICATION.md)
- **语法规范**: [GRAMMAR_EBNF.md](GRAMMAR_EBNF.md)
- **实施路线图**: [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
- **项目总结**: [FINAL_SUMMARY.md](FINAL_SUMMARY.md)

## 🎯 下一步

1. **学习语法**: 查看示例代码
2. **编写程序**: 创建你的第一个 Starlight 程序
3. **贡献代码**: Fork 项目并提交 PR
4. **加入社区**: 参与讨论和开发

---

**Starlight** - 让编程更简洁，让世界更连接 ✨

*快速开始指南 v1.0*
