// 字符串插值示例

fun main() {
    let name = "Alice"
    let age = 25
    
    // 字符串插值语法: ${expression}
    let greeting = "Hello, ${name}! You are ${age} years old."
    println(greeting)
    
    // 表达式插值
    let x = 10
    let y = 20
    let result = "The sum of ${x} and ${y} is ${x + y}"
    println(result)
    
    // 嵌套插值
    let user = User("Bob", 30)
    let message = "User: ${user.name}, Age: ${user.age}"
    println(message)
}

data User(name: string, age: int) {
}

