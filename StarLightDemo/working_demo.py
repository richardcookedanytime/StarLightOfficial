#!/usr/bin/env python3
"""
Starlight 工作演示 - 展示完整的编译流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.jvm_backend import JVMCodeGenerator
from compiler.js_backend import JavaScriptCodeGenerator

def demo_hello_world():
    """演示 Hello World 编译"""
    print("🚀 === Starlight Hello World 演示 ===")
    
    code = """
    fun greet(name) {
        return "Hello, " + name + "! Welcome to Starlight!";
    }
    
    fun main() {
        let message = greet("World");
        println(message);
    }
    """
    
    try:
        # 词法分析
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✅ 词法分析成功，生成 {len(tokens)} 个 token")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✅ 语法分析成功，生成 {len(ast.statements)} 个语句")
        
        # JVM 代码生成
        jvm_generator = JVMCodeGenerator()
        java_code = jvm_generator.generate(ast, "HelloWorld")
        print("✅ JVM 代码生成成功")
        
        # JavaScript 代码生成
        js_generator = JavaScriptCodeGenerator()
        js_code = js_generator.generate(ast, "hello")
        print("✅ JavaScript 代码生成成功")
        
        # 保存生成的文件
        os.makedirs("build", exist_ok=True)
        
        with open("build/HelloWorld.java", "w", encoding="utf-8") as f:
            f.write(java_code)
        print("📁 保存到: build/HelloWorld.java")
        
        with open("build/hello.js", "w", encoding="utf-8") as f:
            f.write(js_code)
        print("📁 保存到: build/hello.js")
        
        # 显示生成的代码
        print("\n📋 生成的 Java 代码:")
        print("-" * 50)
        print(java_code)
        print("-" * 50)
        
        print("\n📋 生成的 JavaScript 代码:")
        print("-" * 50)
        print(js_code)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_calculator():
    """演示计算器编译"""
    print("\n🧮 === Starlight 计算器演示 ===")
    
    code = """
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
    """
    
    try:
        # 词法分析
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✅ 词法分析成功，生成 {len(tokens)} 个 token")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✅ 语法分析成功，生成 {len(ast.statements)} 个语句")
        
        # JVM 代码生成
        jvm_generator = JVMCodeGenerator()
        java_code = jvm_generator.generate(ast, "Calculator")
        print("✅ JVM 代码生成成功")
        
        # 保存生成的文件
        with open("build/Calculator.java", "w", encoding="utf-8") as f:
            f.write(java_code)
        print("📁 保存到: build/Calculator.java")
        
        # 显示生成的代码
        print("\n📋 生成的计算器 Java 代码:")
        print("-" * 50)
        print(java_code)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_web_app():
    """演示 Web 应用编译"""
    print("\n🌐 === Starlight Web 应用演示 ===")
    
    code = """
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
        console.log("Web app initialized!");
    }
    """
    
    try:
        # 词法分析
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✅ 词法分析成功，生成 {len(tokens)} 个 token")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✅ 语法分析成功，生成 {len(ast.statements)} 个语句")
        
        # JavaScript 代码生成
        js_generator = JavaScriptCodeGenerator()
        js_code = js_generator.generate(ast, "webApp")
        print("✅ JavaScript 代码生成成功")
        
        # 保存生成的文件
        with open("build/webApp.js", "w", encoding="utf-8") as f:
            f.write(js_code)
        print("📁 保存到: build/webApp.js")
        
        # 创建 HTML 文件
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Starlight Web Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        button { padding: 10px 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Starlight Web Demo</h1>
    <script src="webApp.js"></script>
</body>
</html>"""
        
        with open("build/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("📁 保存到: build/index.html")
        
        # 显示生成的代码
        print("\n📋 生成的 Web 应用 JavaScript 代码:")
        print("-" * 50)
        print(js_code)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主演示函数"""
    print("🌟 === Starlight 编程语言工作演示 ===")
    print("=" * 60)
    
    # 创建构建目录
    os.makedirs("build", exist_ok=True)
    
    # 运行所有演示
    demos = [
        demo_hello_world,
        demo_calculator,
        demo_web_app
    ]
    
    success_count = 0
    total_demos = len(demos)
    
    for demo in demos:
        if demo():
            success_count += 1
        print()  # 空行分隔
    
    # 总结
    print("=" * 60)
    print(f"🎯 演示结果: {success_count}/{total_demos} 成功")
    
    if success_count == total_demos:
        print("🎉 所有演示成功！Starlight 编译器工作正常！")
        print("\n📋 生成的文件:")
        print("  - build/HelloWorld.java (Hello World 程序)")
        print("  - build/hello.js (Hello World JavaScript)")
        print("  - build/Calculator.java (计算器程序)")
        print("  - build/webApp.js (Web 应用)")
        print("  - build/index.html (Web 演示页面)")
        
        print("\n🚀 下一步:")
        print("  1. 编译 Java 文件: javac build/*.java")
        print("  2. 运行 Java 程序: java -cp build HelloWorld")
        print("  3. 打开 Web 页面: open build/index.html")
        print("  4. 查看项目文档: README.md")
    else:
        print(f"⚠️  有 {total_demos - success_count} 个演示失败，请检查错误信息")
    
    print("\n✨ Starlight - 让编程更简洁，让世界更连接！")

if __name__ == "__main__":
    main()
