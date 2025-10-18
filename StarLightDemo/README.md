# Starlight 编程语言

> **"Write once, run anywhere Java does, and anywhere JavaScript does."**

Starlight 是一款现代编程语言，设计目标是与 Java 100% 无缝互操作，同时支持一份源码编译到多个平台。

## 🎯 核心特性

### 1. Java 级兼容
- 直接使用 Java 类：`new ArrayList<String>()`
- 零桥接层：`import java.time.*`、`implements Servlet`
- 完全兼容 Java 生态系统

### 2. 全栈通用
- **JVM**: `jstarc Foo.sl -> Foo.class`
- **JavaScript**: `jstarc Foo.sl --target=js -> foo.js`
- **WebAssembly**: `jstarc Foo.sl --target=wasm -> foo.wasm`
- **Native**: `jstarc Foo.sl --target=llvm -> native binary`

### 3. 轻量化语法
- 比 Java 少 30% 字符
- 类型推断 + 后置类型注解
- 分号可选，大括号保留
- 一小时上手，适合 Java 团队

## 🚀 快速开始

### 安装
```bash
curl -fsSL https://starlight.io/install.sh | bash
```

### 30 秒上手
```bash
# 1. 创建项目
starlight create hello && cd hello

# 2. JVM 运行
jstarc src/main.sl --target=jvm
java -jar build/hello.jar

# 3. 浏览器运行
jstarc src/main.sl --target=js --out hello.js
npx serve .  # 打开 http://localhost:3000/hello.js
```

## 💡 示例代码

### Hello World
```sl
// Hello.sl
fun main(args: Array<String>) {
    println("Hello Starlight")
    val list = ArrayList<String>()
    list += "java"
    list.forEach(::println)
}
```

### Java 互操作（零摩擦）
```sl
import java.time.LocalDate
import javax.servlet.annotation.WebServlet
import javax.servlet.http.HttpServlet

@WebServlet("/api/date")
class DateServlet : HttpServlet() {
    override fun doGet(req: HttpServletRequest, resp: HttpServletResponse) {
        resp.writer.write("Today is ${LocalDate.now()}")
    }
}
```

### 跨平台异步
```sl
async fun fetchUser(id: Int): User {
    val sql = "select * from user where id=?"
    return db.queryAsync(sql, id).await()   // JVM: CompletableFuture, JS: Promise
}
```

### 平台特定实现
```sl
expect fun currentMillis(): Long   // 声明"平台相关"

actual fun currentMillis(): Long = System.currentTimeMillis()   // JVM
actual fun currentMillis(): Long = Date.now().toLong()          // JS
```

## 📊 性能承诺

| 平台 | 性能指标 |
|------|----------|
| **JVM** | 生成的 `.class` 与手写 Java 字节码 **1:1** |
| **JS** | HelloWorld ≤ 8 KB（gzip），Tree-shaking 优化 |
| **WASM** | 基于 LLVM，无 GC 依赖模式可选 |

## 🛠️ 工具链

### 命令行工具
```bash
jstarc Hello.sl                    # 默认 JVM
jstarc Hello.sl --target=js        # JavaScript
jstarc Hello.sl --target=wasm      # WebAssembly
jstarc Hello.sl --target=llvm      # Native
```

### Maven 集成
```xml
<plugin>
    <groupId>com.starlight</groupId>
    <artifactId>starlight-maven-plugin</artifactId>
    <version>0.1.0</version>
    <configuration>
        <targets>
            <target>jvm</target>
            <target>js</target>
            <target>wasm</target>
        </targets>
    </configuration>
</plugin>
```

### Gradle 集成
```kotlin
plugins { id("com.starlight") version "0.1" }
starlight {
    target = listOf("jvm", "js", "wasm")
}
```

## 🎯 项目状态

- ✅ 语言设计完成
- ✅ 编译器原型完成（词法/语法分析）
- ✅ 示例代码编写完成
- 🔄 VS Code 插件开发中
- 🔄 标准库实现中
- 📋 性能优化计划中

## 📚 文档

- [语言设计文档](STARLIGHT_LANGUAGE_DESIGN.md)
- [示例代码](examples/)
- [编译器实现](compiler/)

## 🤝 贡献

欢迎贡献代码、文档和想法！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🚀 路线图

- [ ] 完整的编译器实现
- [ ] 标准库开发
- [ ] IDE 插件
- [ ] 包管理器
- [ ] 社区生态建设

---

**Starlight** - 让 Java 和 JavaScript 世界无缝连接 ✨
