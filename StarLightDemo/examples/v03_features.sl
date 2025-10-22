// Starlight v0.3.0 新特性展示

// ============================================
// 1. Lambda 表达式
// ============================================

fun demonstrateLambda() {
    println("=== Lambda 表达式示例 ===")
    
    // 基本 Lambda
    let square = (x: int) => x * x
    println("Square of 5: " + square(5))
    
    // 多参数 Lambda
    let add = (a: int, b: int) => a + b
    println("3 + 7 = " + add(3, 7))
    
    // Lambda 作为参数
    let numbers = [1, 2, 3, 4, 5]
    let doubled = map(numbers, (x: int) => x * 2)
    println("Doubled: " + doubled)
}

// ============================================
// 2. 字符串插值
// ============================================

fun demonstrateStringInterpolation() {
    println("=== 字符串插值示例 ===")
    
    let name = "Alice"
    let age = 25
    let city = "Beijing"
    
    // 基本插值
    let intro = "My name is ${name}, I'm ${age} years old."
    println(intro)
    
    // 表达式插值
    let calculation = "Next year I'll be ${age + 1} years old."
    println(calculation)
    
    // 组合插值
    let info = "I'm ${name} from ${city}, age ${age}"
    println(info)
}

// ============================================
// 3. 数据类与模式匹配组合
// ============================================

data Result(success: boolean, value: string, error: string) {
    fun isOk(): boolean = success
    
    fun getOrDefault(default: string): string = 
        if (success) value else default
}

fun demonstrateDataClassWithMatch() {
    println("=== 数据类与模式匹配 ===")
    
    let result1 = Result(true, "Success!", "")
    let result2 = Result(false, "", "Error occurred")
    
    // 模式匹配处理结果
    fun handleResult(r: Result): string {
        return match r.success {
            true => "Operation succeeded: ${r.value}"
            false => "Operation failed: ${r.error}"
            _ => "Unknown result"
        }
    }
    
    println(handleResult(result1))
    println(handleResult(result2))
}

// ============================================
// 4. 高阶函数
// ============================================

fun map(list: array, fn: function): array {
    let result = []
    for item in list {
        result.add(fn(item))
    }
    return result
}

fun filter(list: array, predicate: function): array {
    let result = []
    for item in list {
        if predicate(item) {
            result.add(item)
        }
    }
    return result
}

fun reduce(list: array, initial: any, fn: function): any {
    let result = initial
    for item in list {
        result = fn(result, item)
    }
    return result
}

fun demonstrateHigherOrderFunctions() {
    println("=== 高阶函数示例 ===")
    
    let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    // 映射：每个数乘以2
    let doubled = map(numbers, (x: int) => x * 2)
    println("Doubled: " + doubled)
    
    // 过滤：只保留偶数
    let evens = filter(numbers, (x: int) => x % 2 == 0)
    println("Evens: " + evens)
    
    // 归约：求和
    let sum = reduce(numbers, 0, (acc: int, x: int) => acc + x)
    println("Sum: " + sum)
}

// ============================================
// 5. 类型推断增强
// ============================================

fun demonstrateTypeInference() {
    println("=== 类型推断示例 ===")
    
    // 自动推断为 int
    let x = 42
    println("x = " + x)
    
    // 自动推断为 string
    let message = "Hello"
    println("message = " + message)
    
    // Lambda 返回类型推断
    let multiply = (a, b) => a * b
    println("5 * 6 = " + multiply(5, 6))
}

// ============================================
// 主函数
// ============================================

fun main() {
    println("╔════════════════════════════════════╗")
    println("║  Starlight v0.3.0 功能展示         ║")
    println("╚════════════════════════════════════╝")
    println("")
    
    demonstrateLambda()
    println("")
    
    demonstrateStringInterpolation()
    println("")
    
    demonstrateDataClassWithMatch()
    println("")
    
    demonstrateHigherOrderFunctions()
    println("")
    
    demonstrateTypeInference()
    println("")
    
    println("╔════════════════════════════════════╗")
    println("║  所有功能演示完成！                ║")
    println("╚════════════════════════════════════╝")
}

