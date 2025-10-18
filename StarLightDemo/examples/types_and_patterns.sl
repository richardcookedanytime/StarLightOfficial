// Starlight 语言 - 类型系统和模式匹配示例

// 联合类型定义
type Result<T> = Success(T) | Error(string);

// 枚举定义
enum Status {
    Pending
    Running
    Completed
    Failed(reason: string)
}

// 结构体定义
struct Person {
    name: string
    age: int
    email?: string  // 可选字段
    status: Status
}

// 模式匹配函数
func handlePerson(person: Person) -> string {
    match person {
        Person{name, age: 18..65, status: Status.Completed} =>
            "Adult ${name} has completed their task"
        Person{name, age: 0..17} =>
            "Minor ${name} is still growing up"
        Person{name, status: Status.Failed(reason)} =>
            "Sorry ${name}, failed: ${reason}"
        _ =>
            "Unknown person status"
    }
}

// 结果处理函数
func processResult(result: Result<int>) -> string {
    match result {
        Success(value) =>
            "Operation succeeded with value: ${value}"
        Error(msg) =>
            "Operation failed: ${msg}"
    }
}

// 使用示例
let person1 = Person{
    name: "Alice",
    age: 25,
    email: Some("alice@example.com"),
    status: Status.Completed
};

let person2 = Person{
    name: "Bob",
    age: 16,
    status: Status.Failed("Network timeout")
};

console.log(handlePerson(person1));
console.log(handlePerson(person2));

let successResult = Success(42);
let errorResult = Error("Something went wrong");

console.log(processResult(successResult));
console.log(processResult(errorResult));
