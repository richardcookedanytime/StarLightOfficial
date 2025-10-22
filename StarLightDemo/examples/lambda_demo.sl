// Lambda 表达式示例

fun main() {
    // 简单的 Lambda 表达式
    let add = (a: int, b: int) => a + b
    let result1 = add(5, 3)
    println("5 + 3 = " + result1)
    
    // 无参数 Lambda
    let greeting = () => "Hello, Starlight!"
    let msg = greeting()
    println(msg)
    
    // Lambda 作为高阶函数参数
    let numbers = [1, 2, 3, 4, 5]
    let doubled = map(numbers, (x: int) => x * 2)
    println("Doubled: " + doubled)
    
    // Lambda 用于过滤
    let evens = filter(numbers, (x: int) => x % 2 == 0)
    println("Evens: " + evens)
}

// 高阶函数：map
fun map(list: array, fn: function): array {
    let result = []
    for item in list {
        result.add(fn(item))
    }
    return result
}

// 高阶函数：filter
fun filter(list: array, predicate: function): array {
    let result = []
    for item in list {
        if predicate(item) {
            result.add(item)
        }
    }
    return result
}

