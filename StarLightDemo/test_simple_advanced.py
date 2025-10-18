#!/usr/bin/env python3
"""
简化的高级语法分析器测试
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.advanced_parser import AdvancedParser

def test_basic_parsing():
    """测试基本解析功能"""
    print("=== 测试基本解析 ===")
    
    code = """
    func hello() -> string {
        return "Hello World";
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"词法分析成功，生成 {len(tokens)} 个 token")
        
        parser = AdvancedParser(tokens)
        ast = parser.parse()
        print(f"语法分析成功，生成 {len(ast.statements)} 个语句")
        
        if ast.statements:
            func = ast.statements[0]
            print(f"函数名: {func.name}")
        
        return True
    except Exception as e:
        print(f"❌ 基本解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_async_function():
    """测试异步函数"""
    print("\n=== 测试异步函数 ===")
    
    code = """
    async func getData() -> string {
        return "data";
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # 打印 tokens 来调试
        print("Tokens:")
        for i, token in enumerate(tokens[:10]):  # 只显示前10个
            print(f"  {i}: {token}")
        
        parser = AdvancedParser(tokens)
        ast = parser.parse()
        print("✅ 异步函数解析成功")
        return True
    except Exception as e:
        print(f"❌ 异步函数解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_class():
    """测试数据类"""
    print("\n=== 测试数据类 ===")
    
    code = """
    data User {
        name: string;
        age: int;
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        for i, token in enumerate(tokens[:15]):  # 显示前15个
            print(f"  {i}: {token}")
        
        parser = AdvancedParser(tokens)
        ast = parser.parse()
        print("✅ 数据类解析成功")
        return True
    except Exception as e:
        print(f"❌ 数据类解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starlight 高级语法分析器简化测试")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    if test_basic_parsing():
        success_count += 1
    
    if test_async_function():
        success_count += 1
        
    if test_data_class():
        success_count += 1
    
    print(f"\n测试结果: {success_count}/{total_tests} 通过")
    print("=" * 50)
