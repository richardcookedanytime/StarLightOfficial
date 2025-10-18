#!/usr/bin/env python3
"""
测试高级语法分析器
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.advanced_parser import AdvancedParser, parse_advanced_program
from compiler.advanced_parser import (
    GenericType, AsyncFunctionDeclaration, AwaitExpression,
    PatternMatch, PatternCase, LambdaExpression, ListComprehension,
    DataClassDeclaration, InterfaceDeclaration
)

def test_generic_types():
    """测试泛型类型解析"""
    print("=== 测试泛型类型 ===")
    
    code = """
    func process<T>(data: List<T>) -> T {
        return data[0];
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 泛型类型解析成功")
        if ast.statements:
            print(f"解析出函数: {ast.statements[0].name}")
    except Exception as e:
        print(f"❌ 泛型类型解析失败: {e}")

def test_async_functions():
    """测试异步函数解析"""
    print("\n=== 测试异步函数 ===")
    
    code = """
    async func fetchData(url: string) -> Promise<string> {
        let response = await http.get(url);
        return response.body;
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 异步函数解析成功")
        if ast.statements:
            func = ast.statements[0]
            print(f"解析出异步函数: {func.name}")
            if hasattr(func, 'is_async'):
                print(f"异步标志: {func.is_async}")
    except Exception as e:
        print(f"❌ 异步函数解析失败: {e}")

def test_pattern_matching():
    """测试模式匹配解析"""
    print("\n=== 测试模式匹配 ===")
    
    code = """
    func handleResult(result: Result<string, Error>) -> string {
        return match result {
            Ok(value) => value,
            Err(error) => "Error: " + error.message
        };
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 模式匹配解析成功")
        if ast.statements:
            print(f"解析出函数: {ast.statements[0].name}")
    except Exception as e:
        print(f"❌ 模式匹配解析失败: {e}")

def test_data_classes():
    """测试数据类解析"""
    print("\n=== 测试数据类 ===")
    
    code = """
    data User<T> {
        id: int;
        name: string;
        data: T;
        
        func getName() -> string {
            return this.name;
        }
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 数据类解析成功")
        if ast.statements:
            data_class = ast.statements[0]
            print(f"解析出数据类: {data_class.name}")
            if hasattr(data_class, 'type_parameters'):
                print(f"类型参数: {data_class.type_parameters}")
            if hasattr(data_class, 'fields'):
                print(f"字段数量: {len(data_class.fields)}")
    except Exception as e:
        print(f"❌ 数据类解析失败: {e}")

def test_interfaces():
    """测试接口解析"""
    print("\n=== 测试接口 ===")
    
    code = """
    interface Drawable<T> {
        func draw(canvas: T) -> void;
        func getSize() -> Size;
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 接口解析成功")
        if ast.statements:
            interface = ast.statements[0]
            print(f"解析出接口: {interface.name}")
            if hasattr(interface, 'type_parameters'):
                print(f"类型参数: {interface.type_parameters}")
            if hasattr(interface, 'methods'):
                print(f"方法数量: {len(interface.methods)}")
    except Exception as e:
        print(f"❌ 接口解析失败: {e}")

def test_lambda_expressions():
    """测试 Lambda 表达式解析"""
    print("\n=== 测试 Lambda 表达式 ===")
    
    code = """
    func main() {
        let add = (x: int, y: int) => x + y;
        let result = add(5, 3);
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ Lambda 表达式解析成功")
        if ast.statements:
            print(f"解析出函数: {ast.statements[0].name}")
    except Exception as e:
        print(f"❌ Lambda 表达式解析失败: {e}")

def test_comprehensive_example():
    """测试综合示例"""
    print("\n=== 测试综合示例 ===")
    
    code = """
    data Result<T, E> {
        value: T;
        error: E;
    }
    
    interface Repository<T> {
        func save(item: T) -> Result<T, Error>;
        func findById(id: int) -> Result<T, Error>;
    }
    
    async func processUsers(repo: Repository<User>) -> void {
        let users = await repo.findAll();
        
        let adults = [user | for user in users if user.age >= 18];
        
        for user in adults {
            let result = match user.status {
                "active" => repo.save(user),
                "inactive" => Result{value: user, error: null},
                _ => Result{value: null, error: "Unknown status"}
            };
            
            match result {
                Ok(savedUser) => println("Saved: " + savedUser.name),
                Err(error) => println("Error: " + error.message)
            }
        }
    }
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = AdvancedParser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ 综合示例解析成功")
        print(f"解析出 {len(ast.statements)} 个语句")
        
        for i, stmt in enumerate(ast.statements):
            print(f"  {i+1}. {type(stmt).__name__}")
            if hasattr(stmt, 'name'):
                print(f"     名称: {stmt.name}")
    except Exception as e:
        print(f"❌ 综合示例解析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starlight 高级语法分析器测试")
    print("=" * 50)
    
    test_generic_types()
    test_async_functions()
    test_pattern_matching()
    test_data_classes()
    test_interfaces()
    test_lambda_expressions()
    test_comprehensive_example()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")
