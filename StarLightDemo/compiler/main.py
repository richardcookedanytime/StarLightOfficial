#!/usr/bin/env python3
"""
Starlight 编程语言 - 主编译器入口
"""

import sys
import argparse
from pathlib import Path
from lexer import Lexer
from parser import Parser

def main():
    parser = argparse.ArgumentParser(description='Starlight 编程语言编译器')
    parser.add_argument('input_file', help='输入的 Starlight 源文件')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--tokens', action='store_true', help='只进行词法分析，输出 tokens')
    parser.add_argument('--ast', action='store_true', help='只进行语法分析，输出 AST')
    parser.add_argument('--target', choices=['wasm', 'native', 'js'], default='wasm', 
                       help='目标平台 (默认: wasm)')
    
    args = parser.parse_args()
    
    try:
        # 读取源文件
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"Compiling {args.input_file}...")
        
        # 词法分析
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if args.tokens:
            print("\n=== Tokens ===")
            for token in tokens:
                print(token)
            return
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        if args.ast:
            print("\n=== AST ===")
            print_ast(ast, indent=0)
            return
        
        # 代码生成 (这里只是占位符)
        print("Code generation not implemented yet.")
        print(f"Target platform: {args.target}")
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_ast(node, indent=0):
    """打印 AST 结构"""
    spaces = "  " * indent
    
    if hasattr(node, '__dict__'):
        class_name = node.__class__.__name__
        print(f"{spaces}{class_name}")
        
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                print(f"{spaces}  {key}:")
                for item in value:
                    print_ast(item, indent + 2)
            elif hasattr(value, '__dict__'):
                print(f"{spaces}  {key}:")
                print_ast(value, indent + 2)
            else:
                print(f"{spaces}  {key}: {value}")
    else:
        print(f"{spaces}{node}")

if __name__ == "__main__":
    main()
