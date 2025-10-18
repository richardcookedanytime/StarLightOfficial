#!/usr/bin/env python3
"""
测试 JavaScript 后端
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.js_backend import JavaScriptCodeGenerator

def test_js_backend():
    """测试 JavaScript 后端"""
    
    # 测试代码
    test_code = '''
    func greet(name) {
        return "Hello, " + name;
    }
    
    func main() {
        let message = greet("World");
        println(message);
    }
    '''
    
    print("=== JavaScript 后端测试 ===")
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
    
    # 4. JavaScript 代码生成
    print("4. JavaScript 代码生成...")
    generator = JavaScriptCodeGenerator()
    js_code = generator.generate(ast, "hello")
    
    print("   生成的 JavaScript 代码:")
    print("-" * 30)
    print(js_code)
    print("-" * 30)
    
    # 5. 保存文件
    filepath = generator.save_to_file(js_code, "hello.js")
    print(f"   ✅ JavaScript 代码已保存到: {filepath}")
    
    # 6. 测试运行
    print("5. 测试运行...")
    try:
        result = os.popen(f"node {filepath}").read().strip()
        print(f"   运行结果: {result}")
        print("   ✅ JavaScript 代码运行成功！")
    except Exception as e:
        print(f"   ❌ 运行失败: {e}")
    
    print("\n🎉 JavaScript 后端测试完成！")
    return True

if __name__ == "__main__":
    success = test_js_backend()
    sys.exit(0 if success else 1)
