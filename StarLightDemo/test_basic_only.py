#!/usr/bin/env python3
"""
基础 Starlight 测试 - 只测试基本功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.parser import Parser

def test_basic_function():
    """测试基本函数解析"""
    print("=== 测试基本函数解析 ===")
    
    code = """
    fun greet(name) {
        return "Hello, " + name;
    }
    
    fun main() {
        let message = greet("World");
        println(message);
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✅ 词法分析成功，生成 {len(tokens)} 个 token")
        
        # 使用基础解析器
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✅ 语法分析成功，生成 {len(ast.statements)} 个语句")
        
        for i, stmt in enumerate(ast.statements):
            print(f"  语句 {i}: {type(stmt).__name__}")
            if hasattr(stmt, 'name'):
                print(f"    名称: {stmt.name}")
        
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_variable_declaration():
    """测试变量声明"""
    print("\n=== 测试变量声明 ===")
    
    code = """
    let x = 42;
    let name = "Starlight";
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✅ 词法分析成功，生成 {len(tokens)} 个 token")
        
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✅ 语法分析成功，生成 {len(ast.statements)} 个语句")
        
        for i, stmt in enumerate(ast.statements):
            print(f"  语句 {i}: {type(stmt).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starlight 基础功能测试")
    print("=" * 40)
    
    success_count = 0
    total_tests = 2
    
    if test_basic_function():
        success_count += 1
    
    if test_variable_declaration():
        success_count += 1
    
    print(f"\n测试结果: {success_count}/{total_tests} 通过")
    print("=" * 40)
    
    if success_count == total_tests:
        print("🎉 所有测试通过！基础功能正常！")
    else:
        print(f"⚠️  有 {total_tests - success_count} 个测试失败")
