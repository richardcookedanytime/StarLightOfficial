#!/usr/bin/env python3
"""
Starlight 编程语言 - 语法分析器
负责将 Token 序列解析为抽象语法树 (AST)
"""

from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .lexer import Token, TokenType, Lexer

# AST 节点基类
class ASTNode(ABC):
    pass

# 表达式节点
@dataclass
class Expression(ASTNode):
    pass

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class Literal(Expression):
    value: Any
    type: str

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class Call(Expression):
    callee: Expression
    arguments: List[Expression]

@dataclass
class MemberAccess(Expression):
    object: Expression
    property: str

@dataclass
class ArrayLiteral(Expression):
    elements: List[Expression]

@dataclass
class ObjectLiteral(Expression):
    properties: Dict[str, Expression]

@dataclass
class Conditional(Expression):
    condition: Expression
    then_expr: Expression
    else_expr: Expression

@dataclass
class Lambda(Expression):
    parameters: List[tuple[str, Optional[str]]]  # (name, type)
    body: Union[Expression, List['Statement']]
    return_type: Optional[str]

# 语句节点
@dataclass
class Statement(ASTNode):
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class VariableDeclaration(Statement):
    name: str
    type_annotation: Optional[str]
    initializer: Optional[Expression]
    is_const: bool

@dataclass
class FunctionDeclaration(Statement):
    name: str
    parameters: List[tuple[str, Optional[str]]]  # (name, type)
    return_type: Optional[str]
    body: List[Statement]
    is_async: bool

@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: List[Statement]
    else_branch: Optional[List[Statement]]

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class ForStatement(Statement):
    initializer: Optional[Statement]
    condition: Optional[Expression]
    increment: Optional[Expression]
    body: List[Statement]

@dataclass
class MatchStatement(Statement):
    expression: Expression
    cases: List['MatchCase']

@dataclass
class MatchCase(ASTNode):
    pattern: Expression
    body: List[Statement]

@dataclass
class BlockStatement(Statement):
    statements: List[Statement]

# 类型声明
@dataclass
class StructDeclaration(Statement):
    name: str
    fields: List[tuple[str, str]]  # (name, type)

@dataclass
class DataClassDeclaration(Statement):
    name: str
    fields: List[tuple[str, str]]  # (name, type)
    methods: List[FunctionDeclaration]

@dataclass
class EnumDeclaration(Statement):
    name: str
    variants: List[tuple[str, Optional[str]]]  # (name, type)

@dataclass
class InterfaceDeclaration(Statement):
    name: str
    methods: List[FunctionDeclaration]

@dataclass
class TypeAlias(Statement):
    name: str
    type_expression: str

# Actor 声明
@dataclass
class ActorDeclaration(Statement):
    name: str
    state_fields: List[tuple[str, str]]  # (name, type)
    message_handlers: List['MessageHandler']

@dataclass
class MessageHandler(Statement):
    message_type: str
    parameters: List[tuple[str, str]]  # (name, type)
    body: List[Statement]

@dataclass
class SpawnExpression(Expression):
    actor_type: str
    arguments: List[Expression]

@dataclass
class SendExpression(Expression):
    actor: Expression
    message_type: str
    arguments: List[Expression]

# 程序根节点
@dataclass
class Program(ASTNode):
    statements: List[Statement]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> Program:
        """解析整个程序"""
        statements = []
        
        while not self._is_at_end():
            if self._match(TokenType.SEMICOLON):
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            
            self._consume_newlines()
        
        return Program(statements)
    
    def _is_at_end(self) -> bool:
        """检查是否到达文件末尾"""
        return self.current_token.type == TokenType.EOF
    
    def _advance(self) -> Token:
        """前进到下一个 token"""
        if not self._is_at_end():
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        return self.tokens[self.position - 1] if self.position > 0 else None
    
    def _match(self, *token_types: TokenType) -> bool:
        """检查当前 token 是否匹配给定类型"""
        if self.current_token and self.current_token.type in token_types:
            self._advance()
            return True
        return False
    
    def _consume(self, token_type: TokenType, message: str = None) -> Token:
        """消费指定类型的 token"""
        if self.current_token and self.current_token.type == token_type:
            return self._advance()
        
        error_msg = message or f"Expected {token_type.value}"
        raise SyntaxError(f"{error_msg} at line {self.current_token.line}")
    
    def _consume_newlines(self):
        """消费换行符"""
        while self._match(TokenType.NEWLINE):
            pass
    
    def _parse_statement(self) -> Optional[Statement]:
        """解析语句"""
        if self._match(TokenType.FUNC):
            return self._parse_function_declaration()
        elif self._match(TokenType.LET, TokenType.CONST):
            return self._parse_variable_declaration()
        elif self._match(TokenType.STRUCT):
            return self._parse_struct_declaration()
        elif self._match(TokenType.DATA):
            return self._parse_data_class_declaration()
        elif self._match(TokenType.ENUM):
            return self._parse_enum_declaration()
        elif self._match(TokenType.INTERFACE):
            return self._parse_interface_declaration()
        elif self._match(TokenType.TYPE):
            return self._parse_type_alias()
        elif self._match(TokenType.ACTOR):
            return self._parse_actor_declaration()
        elif self._match(TokenType.IF):
            return self._parse_if_statement()
        elif self._match(TokenType.WHILE):
            return self._parse_while_statement()
        elif self._match(TokenType.FOR):
            return self._parse_for_statement()
        elif self._match(TokenType.RETURN):
            return self._parse_return_statement()
        elif self._match(TokenType.MATCH):
            return self._parse_match_statement()
        elif self._match(TokenType.LEFT_BRACE):
            return self._parse_block_statement()
        else:
            # 尝试解析表达式语句
            expr = self._parse_expression()
            if expr:
                # 分号是可选的
                self._match(TokenType.SEMICOLON)
                return ExpressionStatement(expr)
        
        return None
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """解析函数声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected function name").value
        
        # 解析参数
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        parameters = []
        
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                param_type = None
                
                if self._match(TokenType.COLON):
                    param_type = self._consume(TokenType.IDENTIFIER, "Expected parameter type").value
                
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        
        # 解析返回类型
        return_type = None
        if self._match(TokenType.ARROW):
            return_type = self._consume(TokenType.IDENTIFIER, "Expected return type").value
        
        # 解析函数体
        if self._match(TokenType.ASSIGN):
            # 单行函数体
            expr = self._parse_expression()
            body = [ReturnStatement(expr)]
        else:
            # 多行函数体
            self._consume(TokenType.LEFT_BRACE, "Expected '{' before function body")
            body = self._parse_block_statements()
            self._consume(TokenType.RIGHT_BRACE, "Expected '}' after function body")
        
        return FunctionDeclaration(name, parameters, return_type, body, False)
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """解析变量声明"""
        is_const = self.tokens[self.position - 1].type == TokenType.CONST
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        type_annotation = None
        if self._match(TokenType.COLON):
            type_annotation = self._consume(TokenType.IDENTIFIER, "Expected type annotation").value
        
        initializer = None
        if self._match(TokenType.ASSIGN):
            # 检查是否为箭头函数
            if self._check(TokenType.LEFT_PAREN):
                initializer = self._parse_arrow_function()
            else:
                initializer = self._parse_expression()
        
        # 分号是可选的
        self._match(TokenType.SEMICOLON)
        
        return VariableDeclaration(name, type_annotation, initializer, is_const)
    
    def _parse_arrow_function(self) -> Expression:
        """解析箭头函数"""
        # 解析参数列表
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after arrow function")
        parameters = []
        
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                param_type = None
                
                if self._match(TokenType.COLON):
                    param_type = self._consume(TokenType.IDENTIFIER, "Expected parameter type").value
                
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        
        # 解析返回类型
        return_type = None
        if self._match(TokenType.ARROW):
            return_type = self._consume(TokenType.IDENTIFIER, "Expected return type").value
        
        # 解析函数体
        if self._match(TokenType.FAT_ARROW):
            # 简单表达式体
            body_expr = self._parse_expression()
            # 创建一个简单的函数表达式（这里简化处理）
            return body_expr
        else:
            # 块体
            self._consume(TokenType.LEFT_BRACE, "Expected '{' or '=>' in arrow function")
            body = self._parse_block_statements()
            self._consume(TokenType.RIGHT_BRACE, "Expected '}' after arrow function body")
            # 这里应该创建一个函数表达式，暂时简化
            return Identifier("arrow_function")
    
    def _parse_struct_declaration(self) -> StructDeclaration:
        """解析结构体声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected struct name").value
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before struct body")
        
        fields = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            field_name = self._consume(TokenType.IDENTIFIER, "Expected field name").value
            self._consume(TokenType.COLON, "Expected ':' after field name")
            field_type = self._consume(TokenType.IDENTIFIER, "Expected field type").value
            fields.append((field_name, field_type))
            
            self._match(TokenType.COMMA)
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after struct body")
        
        return StructDeclaration(name, fields)
    
    def _parse_data_class_declaration(self) -> DataClassDeclaration:
        """解析数据类声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected data class name").value
        
        # 解析字段列表
        fields = []
        if self._match(TokenType.LEFT_PAREN):
            while not self._check(TokenType.RIGHT_PAREN) and not self._is_at_end():
                field_name = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                self._consume(TokenType.COLON, "Expected ':' after field name")
                field_type = self._consume(TokenType.IDENTIFIER, "Expected field type").value
                fields.append((field_name, field_type))
                
                if not self._match(TokenType.COMMA):
                    break
            
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after field list")
        
        # 解析方法体
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before data class body")
        
        methods = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.FUNC):
                method = self._parse_data_class_method()
                methods.append(method)
            else:
                # 跳过其他语句
                self._advance()
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after data class body")
        
        return DataClassDeclaration(name, fields, methods)
    
    def _parse_data_class_method(self) -> FunctionDeclaration:
        """解析数据类方法"""
        name = self._consume(TokenType.IDENTIFIER, "Expected method name").value
        
        # 解析参数
        parameters = []
        if self._match(TokenType.LEFT_PAREN):
            while not self._check(TokenType.RIGHT_PAREN) and not self._is_at_end():
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                self._consume(TokenType.COLON, "Expected ':' after parameter name")
                param_type = self._consume(TokenType.IDENTIFIER, "Expected parameter type").value
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
            
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        
        # 解析返回类型
        return_type = None
        if self._match(TokenType.COLON):
            return_type = self._consume(TokenType.IDENTIFIER, "Expected return type").value
        
        # 解析方法体
        if self._match(TokenType.ASSIGN):
            # 单行方法体
            expr = self._parse_expression()
            # 单行方法体不需要分号
            body = [ReturnStatement(expr)]
        else:
            # 多行方法体
            self._consume(TokenType.LEFT_BRACE, "Expected '{' before method body")
            body = []
            while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    body.append(stmt)
            self._consume(TokenType.RIGHT_BRACE, "Expected '}' after method body")
        
        return FunctionDeclaration(name, parameters, return_type, body, False)
    
    def _parse_enum_declaration(self) -> EnumDeclaration:
        """解析枚举声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected enum name").value
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before enum body")
        
        variants = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            variant_name = self._consume(TokenType.IDENTIFIER, "Expected variant name").value
            variant_type = None
            
            if self._match(TokenType.LEFT_PAREN):
                variant_type = self._consume(TokenType.IDENTIFIER, "Expected variant type").value
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after variant type")
            
            variants.append((variant_name, variant_type))
            
            if not self._match(TokenType.COMMA):
                break
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after enum body")
        
        return EnumDeclaration(name, variants)
    
    def _parse_interface_declaration(self) -> InterfaceDeclaration:
        """解析接口声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected interface name").value
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before interface body")
        
        methods = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            method = self._parse_function_declaration()
            methods.append(method)
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after interface body")
        
        return InterfaceDeclaration(name, methods)
    
    def _parse_type_alias(self) -> TypeAlias:
        """解析类型别名"""
        name = self._consume(TokenType.IDENTIFIER, "Expected type alias name").value
        self._consume(TokenType.ASSIGN, "Expected '=' in type alias")
        
        type_expr = ""
        while not self._check(TokenType.SEMICOLON) and not self._is_at_end():
            type_expr += self.current_token.value
            self._advance()
        
        self._consume(TokenType.SEMICOLON, "Expected ';' after type alias")
        
        return TypeAlias(name, type_expr)
    
    def _parse_actor_declaration(self) -> ActorDeclaration:
        """解析 Actor 声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected actor name").value
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before actor body")
        
        state_fields = []
        message_handlers = []
        
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.RECEIVE):
                handler = self._parse_message_handler()
                message_handlers.append(handler)
            else:
                # 状态字段声明
                field_name = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                self._consume(TokenType.COLON, "Expected ':' after field name")
                field_type = self._consume(TokenType.IDENTIFIER, "Expected field type").value
                self._consume(TokenType.SEMICOLON, "Expected ';' after field declaration")
                state_fields.append((field_name, field_type))
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after actor body")
        
        return ActorDeclaration(name, state_fields, message_handlers)
    
    def _parse_message_handler(self) -> MessageHandler:
        """解析消息处理器"""
        message_type = self._consume(TokenType.IDENTIFIER, "Expected message type").value
        
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after message type")
        
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                param_type = self._consume(TokenType.IDENTIFIER, "Expected parameter type").value
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before message handler body")
        body = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after message handler body")
        
        return MessageHandler(message_type, parameters, body)
    
    def _parse_if_statement(self) -> IfStatement:
        """解析 if 语句"""
        condition = self._parse_expression()
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before if body")
        then_branch = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after if body")
        
        else_branch = None
        if self._match(TokenType.ELSE):
            self._consume(TokenType.LEFT_BRACE, "Expected '{' before else body")
            else_branch = self._parse_block_statements()
            self._consume(TokenType.RIGHT_BRACE, "Expected '}' after else body")
        
        return IfStatement(condition, then_branch, else_branch)
    
    def _parse_while_statement(self) -> WhileStatement:
        """解析 while 语句"""
        condition = self._parse_expression()
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before while body")
        body = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after while body")
        
        return WhileStatement(condition, body)
    
    def _parse_for_statement(self) -> ForStatement:
        """解析 for 语句"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after for")
        
        initializer = None
        if not self._check(TokenType.SEMICOLON):
            initializer = self._parse_statement()
        
        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._parse_expression()
        
        self._consume(TokenType.SEMICOLON, "Expected ';' after loop condition")
        
        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._parse_expression()
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses")
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before for body")
        body = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after for body")
        
        return ForStatement(initializer, condition, increment, body)
    
    def _parse_return_statement(self) -> ReturnStatement:
        """解析 return 语句"""
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._parse_expression()
        
        # 分号是可选的
        self._match(TokenType.SEMICOLON)
        
        return ReturnStatement(value)
    
    def _parse_match_statement(self) -> MatchStatement:
        """解析 match 语句"""
        expression = self._parse_expression()
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before match body")
        
        cases = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            # 跳过换行符
            self._consume_newlines()
            pattern = self._parse_expression()
            self._consume(TokenType.FAT_ARROW, "Expected '=>' after match pattern")
            
            # 检查是否是单行表达式还是块
            if self._check(TokenType.LEFT_BRACE):
                # 块体
                self._consume(TokenType.LEFT_BRACE, "Expected '{' before case body")
                body = self._parse_block_statements()
                self._consume(TokenType.RIGHT_BRACE, "Expected '}' after case body")
            else:
                # 单行表达式
                expr = self._parse_expression()
                body = [ExpressionStatement(expr)]
            
            cases.append(MatchCase(pattern, body))
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after match body")
        
        return MatchStatement(expression, cases)
    
    def _parse_block_statement(self) -> BlockStatement:
        """解析块语句"""
        statements = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        
        return BlockStatement(statements)
    
    def _parse_block_statements(self) -> List[Statement]:
        """解析块中的语句列表"""
        statements = []
        
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.SEMICOLON):
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            
            self._consume_newlines()
        
        return statements
    
    def _parse_expression(self) -> Optional[Expression]:
        """解析表达式"""
        return self._parse_assignment()
    
    def _parse_assignment(self) -> Optional[Expression]:
        """解析赋值表达式"""
        expr = self._parse_conditional()
        
        if self._match(TokenType.ASSIGN):
            value = self._parse_assignment()
            # 这里应该创建一个赋值表达式节点
            # 为了简化，暂时返回条件表达式
            return expr
        
        return expr
    
    def _parse_conditional(self) -> Optional[Expression]:
        """解析条件表达式"""
        expr = self._parse_logical_or()
        
        if self._match(TokenType.QUESTION):
            then_expr = self._parse_expression()
            self._consume(TokenType.COLON, "Expected ':' in conditional expression")
            else_expr = self._parse_conditional()
            
            return Conditional(expr, then_expr, else_expr)
        
        return expr
    
    def _parse_logical_or(self) -> Optional[Expression]:
        """解析逻辑或表达式"""
        expr = self._parse_logical_and()
        
        while self._match(TokenType.OR):
            operator = self.tokens[self.position - 1].value
            right = self._parse_logical_and()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_logical_and(self) -> Optional[Expression]:
        """解析逻辑与表达式"""
        expr = self._parse_equality()
        
        while self._match(TokenType.AND):
            operator = self.tokens[self.position - 1].value
            right = self._parse_equality()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_equality(self) -> Optional[Expression]:
        """解析相等性表达式"""
        expr = self._parse_comparison()
        
        while self._match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.tokens[self.position - 1].value
            right = self._parse_comparison()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_comparison(self) -> Optional[Expression]:
        """解析比较表达式"""
        expr = self._parse_term()
        
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, 
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.tokens[self.position - 1].value
            right = self._parse_term()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_term(self) -> Optional[Expression]:
        """解析加减表达式"""
        expr = self._parse_factor()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self.tokens[self.position - 1].value
            right = self._parse_factor()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_factor(self) -> Optional[Expression]:
        """解析乘除表达式"""
        expr = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.tokens[self.position - 1].value
            right = self._parse_unary()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_unary(self) -> Optional[Expression]:
        """解析一元表达式"""
        if self._match(TokenType.NOT, TokenType.MINUS):
            operator = self.tokens[self.position - 1].value
            right = self._parse_unary()
            return UnaryOp(operator, right)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Optional[Expression]:
        """解析基本表达式"""
        if self._match(TokenType.BOOLEAN) and self.tokens[self.position - 1].value == "true":
            return Literal(True, "boolean")
        if self._match(TokenType.BOOLEAN) and self.tokens[self.position - 1].value == "false":
            return Literal(False, "boolean")
        if self._match(TokenType.BOOLEAN) and self.tokens[self.position - 1].value == "null":
            return Literal(None, "null")
        
        if self._match(TokenType.INTEGER):
            return Literal(int(self.tokens[self.position - 1].value), "integer")
        if self._match(TokenType.FLOAT):
            return Literal(float(self.tokens[self.position - 1].value), "float")
        if self._match(TokenType.STRING):
            return Literal(self.tokens[self.position - 1].value, "string")
        
        if self._match(TokenType.IDENTIFIER):
            ident = Identifier(self.tokens[self.position - 1].value)
            
            # 检查是否为函数调用
            if self._check(TokenType.LEFT_PAREN):
                return self._parse_call_with_identifier(ident)
            
            return ident
        
        if self._match(TokenType.LEFT_PAREN):
            # 可能是 Lambda 表达式或括号表达式
            # 先检查是否是 Lambda: (params) => expr
            saved_pos = self.position
            
            # 尝试解析参数列表
            params = []
            is_lambda = False
            
            if not self._check(TokenType.RIGHT_PAREN):
                # 尝试解析参数
                param_name = None
                if self._match(TokenType.IDENTIFIER):
                    param_name = self.tokens[self.position - 1].value
                    
                    # 检查是否有类型注解
                    param_type = None
                    if self._match(TokenType.COLON):
                        if self._match(TokenType.IDENTIFIER):
                            param_type = self.tokens[self.position - 1].value
                    
                    params.append((param_name, param_type))
                    
                    # 检查是否有更多参数
                    while self._match(TokenType.COMMA):
                        param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                        param_type = None
                        if self._match(TokenType.COLON):
                            param_type = self._consume(TokenType.IDENTIFIER, "Expected parameter type").value
                        params.append((param_name, param_type))
            
            if self._match(TokenType.RIGHT_PAREN):
                # 检查是否有 => 符号
                if self._match(TokenType.FAT_ARROW):
                    is_lambda = True
            
            if is_lambda:
                # 解析 Lambda 体
                return_type = None
                
                # 解析 Lambda 体（可以是表达式或块）
                if self._check(TokenType.LEFT_BRACE):
                    self._consume(TokenType.LEFT_BRACE, "Expected '{'")
                    body = self._parse_block_statements()
                    self._consume(TokenType.RIGHT_BRACE, "Expected '}'")
                else:
                    # 单行表达式
                    body = self._parse_expression()
                
                return Lambda(params, body, return_type)
            else:
                # 不是 Lambda，回退并解析普通括号表达式
                self.position = saved_pos
                expr = self._parse_expression()
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
                return expr
        
        return None
    
    def _parse_call_with_identifier(self, callee: Identifier) -> Call:
        """解析函数调用"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                arg = self._parse_expression()
                if arg:
                    arguments.append(arg)
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
        
        return Call(callee, arguments)
    
    def _check(self, token_type: TokenType) -> bool:
        """检查当前 token 类型"""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type

def parse_file(filename: str) -> Program:
    """从文件解析 Starlight 程序"""
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    return parser.parse()

if __name__ == "__main__":
    # 测试语法分析器
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, ${name}!";
    }
    
    let message = greet("World");
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("AST parsed successfully!")
    print(f"Found {len(ast.statements)} statements")
