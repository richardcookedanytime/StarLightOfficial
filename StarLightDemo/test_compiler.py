#!/usr/bin/env python3
"""
测试 Starlight 编译器完整流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.jvm_backend import JVMCodeGenerator

def test_compiler():
    """测试编译器完整流程"""
    
    # 测试代码
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, " + name;
    }
    
    func main() {
        let message = greet("World");
        println(message);
    }
    '''
    
    print("=== Starlight 编译器测试 ===")
    print(f"测试代码:\n{test_code}")
    print("\n" + "="*50)
    
    # 1. 词法分析
    print("1. 词法分析...")
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    print(f"   生成 {len(tokens)} 个 token")
    
    # 2. 语法分析
    print("2. 语法分析...")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"   解析出 {len(ast.statements)} 个语句")
    
    # 3. 语义分析
    print("3. 语义分析...")
    analyzer = SemanticAnalyzer()
    semantic_result = analyzer.analyze(ast)
    
    if semantic_result['success']:
        print("   ✅ 语义分析成功")
        print(f"   符号表: {len(semantic_result['symbols'])} 个符号")
    else:
        print("   ❌ 语义分析失败:")
        for error in semantic_result['errors']:
            print(f"      - {error['message']}")
        return False
    
    # 4. 代码生成
    print("4. JVM 代码生成...")
    generator = JVMCodeGenerator()
    java_code = generator.generate(ast, "HelloWorld")
    
    print("   生成的 Java 代码:")
    print("-" * 30)
    print(java_code)
    print("-" * 30)
    
    # 5. 保存文件
    filepath = generator.save_to_file(java_code, "HelloWorld.java")
    print(f"   ✅ Java 代码已保存到: {filepath}")
    
    print("\n🎉 编译器测试完成！")
    return True

if __name__ == "__main__":
    success = test_compiler()
    sys.exit(0 if success else 1)
