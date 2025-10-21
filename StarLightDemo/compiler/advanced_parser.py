#!/usr/bin/env python3
"""
Starlight 编程语言 - 高级语法分析器
支持泛型、异步、模式匹配等高级特性
"""

from typing import List, Optional, Union, Dict, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from parser import *
from lexer import TokenType

# 扩展的 AST 节点
@dataclass
class GenericType(Expression):
    name: str
    type_arguments: List[Expression]

@dataclass
class AsyncFunctionDeclaration(FunctionDeclaration):
    is_async: bool = True

@dataclass
class AwaitExpression(Expression):
    expression: Expression

@dataclass
class PromiseType(Expression):
    inner_type: Expression

@dataclass
class PatternMatch(Expression):
    expression: Expression
    patterns: List['PatternCase']

@dataclass
class PatternCase:
    pattern: Expression
    guard: Optional[Expression] = None
    body: Expression = None

@dataclass
class DestructuringAssignment(Expression):
    pattern: Expression
    value: Expression

@dataclass
class ListComprehension(Expression):
    expression: Expression
    generator: List['ComprehensionClause']

@dataclass
class ComprehensionClause:
    variable: str
    iterable: Expression
    condition: Optional[Expression] = None

@dataclass
class LambdaExpression(Expression):
    parameters: List[Tuple[str, Optional[str]]]
    body: Expression
    is_async: bool = False

@dataclass
class ExtensionFunction(FunctionDeclaration):
    receiver_type: str

@dataclass
class DataClassDeclaration(Statement):
    name: str
    type_parameters: List[str]
    fields: List[Tuple[str, str]]
    methods: List[FunctionDeclaration]

@dataclass
class InterfaceDeclaration(Statement):
    name: str
    type_parameters: List[str]
    methods: List[FunctionDeclaration]

class AdvancedParser(Parser):
    """高级语法分析器，支持更多语言特性"""
    
    def __init__(self, tokens: List[Token]):
        super().__init__(tokens)
    
    def _parse_generic_type(self) -> Optional[GenericType]:
        """解析泛型类型"""
        if not self._check(TokenType.IDENTIFIER):
            return None
        
        name = self._consume(TokenType.IDENTIFIER, "Expected type name").value
        
        if not self._match(TokenType.LESS):
            return GenericType(name, [])
        
        type_arguments = []
        while not self._check(TokenType.GREATER):
            arg_type = self._parse_type_expression()
            if arg_type:
                type_arguments.append(arg_type)
            
            if not self._match(TokenType.COMMA):
                break
        
        self._consume(TokenType.GREATER, "Expected '>' after type arguments")
        
        return GenericType(name, type_arguments)
    
    def _parse_type_expression(self) -> Optional[Expression]:
        """解析类型表达式"""
        if self._match(TokenType.LEFT_PAREN):
            # 函数类型 (T1, T2) -> T3
            param_types = []
            if not self._check(TokenType.RIGHT_PAREN):
                while True:
                    param_type = self._parse_type_expression()
                    if param_type:
                        param_types.append(param_type)
                    
                    if not self._match(TokenType.COMMA):
                        break
            
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameter types")
            self._consume(TokenType.ARROW, "Expected '->' in function type")
            
            return_type = self._parse_type_expression()
            return GenericType("Function", [GenericType("Tuple", param_types), return_type])
        
        elif self._check(TokenType.IDENTIFIER):
            # 基本类型或泛型类型
            return self._parse_generic_type()
        
        return None
    
    def _parse_async_function_declaration(self) -> AsyncFunctionDeclaration:
        """解析异步函数声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected function name").value
        
        # 解析泛型参数
        type_parameters = []
        if self._match(TokenType.LESS):
            while not self._check(TokenType.GREATER):
                param_name = self._consume(TokenType.IDENTIFIER, "Expected type parameter name").value
                type_parameters.append(param_name)
                
                if not self._match(TokenType.COMMA):
                    break
            self._consume(TokenType.GREATER, "Expected '>' after type parameters")
        
        # 解析参数
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        parameters = []
        
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                param_type = None
                
                if self._match(TokenType.COLON):
                    param_type = self._parse_type_expression()
                
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        
        # 解析返回类型
        return_type = None
        if self._match(TokenType.ARROW):
            return_type = self._parse_type_expression()
        
        # 解析函数体
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before function body")
        body = self._parse_block_statements()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after function body")
        
        return AsyncFunctionDeclaration(name, parameters, return_type, body, True)
    
    def _parse_await_expression(self) -> AwaitExpression:
        """解析 await 表达式"""
        expr = self._parse_expression()
        return AwaitExpression(expr)
    
    def _parse_pattern_match(self) -> PatternMatch:
        """解析模式匹配"""
        expression = self._parse_expression()
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' after match expression")
        
        patterns = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            # 解析模式
            pattern = self._parse_pattern()
            
            # 解析守卫条件（可选）
            guard = None
            if self._match(TokenType.IDENTIFIER) and self.tokens[self.position - 1].value == "if":
                guard = self._parse_expression()
            
            self._consume(TokenType.FAT_ARROW, "Expected '=>' after pattern")
            
            # 解析表达式体
            body = self._parse_expression()
            
            patterns.append(PatternCase(pattern, guard, body))
            
            if not self._match(TokenType.COMMA):
                break
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after match patterns")
        
        return PatternMatch(expression, patterns)
    
    def _parse_pattern(self) -> Expression:
        """解析模式"""
        if self._check(TokenType.IDENTIFIER):
            name = self._consume(TokenType.IDENTIFIER, "Expected pattern identifier").value
            
            # 检查是否为构造器模式
            if self._match(TokenType.LEFT_PAREN):
                args = []
                if not self._check(TokenType.RIGHT_PAREN):
                    while True:
                        arg_pattern = self._parse_pattern()
                        args.append(arg_pattern)
                        
                        if not self._match(TokenType.COMMA):
                            break
                
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after pattern arguments")
                return Call(Identifier(name), args)
            
            # 检查是否为类型模式
            if self._match(TokenType.COLON):
                type_expr = self._parse_type_expression()
                return BinaryOp(Identifier(name), ":", type_expr)
            
            return Identifier(name)
        
        # 字面量模式
        return self._parse_primary()
    
    def _parse_lambda_expression(self) -> LambdaExpression:
        """解析 lambda 表达式"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' in lambda")
        
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                param_name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
                param_type = None
                
                if self._match(TokenType.COLON):
                    param_type = self._parse_type_expression()
                
                parameters.append((param_name, param_type))
                
                if not self._match(TokenType.COMMA):
                    break
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after lambda parameters")
        
        # 检查是否为异步 lambda
        is_async = False
        if self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "async":
            self._advance()
            is_async = True
        
        self._consume(TokenType.FAT_ARROW, "Expected '=>' in lambda")
        
        body = self._parse_expression()
        
        return LambdaExpression(parameters, body, is_async)
    
    def _parse_list_comprehension(self) -> ListComprehension:
        """解析列表推导式"""
        self._consume(TokenType.LEFT_BRACKET, "Expected '[' in list comprehension")
        
        expression = self._parse_expression()
        
        # 解析生成器子句
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
            
            generators.append(ComprehensionClause(variable, iterable, condition))
        
        self._consume(TokenType.RIGHT_BRACKET, "Expected ']' in list comprehension")
        
        return ListComprehension(expression, generators)
    
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
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before class body")
        
        fields = []
        methods = []
        
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
    
    def _parse_interface_declaration(self) -> InterfaceDeclaration:
        """解析接口声明"""
        name = self._consume(TokenType.IDENTIFIER, "Expected interface name").value
        
        # 解析类型参数
        type_parameters = []
        if self._match(TokenType.LESS):
            while not self._check(TokenType.GREATER):
                param_name = self._consume(TokenType.IDENTIFIER, "Expected type parameter name").value
                type_parameters.append(param_name)
                
                if not self._match(TokenType.COMMA):
                    break
            self._consume(TokenType.GREATER, "Expected '>' after type parameters")
        
        self._consume(TokenType.LEFT_BRACE, "Expected '{' before interface body")
        
        methods = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            if self._match(TokenType.FUNC):
                method = self._parse_function_declaration()
                methods.append(method)
            else:
                break
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after interface body")
        
        return InterfaceDeclaration(name, type_parameters, methods)
    
    def _parse_expression(self) -> Optional[Expression]:
        """重写表达式解析，支持更多特性"""
        # 检查 lambda 表达式
        if self._check(TokenType.LEFT_PAREN):
            # 可能是 lambda 或普通表达式
            saved_position = self.position
            try:
                return self._parse_lambda_expression()
            except:
                self.position = saved_position
                return super()._parse_expression()
        
        # 检查 await 表达式
        if self._match(TokenType.AWAIT):
            return self._parse_await_expression()
        
        # 检查列表推导式
        if self._check(TokenType.LEFT_BRACKET):
            saved_position = self.position
            try:
                return self._parse_list_comprehension()
            except:
                self.position = saved_position
                return super()._parse_expression()
        
        # 检查模式匹配
        if self._match(TokenType.MATCH):
            return self._parse_pattern_match()
        
        return super()._parse_expression()
    
    def _parse_statement(self) -> Optional[Statement]:
        """重写语句解析，支持更多特性"""
        # 检查数据类声明
        if self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "data":
            self._advance()  # consume 'data'
            return self._parse_data_class_declaration()
        
        # 检查接口声明
        if self._match(TokenType.INTERFACE):
            return self._parse_interface_declaration()
        
        # 检查异步函数声明
        if self._check(TokenType.IDENTIFIER) and self.tokens[self.position].value == "async":
            self._advance()  # consume 'async'
            self._consume(TokenType.FUNC, "Expected 'func' after 'async'")
            return self._parse_async_function_declaration()
        
        return super()._parse_statement()

def parse_advanced_program(tokens: List[Token]) -> Program:
    """解析高级程序"""
    parser = AdvancedParser(tokens)
    return parser.parse()

if __name__ == "__main__":
    # 测试高级解析器
    from lexer import Lexer
    
    test_code = '''
    data User<T> {
        name: string
        age: int
        data: T
    }
    
    async func fetchUser(id: int): Promise<User<string>> {
        let userData = await http.get("/users/" + id);
        return User{name: userData.name, age: userData.age, data: userData.bio};
    }
    
    func processUsers(users: [User<string>]) -> [string] {
        return [user.name | for user in users if user.age > 18];
    }
    
    func main() {
        let user = match getUserType() {
            "admin" => fetchAdminUser(1)
            "guest" => fetchGuestUser(1)
            _ => createDefaultUser()
        };
        
        let processedNames = processUsers([user]);
        println(processedNames);
    }
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = AdvancedParser(tokens)
    ast = parser.parse()
    
    print("=== 高级语法解析结果 ===")
    print(f"解析出 {len(ast.statements)} 个语句")
    
    for i, stmt in enumerate(ast.statements):
        print(f"语句 {i}: {type(stmt).__name__}")
        if hasattr(stmt, 'name'):
            print(f"  名称: {stmt.name}")
        if hasattr(stmt, 'type_parameters'):
            print(f"  类型参数: {stmt.type_parameters}")
