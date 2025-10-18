#!/usr/bin/env python3
"""
调试 AST 结构
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.parser import Parser, FunctionDeclaration, VariableDeclaration, ExpressionStatement

def debug_ast():
    """调试 AST 结构"""
    
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, " + name;
    }
    
    func main() {
        let message = greet("World");
        println(message);
    }
    '''
    
    print("=== 调试 AST 结构 ===")
    
    # 词法分析
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    # 语法分析
    parser = Parser(tokens)
    ast = parser.parse()
    
    print(f"程序有 {len(ast.statements)} 个语句:")
    
    for i, stmt in enumerate(ast.statements):
        print(f"\n语句 {i}: {type(stmt).__name__}")
        
        if isinstance(stmt, FunctionDeclaration):
            print(f"  函数名: {stmt.name}")
            print(f"  参数: {stmt.parameters}")
            print(f"  返回类型: {stmt.return_type}")
            print(f"  函数体有 {len(stmt.body)} 个语句:")
            
            for j, body_stmt in enumerate(stmt.body):
                print(f"    语句 {j}: {type(body_stmt).__name__}")
                
                if isinstance(body_stmt, VariableDeclaration):
                    print(f"      变量名: {body_stmt.name}")
                    print(f"      类型: {body_stmt.type_annotation}")
                    print(f"      初始化器: {type(body_stmt.initializer).__name__}")
                    
                    if hasattr(body_stmt.initializer, 'callee'):
                        print(f"        调用函数: {body_stmt.initializer.callee}")
                        print(f"        参数: {body_stmt.initializer.arguments}")
                
                elif isinstance(body_stmt, ExpressionStatement):
                    print(f"      表达式: {type(body_stmt.expression).__name__}")
                    
                    if hasattr(body_stmt.expression, 'callee'):
                        print(f"        调用函数: {body_stmt.expression.callee}")
                        print(f"        参数: {body_stmt.expression.arguments}")

if __name__ == "__main__":
    debug_ast()
