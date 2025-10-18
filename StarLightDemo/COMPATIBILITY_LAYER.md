# Starlight 兼容层设计

## 🎯 兼容策略概述

Starlight 采用 **Java/Kotlin 超集策略**，确保：
1. **源码级双向兼容**：任何 Java/Kotlin 文件可直接被 Starlight 调用
2. **零桥接层**：无需转换或适配代码
3. **渐进式迁移**：可以逐步将现有项目迁移到 Starlight

## 📋 兼容级别定义

### Java 兼容性 (100%)

| 特性 | 兼容策略 | 示例 |
|------|----------|------|
| 类继承 | 直接支持 | `class MyClass : ArrayList<String>()` |
| 接口实现 | 直接支持 | `class Service : Servlet` |
| 注解使用 | 100% 兼容 | `@RestController class Api` |
| 泛型系统 | 完全复用 | `List<Map<String, Object>>` |
| 异常处理 | 直接兼容 | `try { } catch (IOException e) { }` |
| 反射 API | 完全支持 | `Class.forName("java.util.List")` |

### Kotlin 兼容性 (95%)

| 特性 | 兼容策略 | 示例 |
|------|----------|------|
| 空安全 | 扩展支持 | `String?` + 自动抬升 |
| 扩展函数 | 语法调整 | `extend String { fun foo() }` |
| 数据类 | 语法统一 | `data User(name: String, age: Int)` |
| 协程 | 完全支持 | `async fun fetch() { await api.get() }` |
| 类型推断 | 增强版 | `val list = ArrayList<String>()` |

## 🔧 关键字冲突解决

### 逃逸策略

使用 `@` 前缀解决关键字冲突：

```starlight
// 当需要访问 Java 中的 Starlight 关键字时
val list = new ArrayList<String>()
list.add("test")

// 使用 @ 前缀逃逸
val @await = "some value"  // 避免与 await 关键字冲突
val @rule = "rule name"    // 避免与 rule 关键字冲突
```

### 关键字映射表

| Starlight | Java 等价 | 说明 |
|-----------|-----------|------|
| `fun` | `public static` | 函数声明 |
| `val` | `final` | 不可变变量 |
| `var` | 无 | 可变变量 |
| `data` | `record` | 数据类 |
| `match` | `switch` | 模式匹配 |
| `rule` | 无 | 规则系统 |

## 🏗️ 类型系统兼容

### 基本类型映射

```starlight
// Starlight 类型 → Java 类型
type_mapping = {
    "int"     -> "int",
    "long"    -> "long", 
    "float"   -> "float",
    "double"  -> "double",
    "boolean" -> "boolean",
    "char"    -> "char",
    "string"  -> "String",
    "void"    -> "void"
}

// 容器类型映射
container_mapping = {
    "List<T>"    -> "java.util.List<T>",
    "Map<K,V>"   -> "java.util.Map<K,V>",
    "Set<T>"     -> "java.util.Set<T>",
    "Optional<T>" -> "java.util.Optional<T>"
}
```

### 泛型系统兼容

```starlight
// Java 泛型完全兼容
class GenericClass<T extends Comparable<T>> {
    fun process(items: List<T>): List<T> {
        return items.sorted()
    }
}

// Kotlin 协变/逆变支持
interface Producer<out T> {
    fun produce(): T
}

interface Consumer<in T> {
    fun consume(item: T)
}
```

## 📦 模块系统兼容

### Java 模块系统

```starlight
// 支持 module-info.java
module com.example.starlight {
    requires java.base;
    requires java.logging;
    exports com.example.starlight.api;
    provides com.example.starlight.Service 
        with com.example.starlight.ServiceImpl;
}
```

### Kotlin Multiplatform

```starlight
// 支持 Kotlin MPP 声明
@file:Suppress("ACTUAL_FUNCTION_WITH_DEFAULT_ARGUMENTS")

expect class Platform() {
    val name: String
}

expect fun getLines(): List<String>

actual class Platform actual constructor() {
    actual val name: String = "JVM"
}

actual fun getLines(): List<String> = 
    java.nio.file.Files.readAllLines(
        java.nio.file.Paths.get("input.txt")
    )
```

## 🔄 注解系统兼容

### Java 注解处理器

```starlight
// 支持 kapt (Kotlin Annotation Processing Tool)
@AutoService(Processor::class)
class StarlightProcessor : AbstractProcessor() {
    override fun process(
        annotations: MutableSet<out TypeElement>?,
        roundEnv: RoundEnvironment
    ): Boolean {
        // 处理注解
        return true
    }
}

// Spring Boot 完全兼容
@SpringBootApplication
@RestController
class StarlightApp {
    @GetMapping("/api/hello")
    fun hello(): ResponseEntity<String> {
        return ResponseEntity.ok("Hello from Starlight!")
    }
}
```

### 自定义注解

```starlight
// 定义注解
@Target(AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class StarlightApi(val version: String = "1.0")

// 使用注解
@StarlightApi("2.0")
fun advancedFunction(): String {
    return "Advanced functionality"
}
```

## 🚀 编译策略

### 编译到 Java

```starlight
// Starlight 源码
data User(name: String, age: Int) {
    fun isAdult(): Boolean = age >= 18
}

// 编译后的 Java 代码
public final class User {
    private final String name;
    private final int age;
    
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    
    public boolean isAdult() {
        return age >= 18;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        User user = (User) obj;
        return age == user.age && Objects.equals(name, user.name);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
    
    @Override
    public String toString() {
        return "User(name=" + name + ", age=" + age + ")";
    }
}
```

### 编译到 Kotlin

```starlight
// Starlight 源码
extend String {
    fun isEmail(): Boolean = this.contains("@")
}

// 编译后的 Kotlin 代码
fun String.isEmail(): Boolean = this.contains("@")
```

## 🔧 运行时兼容

### JVM 字节码兼容

```starlight
// Starlight 函数
fun calculate(a: Int, b: Int): Int = a + b

// 生成的字节码等同于
public static int calculate(int a, int b) {
    return a + b;
}
```

### 反射兼容

```starlight
// Starlight 类可以通过 Java 反射访问
val clazz = Class.forName("com.example.StarlightClass")
val method = clazz.getMethod("starlightMethod", String::class.java)
val result = method.invoke(instance, "test")
```

## 📚 标准库兼容

### Java 标准库直接使用

```starlight
// 直接使用 Java 标准库
import java.time.LocalDate
import java.util.stream.Collectors

fun processDates(): List<String> {
    val dates = listOf(
        LocalDate.now(),
        LocalDate.now().plusDays(1),
        LocalDate.now().plusDays(2)
    )
    
    return dates.stream()
        .map { it.toString() }
        .collect(Collectors.toList())
}
```

### Kotlin 标准库扩展

```starlight
// 使用 Kotlin 标准库功能
import kotlin.collections.*
import kotlin.coroutines.*

fun processList(): List<String> {
    val numbers = listOf(1, 2, 3, 4, 5)
    return numbers
        .filter { it % 2 == 0 }
        .map { it.toString() }
}
```

## 🧪 兼容性测试

### 自动化测试套件

```starlight
// 测试 Java 兼容性
@Test
fun testJavaCompatibility() {
    // 测试 Java 类继承
    val list = ArrayList<String>()
    assert(list.add("test"))
    
    // 测试 Java 接口实现
    val servlet = object : HttpServlet() {
        override fun doGet(req: HttpServletRequest, resp: HttpServletResponse) {
            resp.writer.write("Hello")
        }
    }
    
    // 测试 Java 注解
    @Test
    fun annotatedMethod() {
        assert(true)
    }
}

// 测试 Kotlin 兼容性
@Test
fun testKotlinCompatibility() {
    // 测试空安全
    val nullable: String? = null
    val safe = nullable ?: "default"
    assert(safe == "default")
    
    // 测试扩展函数
    val extended = "test".let { it.uppercase() }
    assert(extended == "TEST")
}
```

## 📋 迁移指南

### 从 Java 迁移到 Starlight

1. **重命名文件**：`.java` → `.sl`
2. **语法调整**：`public static void main` → `fun main()`
3. **类型推断**：`String name = "test"` → `val name = "test"`
4. **保持兼容**：所有 Java 代码保持不变

### 从 Kotlin 迁移到 Starlight

1. **重命名文件**：`.kt` → `.sl`
2. **语法统一**：`fun String.foo()` → `extend String { fun foo() }`
3. **增强功能**：添加规则系统和推导式
4. **保持兼容**：大部分 Kotlin 代码保持不变

## 🎯 兼容性保证

### 向后兼容承诺

1. **语义兼容**：相同代码产生相同结果
2. **API 兼容**：所有 Java/Kotlin API 可用
3. **性能兼容**：编译后性能不降低
4. **工具兼容**：支持现有开发工具

### 版本兼容策略

```starlight
// 版本声明
@version("1.0")
package com.example

// 特性开关
@feature("rules", enabled = true)
@feature("comprehensions", enabled = false)
```

---

**Starlight Compatibility Layer** - 无缝连接 Java 和 Kotlin 世界 ✨
