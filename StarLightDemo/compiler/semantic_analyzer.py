#!/usr/bin/env python3
"""
Starlight 编程语言 - 语义分析器
负责语义分析、符号表管理、作用域检查等
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from .parser import ASTNode, Program, FunctionDeclaration, VariableDeclaration, Identifier, Call, Expression
from .lexer import Token

class SymbolType(Enum):
    VARIABLE = "variable"
    FUNCTION = "function"
    TYPE = "type"
    PARAMETER = "parameter"

@dataclass
class Symbol:
    name: str
    type: SymbolType
    data_type: Optional[str] = None
    is_const: bool = False
    scope_level: int = 0
    node: Optional[ASTNode] = None

@dataclass
class Scope:
    symbols: Dict[str, Symbol] = field(default_factory=dict)
    parent: Optional['Scope'] = None
    level: int = 0
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """在当前作用域查找符号"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def declare(self, symbol: Symbol) -> bool:
        """在当前作用域声明符号"""
        if symbol.name in self.symbols:
            return False  # 符号已存在
        symbol.scope_level = self.level
        self.symbols[symbol.name] = symbol
        return True
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """获取所有符号（包括父作用域）"""
        all_symbols = {}
        if self.parent:
            all_symbols.update(self.parent.get_all_symbols())
        all_symbols.update(self.symbols)
        return all_symbols

class SemanticError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors: List[SemanticError] = []
        self.warnings: List[str] = []
        
        # 内置类型
        self.builtin_types = {
            'int', 'float', 'string', 'boolean', 'void', 'any',
            'List', 'Map', 'Set', 'Array', 'Optional'
        }
        
        # 内置函数
        self.builtin_functions = {
            'println', 'print', 'readLine', 'readInt', 'readFloat',
            'length', 'toString', 'parseInt', 'parseFloat'
        }
    
    def analyze(self, program: Program) -> Dict[str, Any]:
        """执行语义分析"""
        self.errors.clear()
        self.warnings.clear()
        
        try:
            # 分析程序
            self._analyze_program(program)
            
            return {
                'success': len(self.errors) == 0,
                'errors': [{'message': e.message, 'line': e.line, 'column': e.column} for e in self.errors],
                'warnings': self.warnings,
                'symbols': self._get_all_symbols()
            }
        except Exception as e:
            self.errors.append(SemanticError(f"语义分析错误: {str(e)}"))
            return {
                'success': False,
                'errors': [{'message': e.message, 'line': e.line, 'column': e.column} for e in self.errors],
                'warnings': self.warnings,
                'symbols': {}
            }
    
    def _analyze_program(self, program: Program):
        """分析程序"""
        # 第一遍：收集所有声明
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration):
                self._collect_function_declaration(stmt)
            elif isinstance(stmt, VariableDeclaration):
                self._collect_variable_declaration(stmt)
        
        # 第二遍：分析语句
        for stmt in program.statements:
            self._analyze_statement(stmt)
    
    def _collect_function_declaration(self, func: FunctionDeclaration):
        """收集函数声明"""
        if func.name in self.current_scope.symbols:
            self.errors.append(SemanticError(
                f"函数 '{func.name}' 已存在", 
                func.node.line if hasattr(func, 'node') else 0
            ))
            return
        
        symbol = Symbol(
            name=func.name,
            type=SymbolType.FUNCTION,
            data_type=func.return_type or 'void',
            node=func
        )
        
        self.current_scope.declare(symbol)
    
    def _collect_variable_declaration(self, var: VariableDeclaration):
        """收集变量声明"""
        if var.name in self.current_scope.symbols:
            self.errors.append(SemanticError(
                f"变量 '{var.name}' 已存在",
                var.node.line if hasattr(var, 'node') else 0
            ))
            return
        
        symbol = Symbol(
            name=var.name,
            type=SymbolType.VARIABLE,
            data_type=var.type_annotation or self._infer_type(var.initializer),
            is_const=var.is_const,
            node=var
        )
        
        self.current_scope.declare(symbol)
    
    def _analyze_statement(self, stmt: ASTNode):
        """分析语句"""
        if isinstance(stmt, FunctionDeclaration):
            self._analyze_function_declaration(stmt)
        elif isinstance(stmt, VariableDeclaration):
            self._analyze_variable_declaration(stmt)
        elif hasattr(stmt, 'expression'):
            self._analyze_expression(stmt.expression)
    
    def _analyze_function_declaration(self, func: FunctionDeclaration):
        """分析函数声明"""
        # 创建新的作用域
        old_scope = self.current_scope
        self.current_scope = Scope(parent=old_scope, level=old_scope.level + 1)
        
        try:
            # 声明参数
            for param_name, param_type in func.parameters:
                param_symbol = Symbol(
                    name=param_name,
                    type=SymbolType.PARAMETER,
                    data_type=param_type or 'any',
                    node=None
                )
                self.current_scope.declare(param_symbol)
            
            # 先收集函数体内的变量声明
            for stmt in func.body:
                if isinstance(stmt, VariableDeclaration):
                    self._collect_variable_declaration(stmt)
            
            # 然后分析函数体
            for stmt in func.body:
                self._analyze_statement(stmt)
                
        finally:
            # 恢复作用域
            self.current_scope = old_scope
    
    def _analyze_variable_declaration(self, var: VariableDeclaration):
        """分析变量声明"""
        if var.initializer:
            self._analyze_expression(var.initializer)
            
            # 类型检查
            if var.type_annotation:
                inferred_type = self._infer_type(var.initializer)
                if inferred_type and inferred_type != var.type_annotation:
                    self.warnings.append(
                        f"变量 '{var.name}' 类型不匹配: 声明为 {var.type_annotation}, 推断为 {inferred_type}"
                    )
    
    def _analyze_expression(self, expr: Expression):
        """分析表达式"""
        if isinstance(expr, Identifier):
            self._analyze_identifier(expr)
        elif isinstance(expr, Call):
            self._analyze_call(expr)
        elif hasattr(expr, 'left') and hasattr(expr, 'right'):
            # 二元操作
            self._analyze_expression(expr.left)
            self._analyze_expression(expr.right)
        elif hasattr(expr, 'operand'):
            # 一元操作
            self._analyze_expression(expr.operand)
    
    def _analyze_identifier(self, ident: Identifier):
        """分析标识符"""
        symbol = self.current_scope.lookup(ident.name)
        if not symbol:
            # 检查是否为内置函数
            if ident.name not in self.builtin_functions:
                self.errors.append(SemanticError(
                    f"未定义的标识符 '{ident.name}'",
                    ident.node.line if hasattr(ident, 'node') else 0
                ))
    
    def _analyze_call(self, call: Call):
        """分析函数调用"""
        # 分析被调用的函数
        if isinstance(call.callee, Identifier):
            symbol = self.current_scope.lookup(call.callee.name)
            if not symbol:
                if call.callee.name not in self.builtin_functions:
                    self.errors.append(SemanticError(
                        f"未定义的函数 '{call.callee.name}'",
                        call.node.line if hasattr(call, 'node') else 0
                    ))
        
        # 分析参数
        for arg in call.arguments:
            self._analyze_expression(arg)
    
    def _infer_type(self, expr: Expression) -> Optional[str]:
        """推断表达式类型"""
        if hasattr(expr, 'value') and hasattr(expr, 'type'):
            # 字面量
            return expr.type
        elif isinstance(expr, Identifier):
            symbol = self.current_scope.lookup(expr.name)
            if symbol:
                return symbol.data_type
        elif isinstance(expr, Call):
            if isinstance(expr.callee, Identifier):
                symbol = self.current_scope.lookup(expr.callee.name)
                if symbol:
                    return symbol.data_type
        return None
    
    def _get_all_symbols(self) -> Dict[str, Any]:
        """获取所有符号信息"""
        symbols = {}
        all_symbols = self.current_scope.get_all_symbols()
        
        for name, symbol in all_symbols.items():
            symbols[name] = {
                'type': symbol.type.value,
                'data_type': symbol.data_type,
                'is_const': symbol.is_const,
                'scope_level': symbol.scope_level
            }
        
        return symbols
    
    def enter_scope(self):
        """进入新的作用域"""
        self.current_scope = Scope(parent=self.current_scope, level=self.current_scope.level + 1)
    
    def exit_scope(self):
        """退出当前作用域"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        else:
            raise SemanticError("无法退出全局作用域")
    
    def declare_symbol(self, name: str, symbol_type: SymbolType, data_type: str = None, is_const: bool = False) -> bool:
        """在当前作用域声明符号"""
        symbol = Symbol(
            name=name,
            type=symbol_type,
            data_type=data_type,
            is_const=is_const
        )
        return self.current_scope.declare(symbol)
    
    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """查找符号"""
        return self.current_scope.lookup(name)

def analyze_program(program: Program) -> Dict[str, Any]:
    """分析程序的语义"""
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)

if __name__ == "__main__":
    # 测试语义分析器
    from parser import parse_file
    from lexer import lex_file
    
    # 创建测试程序
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, " + name;
    }
    
    let message = greet("World");
    let count: int = 42;
    '''
    
    from lexer import Lexer
    from parser import Parser
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(ast)
    
    print("=== 语义分析结果 ===")
    print(f"成功: {result['success']}")
    print(f"错误数: {len(result['errors'])}")
    print(f"警告数: {len(result['warnings'])}")
    
    if result['errors']:
        print("\n错误:")
        for error in result['errors']:
            print(f"  - {error['message']}")
    
    if result['warnings']:
        print("\n警告:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    print(f"\n符号表:")
    for name, info in result['symbols'].items():
        print(f"  {name}: {info['type']} ({info['data_type']})")
