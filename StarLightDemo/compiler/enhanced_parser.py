#!/usr/bin/env python3
"""
Starlight 编程语言 - 增强语法分析器
支持语法糖、逻辑化扩展和声明式编程
"""

from typing import List, Optional, Union, Dict, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from parser import *
from lexer import TokenType

# 增强的 AST 节点
@dataclass
class DataClassDeclaration(Statement):
    name: str
    type_parameters: List[str]
    fields: List[Tuple[str, str]]
    methods: List[FunctionDeclaration]

@dataclass
class RuleDeclaration(Statement):
    condition: Expression
    action: Expression
    name: Optional[str] = None

@dataclass
class RuleBlock(Statement):
    rules: List[RuleDeclaration]

@dataclass
class ExtensionDeclaration(Statement):
    target_type: str
    functions: List[FunctionDeclaration]

@dataclass
class TransactionBlock(Statement):
    statements: List[Statement]

@dataclass
class ListComprehension(Expression):
    expression: Expression
    generators: List['ComprehensionGenerator']

@dataclass
class ComprehensionGenerator:
    variable: str
    iterable: Expression
    condition: Optional[Expression] = None

@dataclass
class PipeExpression(Expression):
    left: Expression
    right: Expression

@dataclass
class YieldExpression(Expression):
    expression: Expression

@dataclass
class VersionDeclaration(Statement):
    version: str
    package: Optional[str] = None

@dataclass
class FeatureDeclaration(Statement):
    name: str
    enabled: bool

@dataclass
class ExpectActualDeclaration(Statement):
    name: str
    is_expect: bool
    signature: FunctionDeclaration

class EnhancedParser(Parser):
    """增强语法分析器，支持 Starlight 的所有特性"""
    
    def __init__(self, tokens: List[Token]):
        super().__init__(tokens)
    
    def _parse_data_class_declaration(self) -> DataClassDeclaration:
        """解析数据类声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected class name").value
        
        # 解析类型参数
        type_parameters = []
        if self._match(TokenType.LESS):
            while not self._check(TokenType.GREATER):
                param_name = self._consume(TokenType.IDENTIFIER, "Expected type parameter name").value
                type_parameters.append(param_name)
                
                if not self._match(TokenType.COMMA):
                    break
            self._consume(TokenType.GREATER, "Expected '>' after type parameters")
        
        # 解析字段列表
        fields = []
        methods = []
        
        if self._match(TokenType.LEFT_PAREN):
            # 主构造函数参数
            if not self._check(TokenType.RIGHT_PAREN):
                while True:
                    field_name = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                    self._consume(TokenType.COLON, "Expected ':' after field name")
                    field_type = self._parse_type_expression()
                    fields.append((field_name, str(field_type) if field_type else "any"))
                    
                    if not self._match(TokenType.COMMA):
                        break
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after field list")
        
        # 解析类体
        if self._match(TokenType.LEFT_BRACE):
            while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
                if self._check(TokenType.FUNC):
                    self._advance()  # consume 'func'
                    method = self._parse_function_declaration()
                    methods.append(method)
                else:
                    # 字段声明
                    field_name = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                    self._consume(TokenType.COLON, "Expected ':' after field name")
                    field_type = self._parse_type_expression()
                    self._consume(TokenType.SEMICOLON, "Expected ';' after field declaration")
                    
                    fields.append((field_name, str(field_type) if field_type else "any"))
            
            self._consume(TokenType.RIGHT_BRACE, "Expected '}' after class body")
        
        return DataClassDeclaration(name, type_parameters, fields, methods)
    
    def _parse_rule_declaration(self) -> RuleDeclaration:
        """解析规则声明"""
        condition = self._parse_expression()
        self._consume(TokenType.FAT_ARROW, "Expected '=>' after rule condition")
        action = self._parse_expression()
        
        return RuleDeclaration(condition, action)
    
    def _parse_rule_block(self) -> RuleBlock:
        """解析规则块"""
        self._consume(TokenType.LEFT_BRACE, "Expected '{' after 'rule'")
        
        rules = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            rule = self._parse_rule_declaration()
            rules.append(rule)
            
            if not self._match(TokenType.COMMA):
                break
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after rule block")
        
        return RuleBlock(rules)
    
    def _parse_extension_declaration(self) -> ExtensionDeclaration:
        """解析扩展声明"""
        target_type = self._consume(TokenType.IDENTIFIER, "Expected target type name").value
        self._consume(TokenType.LEFT_BRACE, "Expected '{' after target type")
        
        functions = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.FUNC):
                func = self._parse_function_declaration()
                functions.append(func)
            else:
                break
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after extension body")
        
        return ExtensionDeclaration(target_type, functions)
    
    def _parse_transaction_block(self) -> TransactionBlock:
        """解析事务块"""
        self._consume(TokenType.LEFT_BRACE, "Expected '{' after 'transaction'")
        
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after transaction block")
        
        return TransactionBlock(statements)
    
    def _parse_list_comprehension(self) -> ListComprehension:
        """解析列表推导式"""
        self._consume(TokenType.LEFT_BRACKET, "Expected '[' in list comprehension")
        
        expression = self._parse_expression()
        self._consume(TokenType.PIPE, "Expected '|' after expression")
        
        generators = []
        while self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "for":
            self._advance()  # consume 'for'
            
            variable = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
            # 检查 'in' 关键字
            if not (self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "in"):
                raise Exception("Expected 'in' in list comprehension")
            self._advance()  # consume 'in'
            
            iterable = self._parse_expression()
            
            # 可选的条件
            condition = None
            if self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "if":
                self._advance()  # consume 'if'
                condition = self._parse_expression()
            
            generators.append(ComprehensionGenerator(variable, iterable, condition))
        
        self._consume(TokenType.RIGHT_BRACKET, "Expected ']' in list comprehension")
        
        return ListComprehension(expression, generators)
    
    def _parse_type_expression(self) -> Optional[Expression]:
        """解析类型表达式"""
        if self._check(TokenType.IDENTIFIER):
            type_name = self._consume(TokenType.IDENTIFIER, "Expected type name").value
            return Identifier(type_name)
        return None
    
    def _parse_pipe_expression(self) -> PipeExpression:
        """解析管道表达式"""
        left = self._parse_expression()
        self._consume(TokenType.PIPE, "Expected '|' in pipe expression")
        right = self._parse_expression()
        
        return PipeExpression(left, right)
    
    def _parse_yield_expression(self) -> YieldExpression:
        """解析 yield 表达式"""
        expression = self._parse_expression()
        return YieldExpression(expression)
    
    def _parse_version_declaration(self) -> VersionDeclaration:
        """解析版本声明"""
        version = self._consume(TokenType.STRING, "Expected version string").value
        package = None
        
        if self._match(TokenType.IDENTIFIER) and self.tokens[self.position - 1].value == "package":
            package = self._consume(TokenType.STRING, "Expected package string").value
        
        return VersionDeclaration(version, package)
    
    def _parse_feature_declaration(self) -> FeatureDeclaration:
        """解析特性声明"""
        name = self._consume(TokenType.STRING, "Expected feature name").value
        enabled = True
        
        if self._match(TokenType.COMMA):
            if self._match(TokenType.IDENTIFIER) and self.tokens[self.position - 1].value == "enabled":
                if self._match(TokenType.IDENTIFIER) and self.tokens[self.position - 1].value == "true":
                    enabled = True
                elif self._match(TokenType.IDENTIFIER) and self.tokens[self.position - 1].value == "false":
                    enabled = False
        
        return FeatureDeclaration(name, enabled)
    
    def _parse_expect_actual_declaration(self) -> ExpectActualDeclaration:
        """解析 expect/actual 声明"""
        is_expect = self.tokens[self.position - 1].type == TokenType.EXPECT
        
        if self._match(TokenType.FUNC):
            signature = self._parse_function_declaration()
            return ExpectActualDeclaration(signature.name, is_expect, signature)
        else:
            raise Exception("Expected function declaration after expect/actual")
    
    def _parse_expression(self) -> Optional[Expression]:
        """重写表达式解析，支持更多特性"""
        # 先解析基础表达式
        expr = super()._parse_expression()
        
        # 检查是否后跟管道操作符
        if expr and self._match(TokenType.PIPE):
            right_expr = self._parse_expression()
            if right_expr:
                return PipeExpression(expr, right_expr)
        
        # 检查列表推导式
        if self._check(TokenType.LEFT_BRACKET):
            saved_position = self.position
            try:
                # 检查是否为列表推导式（包含 | 符号）
                temp_pos = self.position + 1  # 跳过 [
                while temp_pos < len(self.tokens) and self.tokens[temp_pos].type != TokenType.RIGHT_BRACKET:
                    if self.tokens[temp_pos].type == TokenType.PIPE:
                        return self._parse_list_comprehension()
                    temp_pos += 1
                
                # 不是列表推导式，回退到普通表达式
                self.position = saved_position
                return super()._parse_expression()
            except:
                self.position = saved_position
                return super()._parse_expression()
        
        # 检查 yield 表达式
        if self._match(TokenType.YIELD):
            return self._parse_yield_expression()
        
        return expr
    
    def _parse_statement(self) -> Optional[Statement]:
        """重写语句解析，支持更多特性"""
        # 检查数据类声明
        if self._match(TokenType.DATA):
            return self._parse_data_class_declaration()
        
        # 检查规则声明
        if self._match(TokenType.RULE):
            return self._parse_rule_block()
        
        # 检查扩展声明
        if self._match(TokenType.EXTEND):
            return self._parse_extension_declaration()
        
        # 检查事务块
        if self._match(TokenType.TRANSACTION):
            return self._parse_transaction_block()
        
        # 检查版本声明
        if self._check(TokenType.AT) and self.position + 1 < len(self.tokens):
            if self.tokens[self.position + 1].type == TokenType.VERSION:
                self._advance()  # consume '@'
                self._advance()  # consume 'version'
                return self._parse_version_declaration()
            elif self.tokens[self.position + 1].type == TokenType.FEATURE:
                self._advance()  # consume '@'
                self._advance()  # consume 'feature'
                return self._parse_feature_declaration()
        
        # 检查 expect/actual 声明
        if self._match(TokenType.EXPECT) or self._match(TokenType.ACTUAL):
            return self._parse_expect_actual_declaration()
        
        return super()._parse_statement()

def parse_enhanced_program(tokens: List[Token]) -> Program:
    """解析增强程序"""
    parser = EnhancedParser(tokens)
    return parser.parse()

if __name__ == "__main__":
    # 测试增强解析器
    from lexer import Lexer
    
    test_code = '''
    @version("1.0")
    @feature("rules", enabled=true)
    
    data User(name: string, age: int) {
        fun isAdult(): boolean = age >= 18
    }
    
    rule adult(User.age >= 18) => User.canVote = true
    
    extend String {
        fun isEmail(): boolean = this.contains("@")
    }
    
    transaction {
        account1 -= 100
        account2 += 100
    }
    
    fun processUsers(): [string] {
        return [user.name | for user in users if user.age > 18]
    }
    
    fun main() {
        val user = User("Alice", 25)
        val names = processUsers()
        println(names)
    }
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = EnhancedParser(tokens)
    ast = parser.parse()
    
    print("=== 增强语法解析结果 ===")
    print(f"解析出 {len(ast.statements)} 个语句")
    
    for i, stmt in enumerate(ast.statements):
        print(f"语句 {i}: {type(stmt).__name__}")
        if hasattr(stmt, 'name'):
            print(f"  名称: {stmt.name}")
        if hasattr(stmt, 'type_parameters'):
            print(f"  类型参数: {stmt.type_parameters}")
