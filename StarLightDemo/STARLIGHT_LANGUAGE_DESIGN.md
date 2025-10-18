# Starlight 编程语言设计文档

## 概述

**Starlight** 是一款现代、高适配性、前后端通用的编程语言，定位为 **"像 Kotlin 一样 100% 无缝调用 Java，同时一份源码可编译到 JVM / Node / Browser / Native"**。

### 核心口号
**"Write once, run anywhere Java does, and anywhere JavaScript does."**

## 核心设计理念

### 1. 统一性 (Unity)
- 同一套语法用于前端、后端、移动端开发
- 统一的类型系统，无需类型转换
- 一致的 API 设计模式

### 2. 安全性 (Safety)
- 内存安全，无空指针异常
- 编译时错误检测
- 内置的安全并发模型

### 3. 性能 (Performance)
- 编译到 WebAssembly (前端)
- 编译到机器码 (后端)
- 零成本抽象

### 4. 简洁性 (Simplicity)
- 直观的语法设计
- 强大的类型推断
- 最小化样板代码

## 主要特性

### 类型系统
- **静态类型** + **类型推断**
- **可选类型** (类似 TypeScript)
- **联合类型** 和 **交集类型**
- **泛型** 支持
- **模式匹配**

### 内存管理
- **自动内存管理** (类似 Rust 的所有权系统)
- **零垃圾回收** (编译时确定生命周期)
- **内存安全保证**

### 并发模型
- **Actor 模型** (类似 Erlang)
- **协程** 支持
- **异步/等待** 语法糖

### 平台支持
- **Web** (编译到 WebAssembly)
- **Server** (编译到机器码)
- **Mobile** (编译到原生代码)
- **Desktop** (跨平台 GUI)

## 语法设计

### 基础语法

```starlight
// 变量声明 (类型推断)
name := "Starlight"
age := 25
isActive := true

// 显式类型声明
name: string = "Starlight"
count: int = 0
items: [string] = ["apple", "banana"]

// 函数定义
func greet(name: string) -> string {
    return "Hello, ${name}!"
}

// 箭头函数
greet := (name: string) -> string => "Hello, ${name}!"

// 泛型函数
func identity<T>(value: T) -> T {
    return value
}
```

### 类型系统

```starlight
// 联合类型
type Result<T> = Success(T) | Error(string)

// 结构体
struct Person {
    name: string
    age: int
    email?: string  // 可选字段
}

// 枚举
enum Status {
    Pending
    Running
    Completed
    Failed(reason: string)
}

// 接口
interface Drawable {
    func draw(): void
    func getArea(): float
}
```

### 模式匹配

```starlight
func handleResult(result: Result<int>) -> string {
    match result {
        Success(value) => "Got: ${value}"
        Error(msg) => "Error: ${msg}"
    }
}

// 解构
match person {
    Person{name, age: 18..65, email: Some(email)} => 
        "Adult ${name} with email ${email}"
    Person{name, age: 0..17} => 
        "Minor ${name}"
    _ => "Unknown person"
}
```

### 异步编程

```starlight
// 异步函数
async func fetchData(url: string) -> Result<string> {
    try {
        response := await http.get(url)
        return Success(response.body)
    } catch (error) {
        return Error(error.message)
    }
}

// 并发处理
async func processItems(items: [string]) -> [string] {
    tasks := items.map(item => processItem(item))
    results := await Promise.all(tasks)
    return results
}
```

### Actor 模型

```starlight
// Actor 定义
actor Counter {
    state: int = 0
    
    // 消息处理
    receive Add(value: int) {
        state += value
        reply(state)
    }
    
    receive Get() {
        reply(state)
    }
}

// 使用 Actor
counter := spawn Counter()
result := await counter.send(Add(5))
current := await counter.send(Get())
```

## 平台特定特性

### Web 端
```starlight
// DOM 操作
button := document.getElementById("myButton")
button.addEventListener("click", () => {
    console.log("Button clicked!")
})

// WebSocket
socket := new WebSocket("ws://localhost:8080")
socket.onMessage((data) => {
    console.log("Received: ${data}")
})
```

### 后端
```starlight
// HTTP 服务器
server := new HttpServer()

server.get("/api/users", async (req) => {
    users := await database.query("SELECT * FROM users")
    return Response.json(users)
})

server.post("/api/users", async (req) -> {
    user := req.json<User>()
    result := await database.insert(user)
    return Response.json(result)
})

server.listen(8080)
```

## 优势对比

| 特性 | JavaScript/TypeScript | Rust | Go | Starlight |
|------|---------------------|------|-----|-----------|
| 前后端统一 | ✅ | ❌ | ✅ | ✅ |
| 内存安全 | ❌ | ✅ | ❌ | ✅ |
| 性能 | ❌ | ✅ | ✅ | ✅ |
| 学习曲线 | ✅ | ❌ | ✅ | ✅ |
| 类型安全 | 部分 | ✅ | 部分 | ✅ |
| 并发模型 | Promise | 复杂 | Goroutine | Actor+协程 |
| 编译到 WASM | 需要工具 | ✅ | ❌ | ✅ |

## 实现计划

1. **词法分析器** - 解析源代码为 Token
2. **语法分析器** - 构建抽象语法树
3. **类型检查器** - 静态类型分析
4. **中间表示** - 生成 IR
5. **代码生成器** - 生成目标代码
6. **标准库** - 基础 API 和工具
7. **包管理器** - 依赖管理
8. **开发工具** - IDE 支持、调试器

## 下一步

- 实现基础编译器框架
- 创建示例代码
- 开发标准库
- 编写文档和教程
