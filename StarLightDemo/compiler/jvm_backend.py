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
            elif isinstance(stmt, DataClassDeclaration):
                self._generate_data_class(stmt)
        
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
        
        # 查找 main 函数
        main_function = None
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration) and stmt.name == "main":
                main_function = stmt
                break
        
        if main_function:
            # 生成 main 函数体
            self._generate_function_body(main_function.body, indent="        ")
        else:
            # 如果没有 main 函数，生成其他非函数声明语句
            for stmt in program.statements:
                if not isinstance(stmt, FunctionDeclaration):
                    self._generate_statement(stmt, indent="        ")
        
        self.java_code.append("    }")
        self.java_code.append("")
    
    def _generate_function(self, func: FunctionDeclaration):
        """生成函数"""
        # 生成方法签名
        if func.return_type:
            return_type = JVMType.from_starlight_type(func.return_type)
        else:
            # 推断返回类型
            return_type = self._infer_return_type(func.body)
        
        params = []
        
        for param_name, param_type in func.parameters:
            if param_type:
                jvm_type = JVMType.from_starlight_type(param_type)
            else:
                # 如果没有指定类型，使用 Object
                jvm_type = JVMType.from_starlight_type("any")
            params.append(f"{jvm_type.java_type} {param_name}")
        
        method_signature = f"public static {return_type.java_type} {func.name}({', '.join(params)}) {{"
        self.java_code.append(f"    {method_signature}")
        
        # 生成方法体
        self._generate_function_body(func.body, indent="        ")
        
        self.java_code.append("    }")
        self.java_code.append("")
    
    def _generate_data_class(self, data_class: DataClassDeclaration):
        """生成数据类"""
        # 生成数据类定义
        self.java_code.append(f"    public static class {data_class.name} {{")
        
        # 生成字段
        for field_name, field_type in data_class.fields:
            java_type = JVMType.from_starlight_type(field_type)
            self.java_code.append(f"        public {java_type.java_type} {field_name};")
        
        self.java_code.append("")
        
        # 生成构造函数
        self._generate_data_class_constructor(data_class)
        
        # 生成方法
        for method in data_class.methods:
            self._generate_data_class_method(data_class.name, method)
        
        self.java_code.append("    }")
        self.java_code.append("")
    
    def _generate_data_class_constructor(self, data_class: DataClassDeclaration):
        """生成数据类构造函数"""
        params = []
        assignments = []
        
        for field_name, field_type in data_class.fields:
            java_type = JVMType.from_starlight_type(field_type)
            params.append(f"{java_type.java_type} {field_name}")
            assignments.append(f"        this.{field_name} = {field_name};")
        
        self.java_code.append(f"        public {data_class.name}({', '.join(params)}) {{")
        for assignment in assignments:
            self.java_code.append(assignment)
        self.java_code.append("        }")
        self.java_code.append("")
    
    def _generate_data_class_method(self, class_name: str, method: FunctionDeclaration):
        """生成数据类方法"""
        return_type = JVMType.from_starlight_type(method.return_type or "void")
        params = []
        
        for param_name, param_type in method.parameters:
            jvm_type = JVMType.from_starlight_type(param_type or "any")
            params.append(f"{jvm_type.java_type} {param_name}")
        
        method_signature = f"        public {return_type.java_type} {method.name}({', '.join(params)}) {{"
        self.java_code.append(method_signature)
        
        # 生成方法体
        self._generate_function_body(method.body, indent="            ")
        
        self.java_code.append("        }")
        self.java_code.append("")
    
    def _infer_return_type(self, body: List[Statement]) -> JVMType:
        """推断函数返回类型"""
        for stmt in body:
            if isinstance(stmt, ReturnStatement) and stmt.value:
                # 根据返回值推断类型
                if isinstance(stmt.value, Literal):
                    if stmt.value.type == "string":
                        return JVMType.from_starlight_type("string")
                    elif stmt.value.type == "integer":
                        return JVMType.from_starlight_type("int")
                    elif stmt.value.type == "float":
                        return JVMType.from_starlight_type("float")
                    elif stmt.value.type == "boolean":
                        return JVMType.from_starlight_type("boolean")
                elif isinstance(stmt.value, BinaryOp):
                    # 对于二元操作，根据操作符和操作数推断类型
                    if stmt.value.operator == '+' and self._is_string_operation(stmt.value):
                        # 字符串拼接操作
                        return JVMType.from_starlight_type("string")
                    elif stmt.value.operator in ['+', '-', '*', '/', '%']:
                        # 算术操作，推断为 int
                        return JVMType.from_starlight_type("int")
                    else:
                        # 其他操作，推断为字符串
                        return JVMType.from_starlight_type("string")
                elif isinstance(stmt.value, Call):
                    # 对于函数调用，返回 Object
                    return JVMType.from_starlight_type("any")
        
        # 默认返回 void
        return JVMType.from_starlight_type("void")
    
    def _is_string_operation(self, binary_op: BinaryOp) -> bool:
        """检查是否是字符串操作"""
        # 检查左操作数是否是字符串字面量
        if isinstance(binary_op.left, Literal) and binary_op.left.type == "string":
            return True
        # 检查右操作数是否是字符串字面量
        if isinstance(binary_op.right, Literal) and binary_op.right.type == "string":
            return True
        # 检查是否是字符串变量（只有在明确是字符串操作时才返回 True）
        # 对于算术操作，即使有标识符也不应该是字符串操作
        return False
    
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
        elif isinstance(stmt, MatchStatement):
            self._generate_match_statement(stmt, indent)
        elif isinstance(stmt, FunctionDeclaration):
            # Function declarations are handled separately in _generate_function
            # This should not be called for function declarations in main method
            pass
    
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
    
    def _generate_match_statement(self, match_stmt: MatchStatement, indent: str):
        """生成 match 语句"""
        expression = self._generate_expression(match_stmt.expression)
        
        # 生成 if-else if-else 链
        for i, case in enumerate(match_stmt.cases):
            if i == 0:
                self.java_code.append(f"{indent}if ({self._generate_match_pattern(case.pattern, expression)}) {{")
            else:
                self.java_code.append(f"{indent}}} else if ({self._generate_match_pattern(case.pattern, expression)}) {{")
            
            # 生成 case 体
            for stmt in case.body:
                self._generate_statement(stmt, indent + "    ")
        
        self.java_code.append(f"{indent}}}")
    
    def _generate_match_pattern(self, pattern: Expression, expression: str) -> str:
        """生成模式匹配条件"""
        if isinstance(pattern, Literal):
            # 字面量模式
            pattern_value = self._generate_expression(pattern)
            return f"{expression}.equals({pattern_value})"
        elif isinstance(pattern, Identifier):
            # 变量模式（通配符）
            return "true"
        else:
            # 其他模式，使用 equals
            pattern_value = self._generate_expression(pattern)
            return f"{expression}.equals({pattern_value})"
    
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
        
        # 对于算术操作，添加类型转换
        if op.operator in ['+', '-', '*', '/', '%']:
            # 检查是否需要类型转换（只有在纯算术操作时才转换）
            if self._needs_arithmetic_casting(op.left, op.right):
                left_casted = self._add_arithmetic_casting(op.left)
                right_casted = self._add_arithmetic_casting(op.right)
                return f"({left_casted} {java_op} {right_casted})"
        
        return f"({left} {java_op} {right})"
    
    def _needs_arithmetic_casting(self, left, right) -> bool:
        """检查是否需要算术类型转换"""
        # 只有在纯算术操作时才需要类型转换
        # 检查是否都是数字字面量或标识符
        left_is_numeric = isinstance(left, Literal) and left.type in ['integer', 'float'] or isinstance(left, Identifier)
        right_is_numeric = isinstance(right, Literal) and right.type in ['integer', 'float'] or isinstance(right, Identifier)
        return left_is_numeric and right_is_numeric
    
    def _add_arithmetic_casting(self, expr) -> str:
        """添加算术类型转换"""
        if isinstance(expr, Identifier):
            # 对于标识符，转换为 Integer
            return f"((Integer) {expr.name})"
        elif isinstance(expr, Literal):
            # 对于字面量，直接返回
            return self._generate_expression(expr)
        else:
            # 对于其他表达式，递归处理
            return self._generate_expression(expr)
    
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
