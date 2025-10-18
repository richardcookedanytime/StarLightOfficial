// Starlight 语言 - Hello World 示例
// 展示基本的函数定义和调用

func main() {
    let message = greet("Starlight");
    console.log(message);
}

func greet(name: string) -> string {
    return "Hello, ${name}! Welcome to the future of programming!";
}

// 箭头函数语法
let greetShort = (name: string) -> string => "Hi, ${name}!";

// 调用示例
main();
