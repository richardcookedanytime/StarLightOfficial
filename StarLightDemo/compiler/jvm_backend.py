#!/usr/bin/env python3
"""
Starlight 编程语言 - JVM 后端代码生成器
负责将 AST 转换为 Java 字节码
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .parser import *
from .semantic_analyzer import SemanticAnalyzer

@dataclass
class JVMType:
    """JVM 类型表示"""
    descriptor: str  # JVM 类型描述符
    java_type: str   # Java 类型名称
    
    @classmethod
    def from_starlight_type(cls, starlight_type: str) -> 'JVMType':
        """从 Starlight 类型转换为 JVM 类型"""
        type_mapping = {
            'int': cls('I', 'int'),
            'float': cls('F', 'float'),
            'string': cls('Ljava/lang/String;', 'String'),
            'boolean': cls('Z', 'boolean'),
            'void': cls('V', 'void'),
            'any': cls('Ljava/lang/Object;', 'Object')
        }
        return type_mapping.get(starlight_type, cls('Ljava/lang/Object;', 'Object'))

class JVMCodeGenerator:
    def __init__(self):
        self.class_name = ""
        self.output_dir = "build"
        self.java_code = []
        self.imports = set()
        self.method_count = 0
        
    def generate(self, program: Program, class_name: str = "Main") -> str:
        """生成 Java 代码"""
        self.class_name = class_name
        self.java_code = []
        self.imports.clear()
        self.method_count = 0
        
        # 生成类头
        self._generate_class_header()
        
        # 生成 main 方法
        self._generate_main_method(program)
        
        # 生成其他方法
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration) and stmt.name != "main":
                self._generate_function(stmt)
        
        # 生成类尾
        self._generate_class_footer()
        
        # 生成完整的 Java 代码
        return self._generate_complete_java_code()
    
    def _generate_class_header(self):
        """生成类头"""
        self.java_code.append(f"public class {self.class_name} {{")
        self.java_code.append("")
    
    def _generate_class_footer(self):
        """生成类尾"""
        self.java_code.append("}")
    
    def _generate_main_method(self, program: Program):
        """生成 main 方法"""
        self.java_code.append("    public static void main(String[] args) {")
        
        # 查找 main 函数调用
        main_called = False
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration) and stmt.name == "main":
                self._generate_function_body(stmt.body, indent="        ")
                main_called = True
                break
        
        if not main_called:
            # 生成其他语句
            for stmt in program.statements:
                if not isinstance(stmt, FunctionDeclaration):
                    self._generate_statement(stmt, indent="        ")
        
        self.java_code.append("    }")
        self.java_code.append("")
    
    def _generate_function(self, func: FunctionDeclaration):
        """生成函数"""
        # 生成方法签名
        return_type = JVMType.from_starlight_type(func.return_type or "void")
        params = []
        
        for param_name, param_type in func.parameters:
            jvm_type = JVMType.from_starlight_type(param_type or "any")
            params.append(f"{jvm_type.java_type} {param_name}")
        
        method_signature = f"public static {return_type.java_type} {func.name}({', '.join(params)}) {{"
        self.java_code.append(f"    {method_signature}")
        
        # 生成方法体
        self._generate_function_body(func.body, indent="        ")
        
        self.java_code.append("    }")
        self.java_code.append("")
    
    def _generate_function_body(self, body: List[Statement], indent: str = ""):
        """生成函数体"""
        for stmt in body:
            self._generate_statement(stmt, indent)
    
    def _generate_statement(self, stmt: Statement, indent: str = ""):
        """生成语句"""
        if isinstance(stmt, VariableDeclaration):
            self._generate_variable_declaration(stmt, indent)
        elif isinstance(stmt, ReturnStatement):
            self._generate_return_statement(stmt, indent)
        elif isinstance(stmt, ExpressionStatement):
            self._generate_expression_statement(stmt, indent)
        elif isinstance(stmt, IfStatement):
            self._generate_if_statement(stmt, indent)
        elif isinstance(stmt, WhileStatement):
            self._generate_while_statement(stmt, indent)
        elif isinstance(stmt, BlockStatement):
            self._generate_block_statement(stmt, indent)
    
    def _generate_variable_declaration(self, var: VariableDeclaration, indent: str):
        """生成变量声明"""
        var_type = JVMType.from_starlight_type(var.type_annotation or "any")
        
        if var.initializer:
            expr_code = self._generate_expression(var.initializer)
            self.java_code.append(f"{indent}{var_type.java_type} {var.name} = {expr_code};")
        else:
            self.java_code.append(f"{indent}{var_type.java_type} {var.name};")
    
    def _generate_return_statement(self, ret: ReturnStatement, indent: str):
        """生成返回语句"""
        if ret.value:
            expr_code = self._generate_expression(ret.value)
            self.java_code.append(f"{indent}return {expr_code};")
        else:
            self.java_code.append(f"{indent}return;")
    
    def _generate_expression_statement(self, expr_stmt: ExpressionStatement, indent: str):
        """生成表达式语句"""
        expr_code = self._generate_expression(expr_stmt.expression)
        # 只有函数调用和赋值需要分号
        if isinstance(expr_stmt.expression, (Call, BinaryOp)):
            self.java_code.append(f"{indent}{expr_code};")
        else:
            self.java_code.append(f"{indent}{expr_code};")
    
    def _generate_if_statement(self, if_stmt: IfStatement, indent: str):
        """生成 if 语句"""
        condition = self._generate_expression(if_stmt.condition)
        self.java_code.append(f"{indent}if ({condition}) {{")
        
        for stmt in if_stmt.then_branch:
            self._generate_statement(stmt, indent + "    ")
        
        if if_stmt.else_branch:
            self.java_code.append(f"{indent}}} else {{")
            for stmt in if_stmt.else_branch:
                self._generate_statement(stmt, indent + "    ")
        
        self.java_code.append(f"{indent}}}")
    
    def _generate_while_statement(self, while_stmt: WhileStatement, indent: str):
        """生成 while 语句"""
        condition = self._generate_expression(while_stmt.condition)
        self.java_code.append(f"{indent}while ({condition}) {{")
        
        for stmt in while_stmt.body:
            self._generate_statement(stmt, indent + "    ")
        
        self.java_code.append(f"{indent}}}")
    
    def _generate_block_statement(self, block: BlockStatement, indent: str):
        """生成块语句"""
        for stmt in block.statements:
            self._generate_statement(stmt, indent)
    
    def _generate_expression(self, expr: Expression) -> str:
        """生成表达式"""
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, Literal):
            return self._generate_literal(expr)
        elif isinstance(expr, BinaryOp):
            return self._generate_binary_op(expr)
        elif isinstance(expr, UnaryOp):
            return self._generate_unary_op(expr)
        elif isinstance(expr, Call):
            return self._generate_call(expr)
        else:
            return "/* unknown expression */"
    
    def _generate_literal(self, literal: Literal) -> str:
        """生成字面量"""
        if literal.type == "string":
            return f'"{literal.value}"'
        elif literal.type == "boolean":
            return "true" if literal.value else "false"
        elif literal.type == "null":
            return "null"
        else:
            return str(literal.value)
    
    def _generate_binary_op(self, op: BinaryOp) -> str:
        """生成二元操作"""
        left = self._generate_expression(op.left)
        right = self._generate_expression(op.right)
        
        # 操作符映射
        operator_mapping = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>=',
            '&&': '&&',
            '||': '||'
        }
        
        java_op = operator_mapping.get(op.operator, op.operator)
        return f"({left} {java_op} {right})"
    
    def _generate_unary_op(self, op: UnaryOp) -> str:
        """生成一元操作"""
        operand = self._generate_expression(op.operand)
        
        if op.operator == '!':
            return f"!({operand})"
        elif op.operator == '-':
            return f"-({operand})"
        else:
            return f"{op.operator}({operand})"
    
    def _generate_call(self, call: Call) -> str:
        """生成函数调用"""
        callee = self._generate_expression(call.callee)
        args = [self._generate_expression(arg) for arg in call.arguments]
        
        # 处理内置函数
        if isinstance(call.callee, Identifier):
            if call.callee.name == "println":
                return f"System.out.println({', '.join(args)})"
            elif call.callee.name == "print":
                return f"System.out.print({', '.join(args)})"
        
        return f"{callee}({', '.join(args)})"
    
    def _generate_complete_java_code(self) -> str:
        """生成完整的 Java 代码"""
        complete_code = []
        
        # 不添加包声明，简化测试
        # if self.class_name != "Main":
        #     complete_code.append(f"package {self.class_name.lower()};")
        #     complete_code.append("")
        
        # 添加导入语句
        for imp in sorted(self.imports):
            complete_code.append(f"import {imp};")
        
        if self.imports:
            complete_code.append("")
        
        # 添加类代码
        complete_code.extend(self.java_code)
        
        return "\n".join(complete_code)
    
    def save_to_file(self, java_code: str, filename: str = None):
        """保存 Java 代码到文件"""
        if filename is None:
            filename = f"{self.class_name}.java"
        
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(java_code)
        
        return filepath

def generate_jvm_code(program: Program, class_name: str = "Main") -> str:
    """生成 JVM 代码"""
    generator = JVMCodeGenerator()
    return generator.generate(program, class_name)

if __name__ == "__main__":
    # 测试 JVM 后端
    from lexer import Lexer
    from parser import Parser
    from semantic_analyzer import SemanticAnalyzer
    
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, " + name;
    }
    
    func main() {
        let message = greet("World");
        println(message);
    }
    '''
    
    # 词法分析
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    # 语法分析
    parser = Parser(tokens)
    ast = parser.parse()
    
    # 语义分析
    analyzer = SemanticAnalyzer()
    semantic_result = analyzer.analyze(ast)
    
    if semantic_result['success']:
        # 生成 JVM 代码
        generator = JVMCodeGenerator()
        java_code = generator.generate(ast, "HelloWorld")
        
        print("=== 生成的 Java 代码 ===")
        print(java_code)
        
        # 保存到文件
        filepath = generator.save_to_file(java_code, "HelloWorld.java")
        print(f"\n✅ Java 代码已保存到: {filepath}")
    else:
        print("❌ 语义分析失败:")
        for error in semantic_result['errors']:
            print(f"  - {error['message']}")
